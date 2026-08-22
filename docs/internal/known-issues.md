# Known Issues — YouTube-Description-Generator

Concrete defects and gaps found while writing this repository's documentation in
August 2026. **Nothing here was changed** — each one needs a code, configuration, or
licensing decision rather than a documentation one.

Ordered by severity. See [`docs/roadmap.md`](../roadmap.md) for the narrative version,
which also covers deliberate non-goals.

**5 open:** 1 high, 3 medium, 1 low.

## 1. summarize overwrites the captions it consumed, and describe will not regenerate them

**Severity:** High
**Where:** `src/youtube_description_generator/summarize_descriptions.py` -> `process_frame_folders`; `src/youtube_description_generator/describe_frames.py` -> `describe_images_in_folder`

**What:** `process_frame_folders` reads `description.txt`, sends it to Ollama, and writes the result back to the same path: `desc_file.write_text(summarized, encoding="utf-8")`. The BLIP captions are replaced. `describe_images_in_folder` begins with `if output_file.exists(): return`, so it will not recreate them.

**Why it matters:** The pipeline's whole design is that stages are independent and re-runnable -- files on disk between steps, `describe` skipping completed folders, four separate subcommands. This breaks that for the one stage most likely to need re-running, since the prompt is the documented customisation point. Running `ytdg summarize` twice feeds the summary back as if it were captions, producing a summary of a summary with no indication anything is wrong -- the file has the same name and plausible contents either way. Recovering the captions means deleting `description.txt` and re-running the most expensive step in the pipeline, one BLIP pass per frame per video.

**Suggested fix:** Write to `summary.txt` beside the captions and have `collect` prefer it. That makes `summarize` idempotent, lets the prompt be iterated on without re-captioning, and costs one changed filename. If overwriting is wanted, at least detect already-summarised input and skip it.

## 2. No timeout on the Ollama subprocess

**Severity:** Medium
**Where:** `src/youtube_description_generator/summarize_descriptions.py` -> `summarize_description`

**What:** `subprocess.run([ollama_path, "run", "llama3.1:8b"], input=..., capture_output=True, check=False)` -- no `timeout` argument. `capture_output=True` also means nothing is printed while it runs.

**Why it matters:** A model that stalls -- an Ollama server that is up but not responding, a machine swapping under an 8B model, a partial pull -- hangs the batch indefinitely with no output at all. Because output is captured, the run looks identical to one that is simply slow, and `describe` has already trained the user to expect slow. A batch left running overnight can make no progress past its first video.

**Suggested fix:** Pass a `timeout` (a few minutes is generous for one summary) and convert `subprocess.TimeoutExpired` into the same per-folder failure the surrounding `except` already handles, so one stuck video does not stop the batch.

## 3. collect walks every subdirectory, not just *_frames folders

**Severity:** Medium
**Where:** `src/youtube_description_generator/collect_files.py` -> `collect_descriptions`

**What:** `for folder in sorted(p for p in base_dir.iterdir() if p.is_dir())` -- every immediate subdirectory is checked for a `description.txt` and, if present, the file is **moved** out and renamed. The other three stages all filter on the `_frames` suffix; this one does not. It is a faithful port of `move_files.bat`, which had the same behaviour.

**Why it matters:** `description.txt` is not an unusual filename. Any unrelated subfolder in the working directory that happens to contain one has it silently relocated and renamed after that folder -- and `shutil.move` is not a copy, so the original is gone. Users are told to `cd` into their video folder and run `ytdg run`, which is exactly the situation where other directories are present.

**Suggested fix:** Filter on `folder.name.endswith("_frames")`, matching the rest of the pipeline. The Windows batch file has the same issue if it is kept.

## 4. The documented output filename does not match what collect produces

**Severity:** Medium
**Where:** `README.md` (corrected in this pass), `src/youtube_description_generator/collect_files.py` -> `unique_target`

**What:** The README stated the collect step produces `{video}.txt`, in both the step table ('Moves each `description.txt` out of its frame folder, renamed `{video}.txt`') and the command list. `unique_target` builds `base_dir / f"{folder_name}.txt"` from the **folder** name, which is `{video}_frames` -- so the real output is `{video}_frames.txt`. `tests/test_collect_files.py` asserts `video1_frames.txt`, so the behaviour is intended and the documentation was wrong.

**Why it matters:** The output filename is the pipeline's entire deliverable -- the thing the user opens and pastes into YouTube. Documenting it wrongly means a script or a workflow built on the README looks for files that do not exist, and the failure is a silent no-match rather than an error. It also makes the finished artefact carry an internal implementation detail (`_frames`) in its name.

**Suggested fix:** The README is corrected. Whether to change the behaviour is a separate call: naming the output after the video rather than the folder is friendlier, and would mean stripping the `_frames` suffix in `unique_target` and updating its tests.

## 5. Frames are reached by seeking rather than read sequentially

**Severity:** Low
**Where:** `src/youtube_description_generator/extract_frames.py` -> `extract_frames`

**What:** For each second, the code does `cap.set(cv2.CAP_PROP_POS_FRAMES, int(second * fps))` then `cap.read()`. `fps` comes from `CAP_PROP_FPS` and the loop runs to `int(total_frames / fps) + 1`.

**Why it matters:** Seeking to an exact frame is unreliable on long-GOP codecs and variable-frame-rate footage -- screen recordings and phone video are commonly VFR -- because the decoder may land on the nearest keyframe instead. The result is frames that are not one second apart, or duplicates, which silently degrades the captions the whole pipeline is built on. Seeking is also slower than a sequential read for this access pattern. The `+ 1` separately means the final seek usually lands past the end, producing a spurious warning on nearly every video.

**Suggested fix:** Read sequentially and keep every `round(fps)`-th frame, counting as you go. That is both faster and correct for VFR. Drop the `+ 1` while you are there.

---

## Also, across every repository

**`.bandit` is present on disk but untracked in git.** Verified in PyWorkout, treklogger,
skyscanner-cli, booking-cli, piggy, and aibot — the config file exists locally in each but
`git ls-files` does not know about it, so none of it reached GitHub.

The August 2026 security sweep therefore looks complete locally and landed nowhere. Worth
checking across all 44 repositories it covered.

# YouTube Description Generator — FAQ

## Does my video get uploaded anywhere?

No. BLIP runs locally through Transformers and the LLM runs locally through Ollama. There is no
API key and no network call after the one-time model downloads.

For unpublished video that is the whole point — a cloud captioning service would mean sending
footage you have not released.

## Why is it so slow?

`describe` runs BLIP once per extracted frame, and frames are sampled once per second. A
60-second Short is 60 model passes. A CUDA GPU makes a large difference; on CPU, expect minutes
per video.

The other three steps are fast.

## Can I re-run a step?

`extract`, `describe`, and `collect`, yes. `describe` even skips folders that already have a
`description.txt`, so it resumes cleanly after an interruption.

**`summarize` is the exception.** It writes its output back over `description.txt`, so running it
twice summarises its own summary — and `describe` will not regenerate the captions, because the
file exists. Delete `description.txt` to start a video over. See
[`internal/known-issues.md`](./internal/known-issues.md).

## Why is my output file called `myvideo_frames.txt`?

`collect` names the result after the folder it came from, and the folder is `{video}_frames`. It
is what the code, its tests, and `move_files.bat` all do; earlier documentation said `{video}.txt`
and was wrong.

## How do I change the tone of the output?

Edit the prompt in `summarize_descriptions.py`. It is the intended customisation point — there is
no configuration file. See [Configuration](./configuration.md).

## Can I use a different LLM?

Yes: change the model name in `summarize_descriptions.py` and `ollama pull` it. The model choice
affects the writing style more than the prompt does.

## Can I use a better captioning model?

`describe_frames.py` names `Salesforce/blip-image-captioning-base`. A larger BLIP variant gives
better captions at proportionally more time.

## Do I need Ollama for everything?

No — only `summarize`. Extract, describe, and collect run without it.

## Why one frame per second?

It suits Shorts: a minute of video gives sixty captions, enough signal for a summary without an
unbearable describe step. Not configurable.

## The captions are wrong or repetitive

BLIP describes single images with no temporal context, so a static shot produces sixty nearly
identical lines. The LLM step exists partly to absorb that. A larger captioning model helps; so
does a video that changes.

## Is the output good enough to paste directly?

Usually as a starting point. It is a small local model working from image captions, not a
copywriter — read it before uploading, particularly the hashtags.

## Does it need internet?

Only for the initial model downloads. After that, no.

## Is there a Windows-specific version?

`move_files.bat` predates the cross-platform `ytdg collect` and does the same thing. Use the
command.

## It hangs on summarize

There is no timeout on the Ollama call. Check Ollama is running and the model is pulled, then
interrupt and retry. See [`internal/known-issues.md`](./internal/known-issues.md).

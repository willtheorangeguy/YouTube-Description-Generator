# YouTube Description Generator — Development

## Setup

```bash
git clone https://github.com/willtheorangeguy/YouTube-Description-Generator.git
cd YouTube-Description-Generator
pip install -e .
python -m unittest discover -s tests -v
```

## Tests

```bash
python -m unittest discover -s tests -v
python -m unittest tests.test_summarize_descriptions -v
```

The suite mocks OpenCV, PyTorch, and Transformers, so:

```bash
pip install -e . --no-deps
python -m unittest discover -s tests -v
```

is enough — which is exactly what CI does, on Python 3.9 through 3.12, for every push and pull
request. No model downloads, no GPU, no Ollama.

That is only possible because `describe_frames.py` imports `torch` and `transformers` **inside**
`_load_model` rather than at module scope. Moving those imports to the top of the file would make
CI download PyTorch on every run. Keep them where they are.

| Test file | Covers |
|---|---|
| `test_cli.py` | Subcommand dispatch and directory defaults |
| `test_extract_frames.py` | Frame extraction, with OpenCV mocked |
| `test_describe_frames.py` | Captioning and the skip-existing behaviour |
| `test_summarize_descriptions.py` | Prompt construction and the subprocess call |
| `test_collect_files.py` | Moving, renaming, and collision suffixes |

## Conventions

- **Stages communicate through files**, not return values. A new stage should read a directory
  and write into it.
- **Heavy imports stay inside functions.** It is what keeps the tests light.
- **Subprocess calls: absolute path, list argv, input on stdin.** `summarize_descriptions.py`
  does all three, with `# nosec` comments recording why. Do not regress that into `shell=True`.
- **Pin model revisions.** BLIP is loaded with an explicit `revision`; anything else third-party
  should be too.

## Changing the prompt

It is a literal in `summarize_descriptions.py`, and the intended customisation point. Note that
`test_summarize_descriptions.py` asserts on the prompt's construction, so a change there means
updating the test.

## Adding a stage

Add the module, a subcommand in `cli.py`, an entry in `run`, and a test with the heavy
dependencies mocked. Write output to a **new filename** rather than overwriting an input — see
[`internal/known-issues.md`](./internal/known-issues.md) for why that matters here.

## CI

`.github/workflows/tests.yml` runs the suite on 3.9–3.12 for every push and pull request.

## Recording defects

Bugs found while working here go in [`internal/known-issues.md`](./internal/known-issues.md)
rather than being fixed in passing, unless fixing them is the job you are on.

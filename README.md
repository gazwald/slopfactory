# Resume Converter

Load a PDF copy of a resume into a Pydantic model using ollama.

Original use case for this was to turn an unstructured document like a resume
into JSON or similar for easy reworking into different templates.

**Important**: In it's default setup this will be slow! If you care about
iterating quickly on this then read the [ollama
docs](https://github.com/ollama/ollama?tab=readme-ov-file#ollama).

## Requirements

- Docker
- Docker Compose
- GPU (optional but slow)

All testing for this was done on Linux, and the app creates symlinks for
convenience. If you're using an OS/FS that doesn't support those you should
switch to one that does, or rip out the code that creates them.

## Usage

1. Clone the repo

1. Copy your resume into `./inputs/resume.pdf`

1. Run it:

    ```console
    ./scripts/run
    ```

1. Watch as your CPU churns merrily away

1. Check `./outputs/`:

    ```console
    $ jq < outputs/1752490190069971865_resume.json
    {
      "personal": {
        "contact": null,
        "location": "Victoria, Australia",
        "name": "Gary Brandon",
        "description": "Just a human person doing normal human person things",
        "pronouns": null,
        "title": null
      },
      "history": [
    ...
    ```

## Performance

By default it's using the CPU for ollama which will be slow. Ollama has
GPU-specific image builds depending on what GPU manufacturer you have; their
docs:

- [nvidia](https://hub.docker.com/r/ollama/ollama#nvidia-gpu)
- [amd](https://hub.docker.com/r/ollama/ollama#amd-gpu)

## Model

Play around with the [model](https://ollama.com/library) used as the default
one that I've picked was chosen due to it's size above all else.

I've generally had decent success with `qwen3:8b`.

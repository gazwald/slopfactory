ARG BASE_IMAGE=docker.io/library/python:3.13-slim-bookworm

FROM $BASE_IMAGE AS deps

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=./requirements.txt \
    pip install -r requirements.txt

FROM deps AS app

COPY . .

ENTRYPOINT ["python", "app.py"]

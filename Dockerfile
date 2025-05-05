FROM python:2.7
WORKDIR /app
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY . /app
RUN pip install .[test]
CMD ["pytest", "-s", "--log-cli-level=DEBUG"]

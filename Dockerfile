FROM python:2

COPY src /src

COPY run_pi /

RUN python -m pip install /src/madrob_beast_pi/

# Benchmark type and PI name: given when the docker image is built
ARG BENCHMARK_TYPE
ENV BENCHMARK_TYPE=$BENCHMARK_TYPE

ARG PI_NAME
ENV SCRIPT_NAME=$PI_NAME

ENV PATH="/:${PATH}"

RUN chmod +x /run_pi
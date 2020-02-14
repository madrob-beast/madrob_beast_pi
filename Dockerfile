FROM python:2

RUN git clone https://github.com/madrob-beast/madrob_beast_pi.git

RUN python -m pip install madrob_beast_pi/

# Benchmark type and PI name: given when the docker image is built
ARG BENCHMARK_TYPE
ENV BENCHMARK_TYPE=$BENCHMARK_TYPE

ARG PI_NAME
ENV SCRIPT_NAME=$PI_NAME

ENV PATH="/madrob_beast_pi:${PATH}"

RUN chmod +x /madrob_beast_pi/run_pi
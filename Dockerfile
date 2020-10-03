FROM python:2

COPY src /src

RUN python -m pip install /src/madrob_beast_pi/

MADROB-BEAST Performance Indicators
=================================================

Scripts to calculate performance indicators for the MADROB and BEAST benchmarks, from the Eurobench project.

## Installing the library
Pip can be used to install this module locally:
```
git clone https://github.com/madrob-beast/madrob_beast_pi.git
python -m pip install src/madrob_beast_pi/
```

**Note**: When adding or modifying Performance Indicators, run the installation command again. To keep the PIs up-to-date, run `git pull` and the installation command.

## Docker

The Dockerfile in this project can be used to build Docker images for every PI:
when building, set the `BENCHMARK_TYPE` and `PI_NAME` params to the specific PI ones. E.g. for the 'madrob' benchmark, Performance Indicator 'execution_time':
```
docker build --build-arg BENCHMARK_TYPE=madrob --build-arg PI_NAME=execution_time -t=madrob_execution_time .
```
This creates an image named `madrob_execution_time`. (The `make_docker_images.py` script can create all required images, as mentioned below).

If we run a container from this image and call the `run_pi` command, 
the Performance Indicator will be run.

Assuming `test_data/` contains input data, and the output directory `out_folder/` exists:
```
docker run --rm -v $PWD/test_data:/in -v $PWD/out_folder:/out madrob_execution_time ./run_pi /in/events.csv /in/testbed_config.yaml /out
```

## Creating all Docker images

The script `make_docker_images.py` builds Docker images for all the Performance Indicators in the 'madrob' and 'beast' directories:
```
python make_docker_images.py
```
**Note**: The script runs `"sudo docker ..."`. To run docker in user mode, modify the script.

## Test data

The `test_data/` directory contains preprocessed `.csv` files and a testbed configuration `.yaml` file. These files are from a real benchmark run, and can be used as test input to the `run_pi` command.
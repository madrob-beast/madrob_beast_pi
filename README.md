MADROB-BEAST Performance Indicators
=================================================

Scripts to calculate performance indicators for the MADROB and BEAST benchmarks, from the Eurobench project.

## Installing the library
Pip can be used to install this module locally:
```
git clone https://github.com/madrob-beast/madrob_beast_pi.git
python -m pip install madrob_beast_pi/
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
the Performance Indicator will be run:
```
docker run --name madrob_execution_time -dit madrob_execution_time
docker exec -it madrob_execution_time run_pi madrob_beast_pi/test_data/events_sequence.csv madrob_beast_pi/test_data/testbed_config.yaml .
```

## Creating all Docker images

The script `make_docker_images.py` builds Docker images for all the Performance Indicators in the 'madrob' and 'beast' directories. **Note**: the Dockerfile clones the code from this repo. So when adding a new PI test it locally first, then push it to the repository, and then run the script:
```
python make_docker_images.py
```

## Test data

The `test_data/` directory contains preprocessed `.csv` files and a testbed configuration `.yaml` file. These files are from a real benchmark run, and can be used as test input to the `run_pi` command.
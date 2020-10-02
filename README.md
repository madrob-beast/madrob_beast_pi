MADROB-BEAST Performance Indicators
=================================================

Scripts to calculate performance indicators for the MADROB and BEAST benchmarks, from the Eurobench project.

## Installing the library

Pip can be used to install this module locally:

```term
git clone https://github.com/madrob-beast/madrob_beast_pi.git
cd madrob_beast_pi
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
#python -m pip install src/madrob_beast_pi/
pip install -e src/madrob_beast_pi
```

Using the virtual environment, the package and dependencies is installed locally in the folder `venv`.
To deactivate the virtual environment, type `deactivate`.

To install permanently the code, only use the last command.

**Note**: When adding or modifying Performance Indicators, run the installation command again.
To keep the PIs up-to-date, run `git pull` and the installation command.

## Usage

### Madrob

All PI associated to madrob can be launched using (Assuming folder `out_tests` exists):

```term
run_madrob tests/madrob/input/events.csv tests/madrob/input/wrench.csv tests/madrob/input/jointState.csv tests/madrob/input/testbed_config.yaml out_tests
```

## Docker

The Dockerfile in this project can be used to build Docker images for every PI:
when building, set the `BENCHMARK_TYPE` and `PI_NAME` params to the specific PI ones. E.g. for the 'madrob' benchmark, Performance Indicator 'execution_time':

```term
docker build --build-arg BENCHMARK_TYPE=madrob --build-arg PI_NAME=execution_time -t=madrob_execution_time .
```

This creates an image named `madrob_execution_time` (the `make_docker_images.py` script can create all required images, as mentioned below).

If we run a container from this image and call the `run_pi` command,
the Performance Indicator will be run.

Assuming `test_data/` contains input data, and the output directory `out_folder/` exists:

```term
docker run --rm -v $PWD/test_data:/in -v $PWD/out_folder:/out madrob_execution_time ./run_pi /in/events.csv /in/testbed_config.yaml /out
```

## Creating all Docker images

The script `make_docker_images.py` builds Docker images for all the Performance Indicators in the 'madrob' and 'beast' directories:

```term
python make_docker_images.py
```

**Note**: The script runs `"sudo docker ..."`. To run docker in user mode, modify the script.

## Test data

The [tests](tests) directory contains preprocessed `.csv` files and a testbed configuration `.yaml` file.
These files are from a real benchmark run, and can be used as test input to the `run_pi` command.

## Acknowledgements

<a href="http://eurobench2020.eu">
  <img src="http://eurobench2020.eu/wp-content/uploads/2018/06/cropped-logoweb.png"
       alt="rosin_logo" height="60" >
</a>

Supported by Eurobench - the European robotic platform for bipedal locomotion benchmarking.
More information: [Eurobench website][eurobench_website]

<img src="http://eurobench2020.eu/wp-content/uploads/2018/02/euflag.png"
     alt="eu_flag" width="100" align="left" >

This project has received funding from the European Union’s Horizon 2020
research and innovation programme under grant agreement no. 779963.

The opinions and arguments expressed reflect only the author‘s view and
reflect in no way the European Commission‘s opinions.
The European Commission is not responsible for any use that may be made
of the information it contains.

[eurobench_logo]: http://eurobench2020.eu/wp-content/uploads/2018/06/cropped-logoweb.png
[eurobench_website]: http://eurobench2020.eu "Go to website"

MADROB-BEAST Performance Indicators
=================================================

## Purposes

Scripts to calculate performance indicators for the MADROB and BEAST benchmarks, from the Eurobench project.
Two algorithms have been implemented: `pi_bullet_walking` and `pi_bullet_walkingComplete`.

### Madrob PIs

The following PIs are implemented:

- `capability_level`
- `execution_time`
- `time_to_handle`
- `door_occupation_time`
- `passage_time`
- `roughness_of_door_actuation`
- `smoothness_of_door_actuation`
- `unsafety_of_door_operation`

The PIs require the condition file `condition_Y.yaml` and the following preprocessed data files:

- `subject_X_cond_Y_run_Z_event.csv`
- `subject_X_cond_Y_run_Z_jointState.csv`
- `subject_X_cond_Y_run_Z_wrench.csv`

### Beast PIs

The following PIs are implemented:

- `capability_level`
- `time_to_grip_handle`
- `time_to_checkpoint_1..5`
- `roughness_of_actuation`
- `safety_of_navigation`

The PIs require the condition file `condition_Y.yaml` and the following preprocessed data files:

- `subject_X_cond_Y_run_Z_event.csv`
- `subject_X_cond_Y_run_Z_distance.csv`
- `subject_X_cond_Y_run_Z_wrench.csv`


### Note on PIs and pre-processed data

Each PI writes the result to a `yaml` file with the same name of the PI.
Example: The `capability_level` PI write the results to `capability_level.yaml`.

For both Madrob and Beast, `X`, `Y`, `Z` are the subject number, condition number and run number respectively.
The preprocessed data files are generated during the benchmark execution and are named following the specification in [experiment_data](https://github.com/aremazeilles/eurobench_documentation/blob/master/modules/ROOT/pages/experiment_data.adoc#Experimental%20data).
The preprocessed files and raw data files are collected in a different directory for each run, named `subject_X_cond_Y_run_Z_T`, where T is a timestamp that ensures each run is saved in a different directory.
Note that files referring to the same condition (e.g., condition_1.yaml) are present in multiple run directories, but have the same content.


## Installing the library

Pip can be used to install this module locally:

```term
git clone https://github.com/madrob-beast/madrob_beast_pi.git
cd madrob_beast_pi
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -e src/madrob_beast_pi
```

Using the virtual environment, the package and dependencies is installed locally in the folder `venv`.
To deactivate the virtual environment, type `deactivate`.

To install permanently the code, only use the last command.

**Note**: When adding or modifying Performance Indicators, run the installation command again.
To keep the PIs up-to-date, run `git pull` and the installation command.

## Usage

All PI associated to madrob can be launched using (assuming folder `out_tests` exists):

```term
run_madrob tests/madrob/input/subject_001_cond_001_run_001_event.csv tests/madrob/input/subject_001_cond_001_run_001_wrench.csv tests/madrob/input/subject_001_cond_001_run_001_jointState.csv tests/madrob/input/condition_1.yaml out_tests
```

All PI associated to beast can be launched using (assuming folder `out_tests` exists):

```term
run_beast tests/beast/input/subject_001_cond_001_run_001_event.csv tests/beast/input/subject_001_cond_001_run_001_distance.csv tests/beast/input/subject_001_cond_001_run_001_wrench.csv tests/beast/input/condition_1.yaml out_tests
```
TODO: collect beast test data and update the names in this example (if using a different condition)

## Docker image

### Build from source

The Dockerfile in this project can be used to build the Docker image for madrob and beast:

```term
docker build -t=pi_madrob_beast .
```

### Use official image

An image is available from the [Docker Hub](https://hub.docker.com/r/eurobenchtest/pi_madrob_beast).
It can be directly installed on a Linux machine using:

```term
docker pull eurobenchtest/pi_madrob_beast
```

### Launch the docker image

#### Madrob

Assuming the tests/madrob/input contains the input data, the PI output will be written to `out_tests`:

```term
docker run --rm -v $PWD/tests/madrob/input:/in -v $PWD/out_tests:/out pi_madrob_beast run_madrob /in/subject_001_cond_001_run_001_event.csv /in/subject_001_cond_001_run_001_wrench.csv /in/subject_001_cond_001_run_001_jointState.csv /in/condition_1.yaml /out
```

#### Beast

Assuming the tests/beast/input contains the input data, the PI output will be written to out_tests:

```term
docker run --rm -v $PWD/tests/beast/input:/in -v $PWD/out_tests:/out pi_madrob_beast run_beast /in/subject_001_cond_001_run_001_event.csv /in/subject_001_cond_001_run_001_distance.csv /in/subject_001_cond_001_run_001_wrench.csv /in/condition_1.yaml /out
```
TODO: collect beast test data and update the names in this example (if using a different condition)

## Test data

The [tests/madrob/input](tests/madrob/input) directory contains preprocessed `.csv` files and a condition `.yaml` file.
The [tests/madrob/output](tests/madrob/output) directory contains the pi output `.yaml` file.
These files are from a real benchmark run, and can be used to test the `run_pi` command and Docker images.

Beast data is not available yet.
TODO: collect beast test data and update the names in this example (if using a different condition)

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

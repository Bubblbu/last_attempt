# LastAttempt CLI
A simple *Command Line Interface* for Machine Learning with OpenBCI Hardware.

Created by Team E.T. (Erasmus Terrestrials) during the [Brain & Vision Hack 2016](https://abc-accelerator.com/budapest-hackathon/)

## Installation

+ Setup [OpenBCI](http://docs.openbci.com/tutorials/01-GettingStarted)
+ `pip install -r requirements`
+ `pip install -e .[test]`
+ *Important!* Create a local folder for training data, models and settings. Create an ENV_VAR and point it towards this folder

## Configuration

Have a look at `config.ini` in `last_attempt-cli/last_attempt` in order to get an idea of the current available settings.

+ Set n_channels
+ Set n_motions

### Hardware - OpenBCI

Channels are put into correct mode automatically (measuring voltages between NP of each channel). Also the LSL stream can be simply started with `last_attempt runserver -p [PORT]`

## Getting started

*Note* All commands demanding access to the OpenBCI hardware, require `sudo -E` in order to export the environment variables.

### Create training data

	last_attempt data --outfile <filename> --number-samples <n_samples>

+ Automatic instructions for training data
+ Record data + labels
+ Save training data

### Train your models

	last_attempt model run-tests --infile <filename>
	last_attempt model train --infile <filename> --clf <type>

+ Preprocessing
+ Feature Extraction
+ Compare multiple scores
+ Save a model

### Evaluation

	last_attempt model --run <model>

+ Load model
+ Plot classification
+ Flappy bird???

### Utility functions

	last_attempt listfiles

+ Browse training data and trained models

## License

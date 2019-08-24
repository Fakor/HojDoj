#!/usr/bin/env bash

HOJDOJ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOJDOJ_HOME=$HOME/.hojdoj_home
VIRTUAL_ENV_HOME=$HOJDOJ_HOME/venv

source $VIRTUAL_ENV_HOME/bin/activate

export TEST_FOLDER=$HOJDOJ_PATH/tests
export PYTHONPATH=$HOJDOJ_PATH/hojdoj:$TEST_FOLDER/resources/helper

cd $TEST_FOLDER

python -m unittest test_suite.py



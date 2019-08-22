#!/usr/bin/env bash

HOJDOJ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOJDOJ_HOME=$HOME/.hojdoj_home
VIRTUAL_ENV_HOME=$HOJDOJ_HOME/venv
TEST_FOLDER=$HOJDOJ_PATH/hojdoj/tests
VIRTUAL_ENV_HOME=$HOJDOJ_HOME/venv

source $VIRTUAL_ENV_HOME/bin/activate

export PYTHONPATH=$HOJDOJ_PATH/hojdoj

cd $TEST_FOLDER

python -m unittest sketch_logic_tests.py



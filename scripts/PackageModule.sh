#!/bin/bash

#This script packages the module to a wheel package.
#The package is renamed by removing the suffixes in filename.

#Package the project
export PYTHONPATH=$(pwd)
python $packagepath bdist_wheel
#!/bin/bash

#This script establishes the environment to compile, run tests and deploy Synapse.

#Install Java
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk

#Install Python Libraries
sudo apt-get install python3-setuptools
pip3 install wheel
export PYTHONPATH=$(pwd)
pip3 install pyspark==3.2.1
pip3 install pytest==7.1.2
pip3 install numpy==1.18.5
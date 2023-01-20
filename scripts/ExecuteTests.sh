#!/bin/bash

#This script executes the tests in the established environment.
#If one of the tests fail it throws a strerror and terminates the DevOps pipeline.

#Execute Tests
export PYTHONPATH=$(pwd)
pytest --capture=tee-sys  $testpath
result=$?

#Evaluate the Test Result
echo "Result code is: $result"
expected_result=0

#If all test have not passed (result!=0), throw a stderror
if [ $result -ne $expected_result ]; then
    echo "[error] Deployment Terminated: Some test(s) failed!";
    exit 1;
fi
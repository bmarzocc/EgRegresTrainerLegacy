#!/bin/bash

cd ../CMSSW_10_6_1/src/
cmsenv
cd ../../EgRegresTrainerLegacy/

export PATH=$PATH:./bin/$SCRAM_ARCH #add the binary location to path
export PYTHONPATH=$PYTHONPATH:python #adds the python sub dir to python path, this may be PYTHONPATH in some systems 
export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:$PWD/include

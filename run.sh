#!/bin/bash

ARG_INSTALL_REQUIREMENTS=false
ARG_PYTHON_3=false

# Run the application
function Install_Requirements() {
    echo "Installing requirements...";
    pip install -r requirements.txt;
    echo "Requirements installed";
}

function RUN_USING_PYTHON3(){
    echo "Running using Python 3...";
    python3 ./Modules/control.py & python3 ./MOdules/viewer.py
}

function NORMAL_RUN(){
    echo "Running using any Python...";
    python ./Modules/control.py & python ./MOdules/viewer.py
}

#
for arg in "$@"; do
  if [[ "$arg" = -i ]] || [[ "$arg" = --install-requirements ]]; then
    ARG_INSTALL_REQUIREMENTS=true
  fi
  if [[ "$arg" = -p3 ]] || [[ "$arg" = --python-3 ]]; then
    ARG_PYTHON_3=true
  fi
done
#

#
if [[ "$ARG_INSTALL_REQUIREMENTS" = true ]]; then
  Install_Requirements
fi
if [[ "$ARG_PYTHON_3" = true ]]; then
  RUN_USING_PYTHON3
fi
if [[ "$ARG_PYTHON_3" = false ]]; then
  NORMAL_RUN
fi
#


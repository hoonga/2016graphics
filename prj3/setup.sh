#! /bin/bash

# Set prj to virtualenv
virtualenv spline

# Need to install virtualenv
if [ $? -ne 0 ]; then
    echo "need virtualenv"
    # Installing virtualenv
    pip install virtualenv
    virtualenv spline
fi

source ./spline/bin/activate
pip install -r requirements

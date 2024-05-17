#!/bin/sh
docker run --rm -it -v "$(pwd):/work" -w "/work" python:3.9 python3 setup.py build sdist

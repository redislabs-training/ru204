#!/bin/bash

find . -name __pycache__ | xargs rm -rf
find . -name *.pyc | xargs rm -rf
zip -x *.pyc -r ru101.zip redisu

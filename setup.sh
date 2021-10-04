#!/bin/bash
python setup.py install
python setup.py build_ext --inplace
python -m spacy download en_core_web_lg

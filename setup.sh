#!/bin/bash
pip install scipy==1.2.1 PyOpenGL==3.1.1a1 numpy==1.16.6 PyYAML==5.2 Pillow==6.2.1 ftputil==3.4 spacy==2.0.18 pygame==1.9.6 xlib==0.21 matplotlib==2.2.5
python setup.py develop
python setup.py build_ext --inplace
python -m spacy download en_core_web_lg

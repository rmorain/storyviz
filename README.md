# Install
After cloning this repo, there are a few packages you will need to install. We recommend setting up an Anaconda environment specifically for MCEdit to run within. To learn how to install Anaconda, look here: [How To Get Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

When creating a new environment for anaconda, make sure to use the python=2.7 parameter. MCEdit and some of the required libraries only run in python 2.7. Here is an example of creating a new anaconda environment:

conda create -n py27 python=2.7

Then activate your anaconda environment, by running: 'source activate [name of environment]'

With your activated anaconda environment install the following packages and files:
```console
pip install scipy==1.2.1 PyOpenGL==3.1.1a1 numpy==1.16.6 PyYAML==5.2 Pillow==6.2.1 ftputil==3.4 spacy==2.0.18 pygame==1.9.6 xlib==0.21 matplotlib==2.2.5
python -m spacy download en_core_web_lg
```
Then you can run MCEdit:
```console
python mcedit.py
```

If you are using linux you may need xclip
```console
sudo apt-get install xclip
```

For information about MCEdit and how to run MCEdit filters, [VISIT THE WIKI PAGE](http://github.com/mcgreentn/MCAI/wiki)

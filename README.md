# Install

```console
git clone --recursively git@github.com:rmorain/storyviz.git
```

Recursively clone the repo. 

After cloning this repo, there are a few packages you will need to install. We recommend setting up an Anaconda environment specifically for MCEdit to run within. To learn how to install Anaconda, look here: [How To Get Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

When creating a new environment for anaconda, make sure to use the python=2.7 parameter. MCEdit and some of the required libraries only run in python 2.7. Here is an example of creating a new anaconda environment:

conda create -n py27 python=2.7

Then activate your anaconda environment, by running: 'source activate [name of environment]'

With your activated anaconda environment install the GDMC and storyviz modules as well as other dependencies by running:
```console
./setup.sh
```
Then you can run MCEdit:
```console
./mcedit.sh
```

If you are using linux you may need xclip
```console
sudo apt-get install xclip
```

For information about MCEdit and how to run MCEdit filters, [VISIT THE WIKI PAGE](http://github.com/mcgreentn/MCAI/wiki)

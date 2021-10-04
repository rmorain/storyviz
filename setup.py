from setuptools import setup
# Setup GDMC and storyviz
setup(
    name="storyviz",
    version="1.0",
    description="Create minecraft settlements using stories",
    author="Robert Morain",
    author_email="robert.morain@gmail.com",
    packages=['storyviz', 'GDMC'],
    install_requires=["scipy==1.2.1",
        "PyOpenGL==3.1.1a1",
        "numpy==1.16.6",
        "PyYAML==5.2",
        "Pillow==8.3.2",
        "ftputil==3.4",
        "spacy==2.0.18",
        "pygame==1.9.6",
        "xlib==0.21",
        "matplotlib==2.2.5",
],
)
# Cythonize GDMC
from Cython.Build import cythonize                                                      

# Output annotated .html                                                                
import Cython.Compiler.Options                                                          
Cython.Compiler.Options.annotate = True                                                 

pymclevel_ext_modules = cythonize("GDMC/pymclevel/_nbt.pyx")                                 

setup(                                                                                  
ext_modules=pymclevel_ext_modules                                                   
)         

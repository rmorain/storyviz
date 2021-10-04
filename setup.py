from setuptools import setup
# Setup GDMC and storyviz
setup(
    name="storyviz",
    version="1.0",
    description="Create minecraft settlements using stories",
    author="Robert Morain",
    author_email="robert.morain@gmail.com",
    packages=['storyviz', 'GDMC'],
    install_requires=[],
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

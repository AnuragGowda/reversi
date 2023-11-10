from setuptools import setup

from Cython.Build import cythonize
import shutil
import os
try:
    os.remove('__init__.py')
except:
    pass

setup(ext_modules=cythonize("board.pyx", compiler_directives={'language_level': "3"}))
#touch file
open('__init__.py', 'a').close()
# copy output to temp folder

import os

# shutil.copyfile('build/lib.macosx-10.9-arm64-pypy310/board.pypy310-pp73-darwin.so', '../cython_output/board.cpython-38-x86_64-linux-gnu.so')

#!/usr/bin/env python

from distutils.core import setup

setup(name='CommonPython',
      version='1.0',
      description='A collection of common python scripts.',
      author='Yaoyu Hu',
      author_email='yyhu_live@outlook.com',
      url='huyaoyu.com',
      packages=['CommonPython', \
            'CommonPython.Filesystem', 'CommonPython.ImageDenoise', 'CommonPython.ImageWrite', \
            'CommonPython.ImageMisc']
     )

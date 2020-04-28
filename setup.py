#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Setup script for the readersender module.

@file           setup.py
@author:        Juuso Korhonen (juusokorhonen on github.com)
@license:       MIT License
"""
import os
import sys
assert sys.version_info.major == 3
import distutils
import setuptools


def get_version(version_file='VERSION'):
	"""Returns the current library version.
	@return str -- Current semantical version.
	"""
	return ".".join([str(int(x)) for x in open(version_file, 'r').readline().strip().split('.')][:3])


def get_short_description(readme_file='README.md'):
	"""Returns the short description of the package.
	@return str -- short description
	"""
	return open(readme_file, 'r').readlines(1000)[2].strip()

def get_long_description(readme_file='README.md'):
	"""Returns the long description of the package.
	@return str -- Long description
	"""
	return "".join(open(readme_file, 'r').readlines()[2:])


distutils.core.setup(
	name="readersender",
	description=get_short_description(),
	long_description=get_long_description(),
	long_description_content_type="text/markdown",
	version=get_version(),
	author="Juuso Korhonen",
	author_email="juusokorhonen on github.com",
	url="https://github.com/juusokorhonen/readersender",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 3 - Alpha",
	],
	python_requires='>=3.0',
	)
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='stmspectra',
    version='0.1',
    author='Dacen Waters',
    maintainer='Dacen Waters',
    maintainer_email='dacen.c.waters@gmail.com',
    description='Spectra plotting tool for STM',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=['numpy', 'matplotlib'],
    url='https://github.com/desanni/stmspectra',
    scripts=['bin/stmpspectra.py', 'bin/plot_spectra.py', 'bin/parameters.py', 'bin/spectra_analysis.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: GNU GPLv3",
        "Operating System :: OS Independent",
    ),
)
    

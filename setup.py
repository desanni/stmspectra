from setuptools import setup

setup(
    name='stmspectra',
    version='0.1',
    author='Dacen Waters',
    maintainer='Dacen Waters',
    maintainer_email='dacen.c.waters@gmail.com',
    description='Spectra plotting tool for STM',
    install_requires=['numpy', 'matplotlib'],
    scripts=['bin/stmpspectra.py', 'bin/plot_spectra.py', 'bin/parameters.py', 'bin/spectra_analysis.py']
)
    

from setuptools import setup
from setuptools import find_packages


setup(
    name='tgen',
    version='0.2.0',
    description='Sequence-to-sequence natural language generator',
    author='Ondrej Dusek',
    author_email='odusek@ufal.mff.cuni.cz',
    url='https://github.com/UFAL-DSG/tgen',
    download_url='https://github.com/UFAL-DSG/tgen.git',
    license='Apache 2.0',
    install_requires=['numpy==1.15.4',
                      'regex==2018.11.22',
                      'tensorflow==1.12.0',
                      'kenlm',
                      'pudb==2018.1',
                      'pytreex==0.1dev',
                      'recordclass==0.9',
                      'rpyc==4.0.2',
                      'ufal.morphodita==1.9.2.1',
                      'unicodecsv==1.0.23'],
    dependency_links=['https://github.com/kpu/kenlm/archive/master.zip#egg=kenlm',
                      'https://github.com/leotilli/pytreex/archive/py36.zip#egg=pytreex-0.1dev'],
    packages=find_packages()
)


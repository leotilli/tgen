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
    install_requires=['regex==2019.02.03',
                      'numpy==1.15.4',
                      'rpyc==4.0.2',
                      'pudb==2018.1',
                      'recordclass==0.9',
                      'tensorflow==1.12.0',
                      'kenlm',
                      'pytreex==0.1dev'],
    dependency_links=['https://github.com/kpu/kenlm/archive/master.zip#egg=kenlm',
                      'https://github.com/leotilli/pytreex/archive/py36.zip#egg=pytreex-0.1dev'],
    packages=find_packages()
)


from setuptools import setup, find_packages

setup(
    name='radares',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Bibliotecas customizadas',
    long_description=open('README.txt').read(),
    install_requires=['pandas', 'numpy'],
    url='https://github.com/EneoBovino/radares',
    author='Eneo Bovino',
    author_email='eneo.bovino@splice.com.br'
)
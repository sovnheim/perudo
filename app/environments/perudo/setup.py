from setuptools import setup, find_packages

setup(
    name='perudo',
    version='0.1.0',
    description='Perudo Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gym>=0.19.0',
        'numpy>=1.19.5',
    ]
)

from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:
    requirements_list=[]
    return requirements_list
    


setup(
    name='sensor',#name that can be used by other to pip install name
    version="0.0.1",
    author="satyajit2164",
    author_email="satyajit2164@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),#["pymongo"]
)
"""A Machine Learning-based Network Security project designed to detect and track phishing activities.

This system analyzes URLs and related metadata to identify malicious patterns using trained ML models.
It helps improve cybersecurity by providing early detection and classification of phishing threats.

Built with scalability and real-time monitoring in mind, the project supports secure digital environments
by reducing risks associated with phishing attacks."""

from setuptools import setup, find_packages
from typing import List

def get_dependencies() -> List[str]:
    """Read dependencies from requirements.txt."""

    requirement_list : List[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            #Read lines from the file
            lines = f.readlines()
            #Strip whitespace and ignore empty lines
            for line in lines:
                requirement = line.strip()
                #Ignore empty lines and -e options
                if requirement and not requirement.startswith('-e'):
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found. No dependencies will be installed.")

    return requirement_list

setup(
    name='network_security_ml',
    version='0.1.0',
    author='Yohan Shanuka',
    description='A Machine Learning-based Network Security project for phishing detection.',
    packages=find_packages(),
    install_requires=get_dependencies()
)

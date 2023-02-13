# PackageStatistics: Prints statistics of the top 10 packages with the most files associated with them

Debian uses *deb packages to deploy and upgrade software. The packages 
are stored in repositories and each repository contains the so-called "Contents
index". The format of that file is well described here
https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices.

PackageStatistics is a python console application. It takes as input the architecture
(amd64, arm64, mips etc.) and downloads the compressed Contents file associated 
with it from a Debian mirror. It then parses the file and outputs the 
statistics of the top 10 packages that have the most files associated with them.

-------------------------------------------
The project requires Python3.10
------------------------------------------

## Installation
Please install Python3.10 before running the application.
PackageStatistics uses poetry as the dependency management system. 
Please install poetry first by running the command below (For Linux or MAC)
```bash
python3.10 -m pip install poetry
```
cd into the project directory
```bash
cd PackageStatistics
```
Run the command below so that poetry can automatically create a virtual environment
and install the project dependencies in the newly created virtual environment
```bash
python3.10 -m poetry install
```
To run the code (while still inside the project folder) use the command below
```bash
python3.10 -m poetry run python  src/package_statistics.py
```
To view 'help' information and the command line options, run the command below 
```bash
python3.10 -m poetry run python  src/package_statistics.py --help
```
The unit tests, formatting checks using black, coding style checks using flake8 etc. can be executed by running tox.
First install tox using the command below
```bash
python3.10 -m pip install tox
```
And then run tox using the command below
```bash
python3.10 -m tox -r
```
# Toy Robot Simulator
As per the requirements sent ... well maybe not exactly


## Quick start
Install python 3.10+ (my tests have been done with 3.13, but 3.10 should suffice, maybe even 3.8)

Create virtual environment by running:
```shell
python -m venv vent
```

Actavate the venv
xNix:
```shell
source venv/venv/activate
```
Windows:
```shell
.\venv\Scripts\activate.bat
```

Install requirements
(In this version there should be none, but it was required for the pyglet variant)
```shell
pip install .
```

Run the sim
```shell
python exec.py
```

To run the tests
```shell
pytest .
```

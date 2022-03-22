# Parking Application for Electric Cars

### How to run:

In api / dependencies.py, change DEBUG_MODE = True

Next, run:
* ```cd src / mocks / chargers && python3 main.py 42``` # the number should be equal to amount of places
* ```python3 main.py```

### How to run tests:

To run tests, you need to have installed Pytest package in your python environment.

Then, run ```cd src / mocks / chargers && python3 main.py 42```, to run a vital mock.

Next, run ```python3 -m Pytest```, preferably in the root directory of the project, but it is not necessary. 

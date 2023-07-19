# Test Framework Comparisons

This project aims to compare and evaluate different testing frameworks for automated testing. It includes
implementations using the following frameworks: unittest, pytest, nose, robot, and doctest. The goal is to assess the
features, capabilities, and ease of use of each framework in order to make informed decisions for testing geospatial
APIs.

### Framework Implementations

The project contains separate directories for each testing framework implementation. The directories are organized as
follows:

- unittest: Contains the test scripts and modules implemented using Python's built-in unittest framework.
- pytest: Includes the test scripts and modules implemented using the pytest framework.
- nose: Consists of the test scripts and modules implemented using the nose testing framework.
- robot: Contains the test scripts implemented using the Robot Framework.
- doctest: Includes the doctest examples embedded within the API documentation.

Each framework implementation is self-contained within its respective directory, allowing for easy navigation and
comparison between the different approaches.

Running the Tests

To execute the tests for each framework, follow the instructions below:

**1. unittest: Navigate to the unittest directory and run the test script using the Python interpreter:**

    $ export PYTHONPATH=unit-test-service

**2. pytest: Navigate to the pytest directory and run the pytest command:**

    $ export PYTHONPATH=unit-test-service
    $ pytest unit-test-service/tests_pytest/conftest.py -vv -o log_cli=true

**3. nose: Navigate to the nose directory and run the nosetests command:**

    $ export PYTHONPATH=unit-test-service
    $ nosetests

**4. robot: Navigate to the robot directory and run the robot command:**

    $ export PYTHONPATH=unit-test-service
    $ robot tests

## Documentation

The project includes documentation for the geospatial API, which also contains the doctests for testing the API
functionalities. To generate and view the documentation, follow these steps:

**deploy docker container testing on localhost**

    $ docker-compose up -d

**deploy docker container production on other service**

    $ docker-compose -f docker-compose.prod.yml up -d

## Contributions

Contributions to this project are welcome! If you find any issues or want to add support for additional testing
frameworks, feel free to open an issue or submit a pull request. Please adhere to the project's coding standards and
guidelines.

## License

This project is licensed under the MIT License. You are free to modify and use the code in accordance with the terms
specified in the license.
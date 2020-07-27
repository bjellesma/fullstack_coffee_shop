# Fullstack Coffee Shop

## Getting Started

### Dependencies

1. Download and install [Python](https://www.python.org/downloads/) if it is not already available on your system
2. `pipenv` is used as the virtual environment of choice for this application and you can install it using `pip install pipenv`
3. Install [NodeJS](https://nodejs.org/en/download/) in order to run the development scripts (nodejs is also planned to be used for the frontend)

### Setup

0. Clone this project to your machine.

1. From the command line, navigate to the root directory, `fullstack_coffee_shop`.

#### Backend

For the next steps, use the backend folder

2. Fill in `.env-sample` file using the following 

```
DATABASE_NAME=name of sqlite database file to us
AUTH0_DOMAIN=the tenant domain for users to login with
ALGORITHM=prefered algorithm to use when encrypting data
API_AUDIENCE=the Identifier for the auth api that you've created
```

**Note**: The data present already is there for Udacity's Fullstack Coffee Shop Project

3. Rename `.env-sample` to `.env` when you've finished editing `.env-sample`
4. Run `pipenv install` to install the virtual environment
    1. This command will also install the backend packages located inside of `pipfile`

5. Navigate to the `/backend` directory on the command line.

6. Run `npm run server` to start the development server.

### Frontend

For the next steps, use the folder `frontend`

1. Run `npm install`
2. Change values in `src/environments/environments.ts` if different from the udacity test
3. Run `npm run start` to start the frontend server on port 4200
3. In a web browser, navigate to `http://localhost:4200`

## Contributing

1. Fork this repository

2. Use the instructions to set up a local development server
    1. Use the api documentation for more information on how to make requests to the endpoints.

3. Once you've made any modifications using the Code Style Guide listed in the next section, run the code through unit tests using `npm run test`.
    1. If you've written any new endpoints, please also write a new unit test for the endpoint.
    2. Please also pay attention to the code coverage as output and ensure that coverage is at least 80%
4. When your code is passing the unit tests, please submit a pull request

## Code Style Guide

This code abides by [PEP8](https://www.python.org/dev/peps/pep-0008/) with the exception of using tabs over any spaces.

## Credits

* Bill Jellesma
* Udacity - Udacity created the idea for the course as a teaching project
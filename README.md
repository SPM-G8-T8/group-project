# group-project

### Testing(FastAPI):
``` bash
    # run tests
    python3 -m pytest 

    # run tests with print statements
    python3 -m pytest -s
```

### Running frontend tests:
``` bash
    # install Cypress
    npm install cypress

    # because of a known bug with Cypress https://github.com/cypress-io/cypress/issues/5895, Cypress cannot connect to localhost backend links, so go to api.js (isr-frontend > src > api > api.js) and change the 1st line to:
    const rootURL = "http://0.0.0.0:8000"

    # run tests
    npx cypress open
```
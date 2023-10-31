# IS212-SBRP

![Linting](https://github.com/SPM-G8-T8/group-project/actions/workflows/pylint.yml/badge.svg)
![Automated Tests](https://github.com/SPM-G8-T8/group-project/actions/workflows/pytest.yml/badge.svg)

### Running Backend:
``` bash
    cd isr-backend 
    
    # preferably install dependecines in a virtual env
    pip install -r requirements.txt

    uvicorn main:app --reload  
```

### Running Frontend:
``` bash
    cd isr-frontend
    
    npm i

    npm run dev
```


### Running backend tests:
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
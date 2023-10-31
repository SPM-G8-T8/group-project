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
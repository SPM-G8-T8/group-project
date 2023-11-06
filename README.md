# IS212-SBRP

![Linting](https://github.com/SPM-G8-T8/group-project/actions/workflows/pylint.yml/badge.svg)
![Automated Tests](https://github.com/SPM-G8-T8/group-project/actions/workflows/pytest.yml/badge.svg)

## User Interface
Link to Figma: https://www.figma.com/file/v9lNqU7fPQiWlpX4tbX8hI/Jobpilot---Job-Portal-Figma-UI-Template-(Community)-(Community)?type=design&node-id=4403-909&mode=design

## Continuous Integration
Merged pull requests and code pushes automatically trigger our CI pipeline which checks code quality and runs our test suite via pytest. Passing/Failing Status is also reflected in the status badges.

## Continuous Deployment
When the backend or frontend folders have a code change from a push or merged pull-request, there is an automatic redeployment to `render.com`. The `main` branch deploys to the staging environment, while the `prod` branch deploys to production.
![Alt text](image.png)

Links to deployed sites:
- [Staging Frontend](https://spm-frontend-staging.onrender.com)
- [Staging Backend](https://spm-backend-staging.onrender.com)
- [Production Frontend](https://spm-backend-tfiy.onrender.com)
- [Production Backend](https://spm-frontend.onrender.com)


## Pre-requisites
### Clone Codebase:
```bash
git clone https://github.com/SPM-G8-T8/group-project.git
```
### Environment Variables:
Create a `.env` file in `isr-backend` folder to put environmental variables such as database connection link etc
```bash
DB_URI=
# AWS Keys for image upload to S3 Bucket
ACCESS_KEY=
SECRET_KEY=
```

## Running application

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
The backend service is running on port `8000`, and the frontend is running on port `3000`.

## Running tests

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

# because of a known bug with Cypress https://github.com/cypress-io/cypress/issues/5895, Cypress cannot connect to localhost backend links, so go to api.js (isr-frontend > src > api > api.js) and change the rootURL to:
const rootURL = "http://0.0.0.0:8000"

# run tests
npx cypress open
```
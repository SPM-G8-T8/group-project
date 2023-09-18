### Setup Virtual Env (MacOS)
``` bash
python3 -m venv env
```
``` bash
source ./env/bin/activate
# use this command whenever you need to activate the virtual env
```
```bash
python3 -m pip install --upgrade pip
```
``` bash
pip install -r requirements.txt
```

### Env
Create a .env file and use the DB_URI from the JIRA ticket.

### Running the App
When already in venv:
``` bash
uvicorn main:app --reload
```
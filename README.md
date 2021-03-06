# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Trello setup

go to https://trello.com/ and create an account if not already have one
collect the "key" and "tokens" from here https://trello.com/app-key
create / choese the board you want to use (must have a "To Do" List as minimum)
run the following "GET" in postman to obtain the Board ID, replacing the relevent {feilds}
https://api.trello.com/1/search?query={Board Name}&modelTypes=boards&key={Trello KEY}&token={Trello TOKEN}&search

Add the following to the .env file replacing the {feild} items with the above you have obtained
# Creds for trello
TRELLO_KEY={Trello KEY}
TRELLO_TOKEN={Trello TOKEN}
TRELLO_BOARD_ID={Trello BOARD ID}

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```
To run Tests
```bash
 * Run 'poetry add pytest --dev'
 * Run 'poetry run pytest'
```
You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## installing and running the app with ansible
login to the Control server
```bash
ssh ec2-user@35.179.21.80
```
Copy the files in the deploy folder to the ~ directory
Then run the following:
```bash
ansible-playbook playbook.yml -i inventory.ini
```
enter the required information for the trello token, key, board ID

Once complete you can go to http://35.179.21.80:5000/ to view the page

Note: this is pulling from Module 3 currently so change the version to master in the playbook.yml after commited to master
Note: to apply to another Server update the Inventory.ini file with its ip




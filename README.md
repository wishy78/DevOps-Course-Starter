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
enter the required information for the Azure connection string, Database name and Collection Name

Once complete you can go to http://35.179.21.80:5000/ to view the page

Note: this is pulling from Module 3 currently so change the version to master in the playbook.yml after commited to master
Note: to apply to another Server update the Inventory.ini file with its ip


# Build Docker Image
Run the following in powershell teminal in VSCODE
```powershell
# For Production
docker build --target production --tag todo-app:prod .
# For Development
docker build --target development --tag todo-app:dev .
```
# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 8181:5000 --env-file .\.env todo-app

# Run Docker Image
Run the following in powershell teminal in VSCODE
```powershell
# for Development
docker run -d -p 8181:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
# For Production
docker run -d -p 8182:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:prod
```
or the following replacing 'Port you want to use' with the required port number (Note: you cant use the same port on the same machine)
```powershell
# for Development
docker run -d -p 'Port you want to use':5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
# For Production
docker run -d -p 'Port you want to use':5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:prod
```

Once complete you can go to http://localhost:5000/ to view the page or http://localhost:'Port you want to use'/  replacing 'Port you want to use' with your defined port number

# to Run with selenium and firefox for end to end tests add the following
```bash
poetry add selenium --dev
```
for testing tests in docker run the following

```powershell
docker build --target test --tag todo-app:test .
docker run --env-file .env.test todo-app:test tests
```
You can Change the tests to tests_e2e to run the end to end tests (e2e tests not setup but basics are there)
for example:
```powershell
docker run todo-app:test tests_e2e
#or 
docker run -e CON_STRING={CON_STRING} -e DB_NAME={DB_NAME} -e COLLECTION_NAME={COLLECTION_NAME} todo-app:test tests_e2e
```
Replacing the {Items} with relevent data

# to Run on azure
Create an account on azure

then run the following which will login and create a webapp (i had to use --use-device-code just follow the on screen instructions)

Note: replace anything sourounded with <> bracket with the relevent info from .env file (and remove the <>)
The top 3 represent:
$RGName = '<Resource Group Name>'
$WebAppName = '<Web App Name>'
$ServicePlanName = '<Service plan Name>'
change as apropiate for your environment

````powershell
az login --use-device-code

$RGName = 'Cohort22_JonLon_ProjectExercise'
$WebAppName = 'Wapp-To-Do-Mod9-JL'
$ServicePlanName = 'ASP-Mod8-JonLon'
$FLASKAPP = '<FLASK_APP>'
$FLASKENV = '<FLASK_ENV>'
$SECRETKEY = '<SECRET_KEY>'
$CON_STRING = 'mongodb://ConnectionString'
$DB_NAME = 'CosmosDBName'
$COLLECTION_NAME = 'CollectionNamet'

az appservice plan create --resource-group $RGName -n $ServicePlanName --sku B1 --is-linux

az webapp create --resource-group $RGName --plan $ServicePlanName --name $WebAppName --deployment-container-image-name wishy78/todo-app:latest

az webapp config appsettings set -g $RGName -n $WebAppName --settings FLASK_APP=$FLASKAPP
az webapp config appsettings set -g $RGName -n $WebAppName --settings FLASK_ENV=$FLASKENV
az webapp config appsettings set -g $RGName -n $WebAppName --settings SECRET_KEY=$SECRETKEY
az webapp config appsettings set -g $RGName -n $WebAppName --settings CON_STRING=$CON_STRING
az webapp config appsettings set -g $RGName -n $WebAppName --settings DB_NAME=$DB_NAME
az webapp config appsettings set -g $RGName -n $WebAppName --settings COLLECTION_NAME=$COLLECTION_NAME
az webapp config appsettings set -g $RGName -n $WebAppName --settings WEBSITES_PORT=5000
az webapp config appsettings set -g $RGName -n $WebAppName --settings DOCKER_REGISTRY_SERVER_URL=https://hub.docker.com/repository/registry-1.docker.io

````

In https://portal.azure.com/ navigate to the newly created web app as defined in $WebAppName
on the left select the "Deployment Center"
in the main blade navigate to the bottom of the page and copy the "Webhook URL"

In github secrets add/update the following with this "Webhook URL":
AZURE_WEBHOOK_URL
Note: you will need a / befor the $ sign before you save it

website will be : https://<WebappName>.azurewebsites.net/
for me that is https://wapp-to-do-mod9-jl.azurewebsites.net/


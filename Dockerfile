# base image
FROM python:slim-buster as base
# update Image
RUN apt-get update
# install poetry
RUN pip install poetry
# copy all except in dockerignore
COPY . .
# install prerequisits
RUN poetry install --no-root --no-dev
#RUN pip install -r requirements.txt
# use port 5000 from container
EXPOSE 5000



# prod image
FROM base as production
# install gunicorn
RUN pip install gunicorn
# Cmd /entrypoint
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]

# dev image
FROM base as development
# install flask
#RUN pip install flask

CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debugger"] 

# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 8181:5000 --env-file .\.env todo-app

# docker build --target development --tag todo-app:dev .
# docker build --target production --tag todo-app:prod .

# docker run -d -p 8181:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
# docker run -d -p 8182:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:prod

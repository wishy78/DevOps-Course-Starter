# base image
FROM python:slim-buster as base
# update Image
RUN apt-get update
# install poetry
# RUN pip3 install -U pip poetry
RUN pip install poetry
#RUN poetry:poetry add requests
#RUN pip3 install poetry
# copy all except in dockerignore
COPY . .

# install prerequisits
RUN poetry install --no-root --only main
#RUN poetry config virtualenvs.create false --local && poetry install
#RUN pip install -r requirements.txt
# use port from container
EXPOSE 5000

# dev image
FROM base as development
# install flask
#RUN pip install flask
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=$PORT", "--debugger"] 

# testing stage
FROM base as test
RUN pip install pytest
#RUN poetry Install
RUN poetry add pytest --group dev
#WORKDIR /tests
ENV GECKODRIVER_VER v0.31.0
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz
RUN  pip install selenium   
ENTRYPOINT ["poetry", "run", "pytest"]

# prod image
FROM base as production
# install gunicorn
RUN pip install gunicorn
# Cmd /entrypoint
CMD ["gunicorn"  , "-b", "0.0.0.0:$PORT", "todo_app.app:create_app()"]
#CMD ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "--bind 0.0.0.0:$PORT"]
#ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "--bind 0.0.0.0:$PORT"]
#CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT


# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 8181:5000 --env-file .\.env todo-app

# docker build --target development --tag todo-app:dev .
# docker build --target production --tag todo-app:prod .
# docker build --target test --tag todo-app:test .

# docker run -d -p 8181:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
# docker run -d -p 8182:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:prod
# docker run -d -p 8183:5000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:test
# docker run --env-file .env.test todo-app:test tests
# docker run todo-app:test tests_e2e


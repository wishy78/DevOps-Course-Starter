FROM python:slim-buster
RUN apt-get update
# Install poetry:
RUN pip install poetry
#RUN pip install flask
RUN pip install gunicorn
# Copy in the config files:
COPY pyproject.toml poetry.lock ./
# Install only dependencies:
RUN poetry install --no-root --no-dev
# Copy in everything else and install:
COPY . .
RUN pip install -r requirements.txt
# Flask server configuration.
ARG FLASK_APP=todo_app/app
ARG FLASK_ENV=production
# Change the following values for local development.
ENV SECRET_KEY=secret-key
# Creds for trello
ENV TRELLO_KEY=??????????????????????????
ENV TRELLO_TOKEN=??????????????????????????
ENV TRELLO_BOARD_ID=??????????????????????????
# Run CMD instead of Entrypoint
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]
EXPOSE 5000

# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 5000:5000 todo-app
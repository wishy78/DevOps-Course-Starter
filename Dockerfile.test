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
ENV TRELLO_KEY=2e229db46c431176d76792468e753e07
ENV TRELLO_TOKEN=7744cff66a5d6c0218ca12bd61403bc8c03b923a98ed463d4e790b03469029ab
ENV TRELLO_BOARD_ID=625ea5bf47562a0ccd50cb39
# Run CMD instead of Entrypoint
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]
EXPOSE 5000

# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 5000:5000 todo-app
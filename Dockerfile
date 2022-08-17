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
# Run CMD instead of Entrypoint
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]
EXPOSE 5000

# docker build -f .\Dockerfile --tag todo-app .
# docker run -p 8181:5000 --env-file .\.env todo-app
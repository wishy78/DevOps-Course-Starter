# base image
FROM python:slim-buster as base
# update Image
RUN apt-get update
# install poetry
RUN pip install poetry
# copy all except in dockerignore
COPY . .
# install prerequisits
RUN poetry config virtualenvs.create false --local && poetry install
# use port from container
EXPOSE 5000

# development - image
FROM base as development
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debugger"] 

# testing Image
FROM base as test
#RUN poetry Install
RUN poetry add pytest --dev
ENV GECKODRIVER_VER v0.31.0
# Cmd /entrypoint
ENTRYPOINT ["poetry", "run", "pytest"]

# production image
FROM base as production
# install gunicorn
RUN pip install gunicorn
#this is a default port that can be overidden
ENV PORT=5000
# Cmd /entrypoint
CMD gunicorn -b 0.0.0.0:$PORT "todo_app.app:create_app()"

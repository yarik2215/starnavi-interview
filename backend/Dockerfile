FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock /code/
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile

COPY ./backend /code/app
WORKDIR /code/app

# make script executable
RUN chmod +x run_server.sh

# ENTRYPOINT [ "./run.sh" ]
CMD ./run_server.sh
FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV LISTEN_PORT 5000

RUN pip install --no-cache-dir pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN cd /app && pipenv install --system --deploy

COPY . /app

EXPOSE 5000

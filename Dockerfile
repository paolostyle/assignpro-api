FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install --no-cache-dir pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN cd /app && pipenv install --system --deploy

COPY . /app

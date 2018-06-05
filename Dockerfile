FROM python:3.6

# Install required packages
RUN pip install --no-cache-dir pipenv uwsgi

# Install Flask app dependencies
WORKDIR /api
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

# Copy and run the app using WSGI
COPY . .
RUN cd /var/log && mkdir -p uwsgi && touch uwsgi.log
EXPOSE 3031
CMD ["uwsgi", "--ini", "uwsgi.ini"]

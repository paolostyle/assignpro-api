# AssignPro

## About
**AssignPro** is a web application for solving various [assignment problems](https://en.wikipedia.org/wiki/Assignment_problem). This project is part of my BSc thesis at Warsaw University of Technology.

This repo contains backend/API for solving flow networks.

## Technologies
* Flask - web framework (API routes)
* Google ORTools - flow network solver
* NumPy - matrix calculations
* Docker - containerization
* uWSGI - WSGI web server
* nginx - static files server and reverse proxy for uWSGI
* Swagger - API documentation

## Running the app

### Development
Make sure you have installed Python 3.6 and ``pipenv`` (if not, run ``pip install pipenv``).
```
pipenv install
pipenv shell
python main.py
```

### Production
Make sure you have installed Docker.
```
./deploy.sh
```

## Copyright
Paweł Dąbrowski &copy; 2018

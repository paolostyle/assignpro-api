# AssignPro

## About
**AssignPro** is a web application for solving various [assignment problems](https://en.wikipedia.org/wiki/Assignment_problem). This project is part of my BSc thesis at Warsaw University of Technology.

This repo contains backend/API for solving flow networks.

## Technologies
* Flask - web framework (API routes)
* Google ORTools - flow network solver
* NumPy - matrix calculations
* Docker - containerization
* uWSGI + nginx - serving the Python app
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
In real life, it relies on docker-compose and Traefik for load balancing and SSL encryption.
For "fake" production you should just run:
```
docker build -t assignpro-api .
docker run -d -p 5000:5000 --name api assignpro-api
```

## Copyright
Paweł Dąbrowski &copy; 2018-2019

# AssignPro

## About
**AssignPro** is a web application for solving various [assignment problems](https://en.wikipedia.org/wiki/Assignment_problem). This project is part of my BSc thesis at Warsaw University of Technology.

## Technologies
### Front-end (TypeScript 3.2):
* VueJS 2.5 - JavaScript framework
* Bulma with SASS - CSS framework
* Vuex 3 - state management
* Buefy - components library
* Handsontable - data table for forms
* Firebase - history storage and synchronization
* Webpack 4 - bundler
### Back-end (Python 3.6):
* Flask - web framework (API routes)
* Google ORTools - flow network solver
* NumPy - matrix calculations
### Deployment
* Docker - containerization
* uWSGI - WSGI web server
* nginx - static files server and reverse proxy for uWSGI

## Running the app

### Development
Make sure you have installed Python 3.6, Node 8.9 or higher and ``pipenv`` (if not, run ``pip install pipenv``).
```
cd api
pipenv install
pipenv shell
python app.py
```
```
cd webapp
npm install
npm run dev
```

### Production
Make sure you have installed Docker and Docker Compose.
```
docker-compose up --build
```

## Copyright
Paweł Dąbrowski &copy; 2018

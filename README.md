# RelFinder frontend

This repository contains the frontend for RelFinder, developed as a `VueJS` app.

### Development setup

To run the app for development first install the required libraries by running `npm install` and then run the app with `npm run serve`

### Production setup

The production app is deployed via docker. To build the docker image execute

```sh
docker build . -t relfinder-frontend:0.0.1
```

To run the container execute

```sh
docker run --rm -p 80:80 relfinder-frontend:0.0.1
```

### Todos

* [x] Add class legend (for node colors)
* [x] Dockerize app
# RelFinder frontend

This repository contains the frontend for RelFinder, developed as a `VueJS` app. The backend for Relfinder can be found here: http://github.com/nwa-catch-me-if-you-can-project/relfinder-api

### Development setup

To run the app for development first install the required libraries by running `npm install` and then run the app with `npm run serve`

### Production setup

Before running the app, configure the `.env` file by setting the `VUE_APP_API_ROOT` to the backend URL and the `VUE_APP_API_KEY` to the same value as the backend's `API_KEY`. Once done build the docker with:

```sh
docker build . -t relfinder-frontend:0.0.1
```

To run the container execute

```sh
docker run --rm -p 80:80 relfinder-frontend:0.0.1
```

The app will then be available at [localhost](http://localhost)

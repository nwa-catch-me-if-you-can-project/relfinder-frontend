# RelFinder frontend

This repository contains the frontend for RelFinder, developed as a `VueJS` app.

### Development setup

To run the app for development first install the required libraries by running `npm install` and then run the app with `npm run serve`

### Production setup

Before running the app set the `VUE_APP_API_KEY` variable in the `.env` file. This variable must match the `API_KEY` set for the RelFinder backend. Once done build the docker with:

```sh
docker build . -t relfinder-frontend:0.0.1
```

To run the container execute

```sh
docker run --rm -p 80:80 relfinder-frontend:0.0.1
```

The app will then be available at [localhost](http://localhost)
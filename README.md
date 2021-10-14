# RelFinder frontend

Relfinder is a tool for calculating and visualising paths between entities (nodes) in an RDF Knowledge Graph (or SPARQL endpoint). It is based on the original Relfinder tool developed by Philipp Heim, Steffen Lohmann, Timo Stegemann and others. For more information about the tool and its features, please see: http://www.visualdataweb.org/relfinder.php.

The Relfinder source code in this repository is a `Vue.js` porting of some features of the frontend of the original Relfinder which was developed in Adobe Flash / Flex. We have also developed a backend for this tool here using Python `Flask`: https://github.com/nwa-catch-me-if-you-can-project/relfinder-api

***Note:*** Currently, the Relfinder front-end user interface elements (icons for the nodes in the graph) are customised to represent information about companies, shareholders, mergers, acquisitions and divisions of corporations. This is because it has been developed as part of this project: https://eu-corporate-mobility.org/ However, the application can easily be updated to be customisable to the content of any RDF Knowledge Graph. This feature is planned in the coming months.


### Development setup

To run the app for development first install the required libraries by running `npm install` and then run the app with `npm run serve`

### Production setup

Before running the app, configure the `.env` file by setting the `VUE_APP_API_ROOT` to the URL at which the [backend](https://github.com/nwa-catch-me-if-you-can-project/relfinder-api) is served and the `VUE_APP_API_KEY` to the same value as the backend's `API_KEY`. The variable `VUE_APP_KG_PREFIX` should be set to the main namespace of the entities (nodes) in the RDF graph. Once these variables have been set and configured, build the docker image with:

```sh
docker build . -t relfinder-frontend:0.0.1
```

To run the container, execute

```sh
docker run --rm -p 80:80 relfinder-frontend:0.0.1
```

The app will then be accessible at [localhost](http://localhost)

### License and contributions

The Relfinder front-end is developed and copyrighted by Walter Simoncini and Kody Moodley, and released under a dual license (see LICENSE.md file in this repository).
Contributions and bug reports are helpful and welcome.

# plasticgui

Plasticgui is a template for data-visualization GUI with optional web-server. You can get started quickly with raster-graphics, 3d-graphics, or chart graphics. And an optional web-server is included that provides a ready-to-go user system and file upload/download.

## Quick start

First, download the [package](https://github.com/boscoh/plasticgui/archive/master.zip)

1.  To quickly run PlasticGui in the client/Nodejs-server combo, in the `nodeserver` directory, install the dependencies:

    ```bash
    > npm install
    ```

    Then in the `plasticgui` directory:

    ```bash
    > node gui.js
    ```

2.  Alternatively, for the Python server version, in the `pyserver` directory, install

    ```bash
    > pip install -r requirements.txt
    ```

    Then in the `plasticgui` directory:

    ```bash
    > python gui.py
    ```

This will open the template client that can talk to a local server: fetching text, register/login users, download/upload files.

## Why?

I make a lot of data visualization webapps. Sometimes it's just a static webapp, with which I can just zip and send to users. Other times, I make  desktop web-apps using a local webser. I might occasionally launch a website.

I wrote this template to provide the minimum architecture required to seamlessly cycle through these kinds of situation. There is little setup, with more powerful pieces ready to be swapped in.

## The GUI page

The framework for the data-visualization GUI is as a Single-Page-Application (SPA) in the Vue framework. This means the data-visualization can be split-off as a stand-alone web-page. 

To compile the client into this form, in the `client` directory:

```bash
> npm run build
```

Then open `client/dist/index.html` in the browser

When in development, a SPA can be run as a hot reloaded webpack page, allowing changes in the source-code to be directly injected into your browser. The client is setup with webpack that allows compilation to a static web-page, which can opened from the command-line. Webpack also makes it easy to transpile from ES6, leading to more readable and concise code.

In the `client` directory:

```bash
> npm run dev
```

Then open in the browser: `http://localhost:8080`.

#### Editing the app, the frameworks

For managing complex GUI states, it is imperative to use a framework. [Vue](https://vuejs.org/) was can be progressively built up within the Javascript ecosystem. It also does not require learning another language, such as Typescript for Angular, or JSX for React. 

As GUI elements quickly run into cross-platform difficulties using standard HTML inputs, a Material Design component framework was used, [Vueitfy](https://vuetifyjs.com/en/getting-started/quick-start), which provides well thought out controls that work the same in all browser environments, even touch.

To get started, the first file you will work on will be `client/src/components/Home.vue`. The components in that file are from [vuetify](https://vuetifyjs.com/en/getting-started/quick-start). This is a Google Material Design library written for Vue. From experience, using a slick and comprehensive theme such as Google Material Design will save a lot of time later on. Google Material Design has many well-designed components readily, which are web-responsive and works well with desktop and mobile.

#### Chart-widget

To help things along, I've included two wrappers, `chart-widget` and `canvas-widget`. These are convenient classes that simplify the API to `chart.js` for interactive charts, and to the HTML `canvas` element for raster graphics.

#### Canvas-widget

#### Webgl-widget

## Optional Webserver

Of course, you are very likely to want to plug your data visualization to a server, either to serve complex data, talk to files, or to deploy on a external website.

#### Talking between client and server

There are quite a few different ways of communicating to the server, the most popular seems to be Rest, and GraphQL. They each have their advantages. Here I've revived a much older approach, the Remote Procedural Call approach, following the RPC-JSON 2.0 specification.

I've found for data visualization, the data will often need to be massaged and transformed, and will unlikely be stored in a database. This makes it extremely tedious to map to a static REstful interface. Instead, the RPC approach allows the client to call Javascript functions in the server. The downside is if your data starts increasing in complexity then you'll be writing a lot of interfacing Javascript functions. However, that is far off in the future, and now you just want to be prototyping.

To do any kind of communicating, you need matching end-points on the client and the server. The infrastructure allows the `rpc` module in the client builds to call functions directly in the `handler` module in the server. There are four basic ways the client can talk to the server:

- basic functions
- file upload functions
- file download functions
- direct access to files on the server

#### Configuration

A minimally useful set of features has been implemented that links the SPA with the server. These typically have to written together. Given that we have chosen to use an SPA that can be optionally hot re-loaded, we must use CORS. Thus the SPA talks to the browser through `http://localhost:3000`, or this could be set as configuration

#### Database

Sequelize is used to connect to the database. A basic Sqlite3 is the default installation where the location of the file is specified in the `nodeserver/config.js` file. By changing the `config.js`, different databases can be used by Sequelize. This is used to store Users and other data, such as tasks status, messages to the user etc.

#### File System

- basic functions
- file upload functions
- file download functions
- direct access to files on the server

#### User system

You can access the client at `http://localhost:8080`. As you change the source code, the client will hot-reload! If the server is running, CORS has been enabled to allow the client at port 8080 to talk to the server at port 3000.

If your webapp starts getting traction, you'll probably have to implement a user system. There's a lot of things to get right just to get a basic user system up and running, such as sessions, database storage and encryption. So a user system is implemented out of the box.

In the node server, passport manages user sessions, and sequelize is used to manage the database. In the python server, flask-login manages sessions, and sqlalchemy manages the database.

In the client, passwords are hashed and persistent session information is saved in LocalStorage, which is used to retry login on client initialisation. In the database, passwords are salted.

In the client, a register, login and edit-user page is included. The user system can be turned off in the `config.js` file.

As my focus is on data visualisation, I often work with Python codebases. That's why I need a Python server to talk to other Python libraries. However, I also love using a single language from the client and the server (hello Javascript). Why can't I do both? So I've included a choice of two functionally identical servers - `nodeserver` and `pyserver` - to talk to the client.

### Python server

Database is accessed through ORM, and uses only generic fields. An SQLite database is used as it is trivial to setup. Since an ORM is used, it is easy to swap it out for a more powerful database if the need arises.

In Python, the `flask` framework is used. In Node, it's `express`.

  ​

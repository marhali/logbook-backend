# Logbook Backend
This project was created as a part of my final exam as a IT specialist for systems integration (2019).

The goal was to provide an interface for a digital logbook system based on an [RESTful-API](https://de.wikipedia.org/wiki/Representational_State_Transfer). The api is entirely written with [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) using the [Flask framework](https://www.palletsprojects.com/p/flask/) and [SQLAlchemy](https://www.sqlalchemy.org/) as the [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping).

Note: This project has no frontend web interface - it only provides the backend system.

# Features
- RESTful-API easy access
- User authentication and authorization
- User and car management
- Ability to group cars into pools
- Store bills and driving routes

# Requirements
Installed version of [Python](https://www.python.org/), [Flask](https://www.palletsprojects.com/p/flask/) and [SQLAlchemy](https://www.sqlalchemy.org/). A suitable database e.g. [MySQL](https://www.mysql.com/de/) with a dedicated database and user access.

# Installation
The database can be configured using the attached [db-setup](./db-setup.sql) script. This script adds every required table and configures relational mappings. An overview of the database can be found [here](./db-model.png).

Configure the database connection settings inside [/config.py](./config.py):
```bash
# Database settings
# MySQL-URI: mysql://username:password@host/database
SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<host>/<database>'
```

To run the application simply call this inside the application root:
```bash
$ flask run
```
The API should be up running now - you can test if everything works by using an http client and call:
```bash
$ curl -u <username>:<password> -X GET <host-address>/<endpoint>
```

# API Endpoints
![API Endpoints](./endpoints.png "API Endpoints")

# Usage
To use the REST-API simply call the endpoints which can be found above. All endoints are secured by using [Basic Auth](https://en.wikipedia.org/wiki/Basic_access_authentication).  Make sure that every request to the API contains the authentication header.

## License
[MIT](./LICENSE.md)
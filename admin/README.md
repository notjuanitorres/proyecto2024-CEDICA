# CEDICA's Administration

## Table of Contents

- [CEDICA's Administration](#cecidas-administration)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Built Using ](#built-using-)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
  - [Running the tests ](#running-the-tests-)
    - [Break down](#break-down)
    - [And coding style tests](#and-coding-style-tests)
  - [Usage ](#usage-)

## About <a name = "about"></a>
This private application is a web-based tool developed using Flask and Python, designed to facilitate the management of administrative functions at CEDICA's organization, as handling large amounts of documents of several areas with user authentication and role-based permissions. This application serves as the backbone of the system, enabling administrators and authorized users to efficiently manage and operate the various components of the platform.

## Built Using <a name = "built_using"></a>

- [Poetry](https://python-poetry.org/) - Package and dependency management
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - Python Server Framework
  - [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - Templating Engine
- [PostgreSQL](https://www.postgresql.org/) - Database Management System 
- - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [MiniIO](https://github.com/minio/minio) - Object Storage Server (S3)

### Prerequisites

You will need Python install
```
- Python 3.12.3
- Poetry >= 1.8.3
- PostgreSQL >= 16
```

### Installing

After cloning the repository on your local machine, enter on this project
```
$ cd admin/
```


To install the project and all its dependencies, use Poetry:
```
$ poetry install
```


Create a .env file in the project's root folder by copying the .env.dist file and filling in the necessary values
```
cp .env.dist .env
```

Install postgres with:
- port: '5432' 
- host: 'localhost'

Make sure the .env variables are the same as the ones in the postgres configuration file

Now you can run the project with:

```
$ poetry run flask run --app app --debug
```


Alternatively, you can create a Poetry shell and then run the project:
```
$ poetry shell
$ flask run --app app --debug
```


Now you should see a development server starting
## Running the tests <a name = "tests"></a>

### Break down

Once the project is installed and running, you can run the unit tests with:
```
$ poetry run pytest 
```

### And coding style tests
Nothing to see here, yet...
```
Coming soon
```


## Usage <a name = "usage"></a>

Add notes about how to use the system.

<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Grupo 19</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Gitlab](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2024/proyectos/grupo19/code/-/issues)
[![Gitlab Merge Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2024/proyectos/grupo19/code/-/merge_requests)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center">A little description about the project
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🔧 Running the tests ](#-running-the-tests-)
  - [Break down](#break-down)
  - [And coding style tests](#and-coding-style-tests)
- [🎈 Usage ](#-usage-)
- [🚀 Deployment ](#-deployment-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Authors ](#️-authors-)
- [🎉 Acknowledgements ](#-acknowledgements-)

## 🧐 About <a name = "about"></a>

Write about 1-2 paragraphs describing the purpose of your project.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

You will need Python install
```
- Python 3.12.3
- Poetry >= 1.8.3
```

### Installing

Clone the project locally trough SSH.

```
$ git@gitlab.catedras.linti.unlp.edu.ar:proyecto2024/proyectos/grupo19/code.git

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
## 🔧 Running the tests <a name = "tests"></a>

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

## 🎈 Usage <a name="usage"></a>

Nothing here, yet...

## 🚀 Deployment <a name = "deployment"></a>

You should use a Merge Request from development to main in order to trigger the deployment pipeline.

## ⛏️ Built Using <a name = "built_using"></a>

- [Poetry](https://python-poetry.org/) - Package and dependency management
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - Server Framework
- [PostgreSQL](https://www.postgresql.org/) - DBMS  \
- - [pgAdmin]( https://www.pgadmin.org/) - DB Administration User Interface 
- - [SQLAlchemy](SQLAlchemy) - ORM

## ✍️ Authors <a name = "authors"></a>

- [@torresjuanilp ](https://gitlab.catedras.linti.unlp.edu.ar/torresjuanilp)
- [@eduardokusznieryk ](https://gitlab.catedras.linti.unlp.edu.ar/eduardokusznieryk )
- [@gomezcarriquematias ](https://gitlab.catedras.linti.unlp.edu.ar/gomezcarriquematias)
- [@nikiforovdaniel ](https://gitlab.catedras.linti.unlp.edu.ar/nikiforovdaniel)

See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Catedra Proyecto de Software 2024 - Universidad Nacional de La Plata
- [Facundo Diaz]("")
# Web Scraping
- Herramienta de minado para generar una BBDD de contactos comerciales.
- *Mining tool to generate a database of commercial contacts.*

## Description

- El proyecto se concibió inicialmente como una práctica en el uso de Beautiful Soup.
- Utilizando esta biblioteca, se ha desarrollado una herramienta para recopilar la información disponible de todas las empresas registradas en España a partir de un directorio web.

-   *The project was initially conceived as a practice in the use of Beautiful Soup.*
-   *Using this library, a tool has been developed to gather available information from all registered companies in Spain from a web directory.*

## Contents
-  [Installation](#installation)
-  [Files](#files)
-  [Usage](#usage)
-  [License](#license)
- [Badges](#badges)

## Installation

Para instalar las dependencias necesarias para ejecutar este proyecto, se recomienda utilizar un entorno virtual e instalar los paquetes con el siguiente comando:

*To install the necessary dependencies to run this project, it is recommended to use a virtual environment and install the packages with the following command:*

```pip install -r requirements.txt```

## Usage

1. Ejecuta [1-Listados](1-Listados.ipynb).  Generará los listados provinciales en ```src\data\0_Provincias```
*Execute [1-Listados](1-Listados.ipynb).  It will generate the provincial lists in  ```src\data\0_Provincias```*

1. Ejecuta [2-Mining](2-Mining.ipynb).  Generará los directorios de empresas por provincia en ```src\data\1_Directorios```
*Execute [2-Mining](2-Mining.ipynb).  It will generate the company directories by province in ```src\data\1_Directorios```*




## Files

### Notebooks:

1. [Listados](1-Listados.ipynb): Genera los listados de municipios por provincia. / *Generates lists of municipalities by province.*
2. [Mining](2-Mining.ipynb): Extrae los datos de empresas. / *Extracts data of companies.*

### Script:

- AxesorMining: Clase donde recopilamos los distintos métodos que usa la herramienta. / *Class where we compile the different methods used by the tool.*

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.



## Badges
[![wakatime](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f.svg?style=for-the-badge)](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f)
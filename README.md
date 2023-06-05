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
- [Getting started](#getting-started)
-  [License](#license)
- [Badges](#badges)


## Files

### Notebooks:

1. [Listados](1-Listados.ipynb): Genera los listados de municipios por provincia. / *Generates lists of municipalities by province.*
2. [Mining](2-Mining.ipynb): Extrae los datos de empresas. / *Extracts data of companies.*

### Script:

- AxesorMining: Clase donde recopilamos los distintos métodos que usa la herramienta. / *Class where we compile the different methods used by the tool.*

## Getting started

Este proyecto te permite extraer información de las empresas registradas en España a partir de un directorio web. Para empezar, sigue estos pasos:

- Clona este repositorio en tu máquina local.
- Crea un entorno virtual e instala las dependencias con `pip install -r requirements.txt`.
- Ejecuta el notebook `1-Listados.ipynb` para generar los listados de municipios por provincia en la carpeta `src\data\0_Provincias`.
- Ejecuta el notebook `2-Mining.ipynb` para generar los directorios de empresas por provincia en la carpeta `src\data\1_Directorios`.
- Explora los datos obtenidos y disfruta.

This project allows you to extract information from the companies registered in Spain from a web directory. To get started, follow these steps:

- Clone this repository on your local machine.
- Create a virtual environment and install the dependencies with `pip install -r requirements.txt`.
- Run the notebook `1-Listados.ipynb` to generate the lists of municipalities by province in the folder `src\data\0_Provincias`.
- Run the notebook `2-Mining.ipynb` to generate the directories of companies by province in the folder `src\data\1_Directorios`.
- Explore the data obtained and enjoy.
## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.



## Badges
[![wakatime](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f.svg?style=for-the-badge)](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f)
# Web Scraping

Herramienta de webscrapping para obtener información comercial.

### Checkea los stats:

[![wakatime](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f.svg?style=for-the-badge)](https://wakatime.com/badge/user/b1ab7341-4bc0-42d2-b23e-64c7e9be3d50/project/039a28fe-172d-468d-b8ad-fd4c64db1b2f)

### Ideas generales:

- Recorro la carpeta de provincias.
- Dentro de cada archivo, recorro los municipios.
- Dentro de cada municipio, **empieza la fiesta**:

  - En el municipio aparece un listado paginado que parte de 1. En el directorio que generemos insertaremos el número de página para retomar el minado en caso de parada.

  - En el caso de que solo exista una página, hay que puentear la iteración.

  - El bucle debe completar todas las empresas de la página antes de pasar a la siguiente.
    Debemos leer el total de páginas para saber cuando parar.

  - Una vez dentro de la página de la empresa, extraemos todos los datos. Cabe la posibilidad de que la empresa esté extinta, por lo que validamos para pasar de largo de ese registro.

### Notebooks:
1. Listados: Genera los listados de municipios por provincia.
1. Mining: Extrae los directorios de empresas.

### Recursos:
- AxesorMining: Clase donde recopilamos los distintos métodos que usa el minado.



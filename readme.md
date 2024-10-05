# Proyecto FastAPI para la Gestión de Pokémon

## Descripción del Proyecto
Este proyecto implementa un servicio web RESTful usando **FastAPI** para la gestión de Pokémon. Incluye tres endpoints principales: uno para obtener una lista general de Pokémon, otro para detalles específicos de un Pokémon, y un tercero para actualizar información de un Pokémon. El almacenamiento de los datos está hecho con **SQLite**.

## Requisitos Previos
Para poder ejecutar este proyecto necesitas **Python 3.11**. Asegúrate de tener esta versión instalada para garantizar la compatibilidad con las dependencias y características utilizadas en el código. Las dependencias están especificadas en el archivo `requirements.txt`.

### ¿Por qué Python 3.11?
Python 3.11 es la versión más reciente y trae mejoras significativas en términos de rendimiento y nuevas características que hacen el código más eficiente y seguro. Se recomienda usar esta versión para aprovechar estos beneficios en el proyecto.

## Instalación

### 1. Iniciar proyecto
Primero, clona el repositorio en tu máquina local con los siguientes comandos:

```bash
git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto


# Crear el entorno virtual
python3.11 -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate

# En MacOS/Linux
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

### 2. Probar api
Al ejecutar el proyecto podras encontrar la siguiente documentacion open api en la siguiente url

[http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/ "Documentacion")

- GET /pokemon/specific/?data_to_search=<nombre_o_numero_pokedex>
- GET /pokemon/general/?data_to_search=<nombre_o_numero_pokedex>
- PUT /pokemon/{pokedex_number}

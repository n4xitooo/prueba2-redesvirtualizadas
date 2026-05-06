# Sistema de Scouting - Football Manager

Aplicacion de consola en Python para consultar TheSportsDB y generar un informe tecnico de un futbolista. El proyecto integra consumo de API externa, variables de entorno, Docker, GitHub y una propuesta de automatizacion con Jenkins.

## Stakeholder

El stakeholder es un analista de scouting de un club de futbol que necesita revisar rapidamente datos publicos de jugadores antes de una reunion tecnica o una comparacion preliminar de candidatos.

## Problema y solucion

El analista pierde tiempo buscando datos basicos de un jugador en distintas paginas. Esta herramienta centraliza la consulta en una ejecucion puntual, obtiene datos reales desde TheSportsDB y entrega por consola campos utiles como equipo actual, seleccion, posicion, nacionalidad, edad, altura, peso, pie dominante, salario y costo de fichaje cuando la API los informa.

## Variables de entorno

La aplicacion no contiene credenciales hardcodeadas. Antes de ejecutar, configure:

```bash
export THESPORTSDB_API_KEY="tu_api_key"
export PLAYER_NAME="Lionel Messi"
```

`PLAYER_NAME` es opcional. Si no se define, se consulta `Lionel Messi`.

## Ejecucion local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Ejecucion con Docker

El script `build.sh` genera el `Dockerfile`, construye la imagen, elimina el contenedor previo si existe, ejecuta la aplicacion y guarda evidencias en `evidencias/docker/output.txt`.

```bash
chmod +x build.sh
export THESPORTSDB_API_KEY="tu_api_key"
export PLAYER_NAME="Lionel Messi"
./build.sh
```

## Manejo de errores

El script maneja los siguientes escenarios:

- API key faltante o invalida.
- Recurso no encontrado, incluyendo error HTTP 404.
- Timeout de la consulta.
- Problemas de conexion o DNS.
- Respuestas HTTP no exitosas.
- JSON invalido.
- Jugador inexistente o no asociado a futbol.

## Jenkins

Se deben crear dos trabajos:

- `BuildAppJob`: trabajo freestyle que clona este repositorio con credenciales seguras y ejecuta `./build.sh`.
- `SamplePipeline`: pipeline con etapas `Preparation` y `Build`, usando el contenido de `evidencias/jenkins/pipeline_script.txt`.

Las capturas obligatorias deben guardarse en `evidencias/jenkins/`:

- `stage_view.png`
- `console_output_build.png`
- `credentials.png`
- `pipeline_script.txt`

## Estructura

```text
.
├── app.py
├── build.sh
├── Dockerfile
├── requirements.txt
├── .gitignore
├── README.md
└── evidencias/
    ├── docker/
    │   ├── bitacora_errores.txt
    │   ├── output.txt
    │   └── screenshot.png
    └── jenkins/
        ├── stage_view.png
        ├── console_output_build.png
        ├── credentials.png
        └── pipeline_script.txt
```

# Aplicación de Notificaciones

### Requisitos para inicializar el proyecto
Se debe tener instalado en su entorno
- Docker
- Docker compose

### Copiar variables de entorno
Desde la terminal, ejecutar el siguiente comando para copiar las variables de entorno
```    
cp env.example .env
```

### Iniciar aplicación con Docker
Para inicializar la aplicación, ejecutar desde consola el siguiente comando
```
docker compose up --build -d
```

### Docs
Si en las variables de entorno tiene "IS_DEBUG" en True, podrá acceder a la documentación 
generada por **Swagger** a través de la siguiente ruta
```
http://localhost:8000/docs#/
```

# Descripción
Para el funcionamiento de la apliación se utilizan los siguientes servicios, enfocados en la implementación
de la arquitectura **CDC (Change Data Capture)**, utilizada para capturar los cambios que se realizan en nuestra base 
de datos en tiempo real, utilizando **Postgres** para la persistencia de datos, utilizando
**Debezium** para la captura de cambios, almacenando éstos últimos en **Kafka** para el consumo en la
aplicación de **FastAPI**, y usando **Zookeeper** y **Schema Registry** para la gestión y 
coordinacion de esquemas.

## Framework
Se utiliza el framework **FastAPI** para el desarrollo, aprovechando el beneficio de las
herramientas de **Python** que permite la integración del resto de herramientas utilizadas
en el proyecto, y mejorando el rendimiento de los procesos por medio del asincronismo.

## Base de datos
### Postgres
Se utiliza el motor de **PostgreSQL** que nos permitirá persistir nuestros datos y manejar
consultas y relaciones. Para la interacción con nuestra base de datos se utiliza la biblioteca
**SQLAlchemy** que brinda su ORM y nos permite utilizar un motor asincrono a través de **asyncio**.

### Debezium
Se utiliza esta plataforma como conector con nuestra base de datos, encargandose de capturar información
de cambios en tiempo real. Una vez que se conecta, hace un snapshot de todos los **schemas**, para luego
capturar cambios "commiteados" a nivel de fila, generando registros de eventos que se enviarán a tópicos
de **Kafka**

### Kafka
Se encarga de producir, distribuir, y transmitir los eventos de nuestra aplicación

### Kafkacat
Es una herramienta de línea de comandos que se utiliza para interactuar con los temas de Kafka. 
En este caso, se utiliza para consumir los eventos de cambio de datos emitidos por Debezium a Kafka.

Descripción

El Telegram News Bot es una aplicación basada en contenedores que permite a los usuarios recibir noticias relevantes directamente en su cuenta de Telegram. Utiliza un bot personalizado que interactúa con una API para extraer noticias y las envía al usuario en tiempo real. El proyecto está diseñado para ser escalable y fácilmente desplegable mediante Amazon ECS con soporte de AWS Fargate.

Características

Enlace directo con Telegram para recibir mensajes.

Consulta automática de noticias desde una fuente de datos confiable.

Diseño escalable y basado en contenedores.

Programación flexible para iniciar y detener el servicio.

Implementado con las mejores prácticas de AWS.

Tecnologías utilizadas

Backend

Lenguaje: Python

Frameworks y librerías:

python-telegram-bot

requests

Infraestructura

Contenerización: Docker

Despliegue: Amazon ECS (Elastic Container Service)

AWS Fargate para tareas serverless

Almacenamiento de configuraciones sensibles: AWS Secrets Manager

Programación de tareas: Amazon EventBridge

Requisitos previos

Credenciales de AWS configuradas en tu sistema local:

aws configure

Docker instalado y configurado.

Una cuenta de Telegram con permisos para crear un bot.

Acceso a Amazon ECS y permisos para gestionar ECR.

Configuración del proyecto

1. Clonar el repositorio

git clone <URL_DEL_REPOSITORIO>
cd noticias-bot

2. Configurar las variables de entorno

Crea un archivo .env con las siguientes variables:

TELEGRAM_TOKEN=<TU_TOKEN_DEL_BOT>
API_NEWS_KEY=<TU_API_KEY_DE_NOTICIAS>

3. Construir la imagen de Docker

docker build -t noticias-bot .

4. Subir la imagen a Amazon ECR

Crear un repositorio en ECR:

aws ecr create-repository --repository-name noticias-bot

Obtener el login para Docker:

aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com

Etiquetar y subir la imagen:

docker tag noticias-bot:latest <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com/noticias-bot:latest
docker push <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com/noticias-bot:latest

Despliegue en Amazon ECS

1. Crear un clúster

aws ecs create-cluster --cluster-name my-cluster

2. Definir una tarea

Configura un archivo task-definition.json:

{
  "family": "noticias-bot-task",
  "containerDefinitions": [
    {
      "name": "noticias-bot",
      "image": "<TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com/noticias-bot:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "environment": [
        { "name": "TELEGRAM_TOKEN", "value": "<TU_TOKEN_DEL_BOT>" },
        { "name": "API_NEWS_KEY", "value": "<TU_API_KEY_DE_NOTICIAS>" }
      ]
    }
  ],
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512"
}

Registrar la definición de tarea:

aws ecs register-task-definition --cli-input-json file://task-definition.json

3. Crear y ejecutar el servicio

aws ecs create-service \
  --cluster my-cluster \
  --service-name noticias-bot-service \
  --task-definition noticias-bot-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SECURITY_GROUP_ID>],assignPublicIp=ENABLED}"

Programación de tareas

Usa Amazon EventBridge para iniciar y detener tareas en intervalos definidos:

Regla para iniciar:

Configura una regla con la expresión cron adecuada.

Regla para detener:

Configura una regla con un target que ejecute StopTask en el clúster.

Monitorización y costos

CloudWatch para revisar logs y métricas.

Asegúrate de detener tareas e instancias cuando no estén en uso para optimizar costos.

Pruebas locales

Para ejecutar el bot localmente:

docker run --env-file .env -p 5000:5000 noticias-bot

Contacto

Autor: Matthieu Navarro ChamuceroEmail: tu-email@ejemplo.com

# Telegram News Bot

El Telegram News Bot es una aplicación basada en contenedores que permite a los usuarios recibir noticias relevantes directamente en su cuenta de Telegram. Utiliza un bot personalizado que interactúa con una API para extraer noticias y las envía al usuario en tiempo real. El proyecto está diseñado para ser escalable y fácilmente desplegable mediante Amazon ECS con soporte de AWS Fargate.

## Características

- **Enlace directo con Telegram**: Recibe mensajes directamente en tu cuenta.
- **Consulta automática de noticias**: Se conecta a una fuente confiable de datos para extraer noticias.
- **Diseño escalable**: Basado en contenedores para facilitar el despliegue.
- **Programación flexible**: Inicia y detiene el servicio según lo necesites.
- **Implementado con las mejores prácticas de AWS**.

## Tecnologías utilizadas

### Backend

- **Lenguaje**: Python
- **Frameworks y librerías**:
  - `python-telegram-bot`
  - `requests`

### Infraestructura

- **Contenerización**: Docker
- **Despliegue**: Amazon ECS (Elastic Container Service)
- **AWS Fargate**: Tareas serverless
- **Almacenamiento de configuraciones sensibles**: AWS Secrets Manager
- **Programación de tareas**: Amazon EventBridge

## Requisitos previos

1. Credenciales de AWS configuradas en tu sistema local:
   ```bash
   aws configure
   Configuración del proyecto
1. Clonar el repositorio
bash
Copiar código
git clone <URL_DEL_REPOSITORIO>
cd noticias-bot
2. Configurar las variables de entorno
Crea un archivo .env con las siguientes variables:

env
Copiar código
TELEGRAM_TOKEN=<TU_TOKEN_DEL_BOT>
API_NEWS_KEY=<TU_API_KEY_DE_NOTICIAS>
3. Construir la imagen de Docker
bash
Copiar código
docker build -t noticias-bot .
4. Subir la imagen a Amazon ECR
Crear un repositorio en ECR:
bash
Copiar código
aws ecr create-repository --repository-name noticias-bot
Obtener el login para Docker:
bash
Copiar código
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com
Etiquetar y subir la imagen:
bash
Copiar código
docker tag noticias-bot:latest <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com/noticias-bot:latest
docker push <TU_ID_CUENTA>.dkr.ecr.<REGION>.amazonaws.com/noticias-bot:latest
Despliegue en Amazon ECS
1. Crear un clúster
bash
Copiar código
aws ecs create-cluster --cluster-name my-cluster
2. Definir una tarea
Crea un archivo task-definition.json con el siguiente contenido:

json
Copiar código
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
bash
Copiar código
aws ecs register-task-definition --cli-input-json file://task-definition.json
3. Crear y ejecutar el servicio
bash
Copiar código
aws ecs create-service \
  --cluster my-cluster \
  --service-name noticias-bot-service \
  --task-definition noticias-bot-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SECURITY_GROUP_ID>],assignPublicIp=ENABLED}"
Programación de tareas
Usa Amazon EventBridge para iniciar y detener tareas en intervalos definidos.

Regla para iniciar
Configura una regla con la expresión cron adecuada.

Regla para detener
Configura una regla con un target que ejecute StopTask en el clúster.

Monitorización y costos
Logs y métricas: Usa CloudWatch para revisar logs y métricas.
Optimización de costos: Detén tareas e instancias cuando no estén en uso.
Pruebas locales
Para ejecutar el bot localmente:

bash
Copiar código
docker run --env-file .env -p 5000:5000 noticias-bot
Contacto
Autor: Matthieu Navarro Chamucero
Email: tu-email@ejemplo.com

#!/usr/bin/env zsh

DOTENV_PATH=./mysite/.env.dev
source ${DOTENV_PATH}

IMAGE=${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REGISTRY_REPO_NAME}/${SERVICE_NAME}
CLOUD_SQL_INSTANCE=${PROJECT_ID}:${REGION}:${CLOUD_SQL_INSTANCE_NAME}

gcloud run deploy $SERVICE_NAME \
    --platform $PLATFORM \
    --region $REGION \
    --image $IMAGE \
    --add-cloudsql-instances $CLOUD_SQL_INSTANCE \
    --allow-unauthenticated

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform $PLATFORM \
    --region $REGION --format "value(status.url)")

gcloud run services update $SERVICE_NAME \
    --platform $PLATFORM \
    --region $REGION \
    --set-env-vars CLOUDRUN_SERVICE_URL=$SERVICE_URL

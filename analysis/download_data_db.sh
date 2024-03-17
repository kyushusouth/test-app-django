#!/usr/bin/env zsh

DOTENV_PATH=../.env.local
source ${DOTENV_PATH}

SERVICE_ACCOUNT_EMAIL_ADDRESS=$(gcloud sql instances describe ${CLOUD_SQL_INSTANCE_NAME} --format="value(serviceAccountEmailAddress)")

gsutil iam ch serviceAccount:${SERVICE_ACCOUNT_EMAIL_ADDRESS}:objectAdmin gs://${GCS_BUCKET_NAME_SQL_EXPORT_DEST}

gcloud sql export sql ${CLOUD_SQL_INSTANCE_NAME} gs://${GCS_BUCKET_NAME_SQL_EXPORT_DEST}/${SAVE_LOCAL_FILENAME} \
    --database=${CLOUD_SQL_DATABASE_NAME} \
    --offload

gcloud storage cp gs://${GCS_BUCKET_NAME_SQL_EXPORT_DEST}/${SAVE_LOCAL_FILENAME} ${SAVE_LOCAL_DIR}

# データベース接続手順
# createdb ${データベース名}
# gzip -dc ${ダウンロードしたダンプファイル} | psql ${データベース名}

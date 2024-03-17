# 主観評価実験アプリ

音声の主観評価実験に用いるwebアプリ。

DjangoとGCPを利用。

参考ページ

- <https://cloud.google.com/python/django/run?hl=ja#setup-sql>


gcloud builds submit --config cloudbuild.yaml
sh cloudrun_deploy.sh
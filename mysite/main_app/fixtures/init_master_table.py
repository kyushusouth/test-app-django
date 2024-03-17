import datetime
import json

from google.cloud import storage
from google.oauth2 import service_account


def main():
    key_path = (
        "/Users/minami/dev/python/test-app-django/django-416415-3d48fa009149.json"
    )
    service_account_info = json.load(open(key_path))
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info
    )
    storage_client = storage.Client(
        credentials=credentials,
        project=credentials.project_id,
    )

    bucket_name = "wav_files_98723487"
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(
        prefix="avhubert_preprocess_fps25_gray/",
    )
    speaker_name_unique = set()
    model_name_unique = set()
    sample_name_unique = set()
    kind_unique = set()
    for blob in blobs:
        if blob.name.endswith(".wav"):
            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(minutes=60),
                method="GET",
            )
            url_split = url.split("/")
            speaker_name = url_split[7]
            model_name = url_split[5]
            sample_name = url_split[8]
            kind = url_split[9].split(".wav")[0]
            speaker_name_unique.add(speaker_name)
            model_name_unique.add(model_name)
            sample_name_unique.add(sample_name)
            kind_unique.add(kind)

    data = []

    for pk, speaker_name in enumerate(speaker_name_unique):
        data.append(
            {
                "model": "main_app.speakernames",
                "pk": pk + 1,
                "fields": {
                    "speaker_name": speaker_name,
                },
            }
        )
    for pk, model_name in enumerate(model_name_unique):
        data.append(
            {
                "model": "main_app.modelnames",
                "pk": pk + 1,
                "fields": {
                    "model_name": model_name,
                },
            }
        )
    for pk, sample_name in enumerate(sample_name_unique):
        data.append(
            {
                "model": "main_app.samplenames",
                "pk": pk + 1,
                "fields": {
                    "sample_name": sample_name,
                },
            }
        )
    for pk, kind in enumerate(kind_unique):
        data.append(
            {
                "model": "main_app.kinds",
                "pk": pk + 1,
                "fields": {
                    "kind": kind,
                },
            }
        )

    with open(f'{__file__.split(".")[0]}.json', "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()

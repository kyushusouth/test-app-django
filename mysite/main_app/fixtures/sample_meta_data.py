import json
import uuid
from pathlib import Path

from google.cloud import storage


def main():
    bucket_name = "test_media_storage"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob_list = bucket.list_blobs()
    for blob in blob_list:
        blob.delete(if_generation_match=blob.generation)

    data_dir = Path("../static/main_app/wav_files")
    data_path_list = list(data_dir.glob("**/*.wav"))
    data_list = []
    for pk, data_path in enumerate(data_path_list):
        data_path_split = data_path.parts
        kind = data_path_split[-1].split(".")[0]
        sample_name = data_path_split[-2]
        speaker_name = data_path_split[-3]
        model_name = data_path_split[-5]
        new_filename = str(uuid.uuid4())
        data_list.append(
            {
                "model": "main_app.samplemetadata",
                "pk": pk + 1,
                "fields": {
                    "file_path": f"{new_filename}.wav",
                    "file_name": new_filename,
                    "speaker_name": speaker_name,
                    "model_name": model_name,
                    "sample_name": sample_name,
                    "kind": kind,
                },
            }
        )
        blob = bucket.blob(f"{new_filename}.wav")
        blob.upload_from_filename(str(data_path))

    with open(f'{__file__.split(".")[0]}.json', "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False)


if __name__ == "__main__":
    main()

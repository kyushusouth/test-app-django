import json
import shutil
import uuid
from pathlib import Path

from google.cloud import storage


def main():
    bucket_name = "test_media_storage"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    data_dir = Path("../static/main_app/wav_files")
    data_path_list = list(data_dir.glob("**/*.wav"))
    data_dir_encrypted = Path("../static/main_app/wav_files_encrypted")
    if data_dir_encrypted.exists():
        shutil.rmtree(str(data_dir_encrypted))
    data_dir_encrypted.mkdir(parents=True, exist_ok=True)

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

        save_path = data_dir_encrypted / f"{new_filename}.wav"
        shutil.copy(str(data_path), str(save_path))

        blob = bucket.blob(f"{new_filename}.wav")
        blob.upload_from_filename(str(data_path))

    with open(f'{__file__.split(".")[0]}.json', "w") as f:
        json.dump(data_list, f)


if __name__ == "__main__":
    main()

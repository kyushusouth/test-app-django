import json


def main():
    data_list = [
        {
            "model": "main_app.sex",
            "pk": 1,
            "fields": {
                "kind": "男性",
            },
        },
        {
            "model": "main_app.sex",
            "pk": 2,
            "fields": {
                "kind": "女性",
            },
        },
        {
            "model": "main_app.sex",
            "pk": 3,
            "fields": {
                "kind": "無回答",
            },
        },
    ]
    
    
    with open(f'{__file__.split(".")[0]}.json', "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False)
    
    
if __name__ == '__main__':
    main()
import json


def main():
    data_list = [
        {
            "model": "main_app.intelligibilityitems",
            "pk": 1,
            "fields": {
                "item": "非常に悪い",
            },
        },
        {
            "model": "main_app.intelligibilityitems",
            "pk": 2,
            "fields": {
                "item": "悪い",
            },
        },
        {
            "model": "main_app.intelligibilityitems",
            "pk": 3,
            "fields": {
                "item": "普通",
            },
        },
        {
            "model": "main_app.intelligibilityitems",
            "pk": 4,
            "fields": {
                "item": "良い",
            },
        },
        {
            "model": "main_app.intelligibilityitems",
            "pk": 5,
            "fields": {
                "item": "非常に良い",
            },
        },
    ]
    
    
    with open(f'{__file__.split(".")[0]}.json', "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False)
    
    
if __name__ == '__main__':
    main()
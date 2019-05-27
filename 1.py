import requests
import json

for i in range(1):
    headers = {
        "Content-type ": "application/json; charset=UTF-8"
    }

    url = "http://127.0.0.1:8000"

    data = {
        "call": "test:Transcoding:transcoding",
        "params": {
        "path": "video",
        "osskey": "pythontest{}".format(i+1)
      }
    }

    data = requests.post(url, headers=headers, data=json.dumps(data))

    print(data.text)
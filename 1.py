import requests
import json

headers = {
    "Content-type ": "application/json; charset=UTF-8"
}

url = "http://127.0.0.1:8000"

data = {
    "call": "test:Transcoding:transcoding",
    "params": {
    "path": "video",
    "osskey": "pythontest{}".format(11)
  }
}

data = requests.post(url, headers=headers, data=json.dumps(data))

print(data.text)
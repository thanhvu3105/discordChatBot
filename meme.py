import requests
import json

import random

def get_meme():
  response = requests.get("http://alpha-meme-maker.herokuapp.com/1")
  json_data = json.loads(response.content)
  meme = json_data["data"][random.randint(1,20)]["image"]
  return meme
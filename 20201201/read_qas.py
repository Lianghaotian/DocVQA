import json

with open('infographicVQA_train_v0.1.json', 'r') as f:
    data = json.load(f)
    print(data)
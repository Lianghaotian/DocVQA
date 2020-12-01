import os
import urllib.request
import json
import tqdm

data_dir = "./infographicVQA_train_0.1/infographicVQA_train_v0.1.json"
img_dir =  "./img"
with open(data_dir,'r') as load_f:
    data_raw = json.load(load_f)

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

urllib.request.install_opener(opener)
url = []
url_complete = []
for i, data in enumerate(data_raw["data"]):
    if not (data["image_url"] in url):
        url.append(data["image_url"])
        try:
            filename = '{}/{}'.format(img_dir, data["image_local_name"])
            if not os.path.isfile(filename):
                urllib.request.urlretrieve(data["image_url"], filename)
            url_complete.append(data["image_url"])
        except:
            continue

url_error = list(set(url).difference(set(url_complete)))
print(len(url_error))


with open('url_error.txt', 'w') as f:
    for i in range(len(url_error)):
        for key, values in url_error[i].items():
            print(key+","+values+"\r")
            f.write(key+","+values+"\r")





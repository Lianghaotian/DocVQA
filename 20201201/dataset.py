import json
import os
from tqdm import tqdm
from PIL import Image

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
def read_qas(img_path):
    qas = []
    with open('infographicVQA_train_v0.1.json', 'r') as f:
        json_data = json.load(f)
        for data in json_data["data"]:
            if data["image_local_name"] == img_path:
                qa = {}
                qa["qid"] = data["questionId"]
                qa["question"] = data["question"]
                qa["answer"] = data["answers"]
                qas.append(qa)
    return qas
def adj_boxes(boxes,img_heigh, img_width):
    img_heigh = img_heigh
    img_width = img_width
    adj_boxes = [(img_width * boxes["BoundingBox"]["Left"]),
                 (img_heigh * boxes["BoundingBox"]["Top"]),
                 (img_width * (boxes["BoundingBox"]["Left"]+
                               boxes["BoundingBox"]["Width"])),
                 (img_heigh * (boxes["BoundingBox"]["Top"]+
                               boxes["BoundingBox"]["Height"])),
                 ]
    return adj_boxes
def read_examples(input_file, is_training, skip_match_answers=True):
    base = './img'
    img_path = []
    examples = []
    for i in findAllFile(base):
        img_path.append(i)

    for img in tqdm(img_path):
        one_img_path = './img/{}'.format(img)
        try:
            fp = open(one_img_path, 'rb')
            img_ = Image.open(fp)
        except:
            os.remove(one_img_path)
            img_path.remove(img)
            print("####################################Delete error image###########################")
            continue
        img_heigh = img_.size[0]
        img_width = img_.size[1]
        fp.close()
        example={}
        example_path = '{}/{}'.format("infographicVQA_train_v0.1_ocr_outputs",
                                      img.split(".")[0]+'.json')
        with open(example_path,'r') as reader:
            input_data = json.load(reader)
            context = []
            boxes = []
            for word in input_data["WORD"]:
                boxes.append(adj_boxes(word["Geometry"],img_heigh,img_width))
                context.append(word["Text"])

            qas = read_qas(img)

        example["qas"] = qas
        example["image_id"] = img
        example["context"] = context
        example["boxes"] = boxes

        examples.append(example)
        print(len(examples))
    return examples


train_path = "./infographicVQA_train_v0.1_ocr_outputs/30002.json"

examples = read_examples(train_path,is_training=True)

print(examples)
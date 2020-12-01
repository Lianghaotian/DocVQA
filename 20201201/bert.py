# -*- encoding: utf-8 -*-
import warnings
import torch.nn as nn
warnings.filterwarnings('ignore')
from transformers import BertModel, BertTokenizer, BertConfig
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
inputs = tokenizer("43.4 billion", return_tensors="pt")
print(inputs["input_ids"])
outputs = model(**inputs)


print(outputs)

class net(nn.module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')

    def forward(self,x):
        x = self.bert(x)

        return x
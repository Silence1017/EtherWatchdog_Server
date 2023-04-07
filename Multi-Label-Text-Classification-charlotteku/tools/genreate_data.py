import json
import random

data_file = "../data/test.txt"
label_file = "../data/label.txt"
threshold = [0.7, 0.2, 0.1]

train_file = "../data/train.json"
validation_file = "../data/val.json"
test_file = "../data/test.json"

d_f = open(data_file, "r", encoding="utf-8")
l_f = open(label_file, "r", encoding="utf-8")

train_f = open(train_file, "w", encoding="utf-8")
validation_f = open(validation_file, "w", encoding="utf-8")
test_f = open(test_file, "w", encoding="utf-8")
index = 0

while True:
    data = d_f.readline()
    label = l_f.readline()
    dic = dict()
    if data and label:
        data_arr = data.strip().split(" ")
        label_arr = label.strip()[1:-1].split(",")
        label_list = []
        for i, l in enumerate(label_arr):
            if l == '1':
                label_list.append(str(i))
        dic["testid"] = str(index)
        dic["features_content"] = data_arr
        dic["labels_index"] = label_list
        dic["labels_num"] = len(label_list)
        json_str = json.dumps(dic)
        random_value = random.random()
        if random_value <= threshold[0]:
            train_f.write(json_str + "\n")
        elif random_value <= threshold[0] + threshold[1]:
            validation_f.write(json_str + "\n")
        else:
            test_f.write(json_str + "\n")
    else:
        break
    index += 1

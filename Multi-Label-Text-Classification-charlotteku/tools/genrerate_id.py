# 数据文件,one-hot生成
train_file = "../data/test.txt"
id_set = set()
with open(train_file, "r", encoding="utf-8") as f:
    while True:
        line = f.readline()
        if line:
            arr = line.strip().split(" ")
            for word in arr:
                id_set.add(word)
        else:
            break

id_file = "../data/id.txt"
with open(id_file, 'w', encoding="utf-8") as f:
    for index, word in enumerate(sorted(list(id_set))):
        f.write(word + "\n")

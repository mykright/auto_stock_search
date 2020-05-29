
with open("/Users/xxxx1/Downloads/仙逆1.txt", "a+", encoding="utf-8") as f1:
    with open("/Users/xxxx1/Downloads/仙逆.txt", "r", encoding="gbk") as f:
        for line in f:
            f1.write(line)
            
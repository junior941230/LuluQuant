with open("backEnd/strategy.py", "r", encoding="utf-8") as f:
    fileContent = f.read()
front = fileContent.split("# insertCode")[0]
back = fileContent.split("# insertCode")[1]
with open("strategy/test.py", "r", encoding="utf-8") as f:
    fileContent = f.read()
all = front + fileContent + back
print(all)

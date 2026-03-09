import os
import textwrap
with open("backEnd/strategy.py", "r", encoding="utf-8") as f:
    fileContent = f.read()
front = fileContent.split("# insertCode")[0]
back = fileContent.split("# insertCode")[1]
with open("strategy/test.py", "r", encoding="utf-8") as f:
    fileContent = f.read()
all = front + fileContent + back
# print(all)





# 呼叫範例：你可以從變數取得檔名
currentFile = "test.py"
finalCode = generateFullCode(currentFile)

if finalCode:
    print(f"已成功載入 {currentFile} 並完成組合")
    print(finalCode)

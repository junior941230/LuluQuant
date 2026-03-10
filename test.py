import os
import textwrap


def generateFullCode(targetFileName):
    templatePath = "backEnd/strategyTemplate.py"
    injectPath = os.path.join("strategy", targetFileName)
    separator = "# insertCode"

    # 1. 讀取模板
    with open(templatePath, "r", encoding="utf-8") as f:
        templateContent = f.read()

    if separator not in templateContent:
        raise ValueError(f"在 {templatePath} 中找不到 {separator}")

    # 偵測標記行的縮排層級（這一步很重要！）
    lines = templateContent.splitlines()
    indent_prefix = ""
    for line in lines:
        if separator in line:
            # 抓取該行在 separator 出現前的空白部分
            indent_prefix = line[:line.find(separator)]
            break

    # 2. 讀取注入內容
    if not os.path.exists(injectPath):
        print(f"錯誤：找不到檔案 {injectPath}")
        return None

    with open(injectPath, "r", encoding="utf-8") as f:
        injectCode = f.read()

    # --- 核心修復步驟 ---
    # A. 先將注入內容裡的 Tab 全部轉為 4 個空格
    injectCode = injectCode.replace("\t", "    ")

    # B. 移除原本可能不對的縮排 (dedent)
    injectCode = textwrap.dedent(injectCode)

    # C. 根據模板標記所在的縮排，重新進行縮排 (使用偵測到的 indent_prefix)
    tabbedCode = textwrap.indent(injectCode, indent_prefix)
    # -------------------

    # 3. 組合
    # 我們用取代的方式，把 "# insertCode" 直接換成處理好的代碼
    fullCode = templateContent.replace(separator, tabbedCode)

    # 4. 寫入檔案
    with open("strategy/run.py", "w", encoding="utf-8") as f:
        f.write(fullCode)

    print("成功生成 run.py，縮排已自動對齊。")


# 呼叫範例：你可以從變數取得檔名
currentFile = "test.py"
finalCode = generateFullCode(currentFile)

if finalCode:
    print(f"已成功載入 {currentFile} 並完成組合")
    print(finalCode)

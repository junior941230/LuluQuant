from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs


class PythonEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. 設定語法高亮 (Lexer)
        lexer = QsciLexerPython(self)
        self.setLexer(lexer)

        # 2. 設定邊欄行號 (Margin)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "000")  # 設定寬度足以容納三位數
        # self.setMarginsBackgroundColor()

        # 3. 設定程式碼摺疊 (Folding)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)

        # 4. 設定自動補全 (Autocompletion)
        self.apis = QsciAPIs(lexer)
        # 加入自定義的提示詞，你也可以從檔案載入
        self.apis.add("print")
        self.apis.add("import")
        self.apis.add("st.title")
        self.apis.add("self.previewLayout")
        self.apis.prepare()

        self.setAutoCompletionThreshold(1)  # 打 1 個字就觸發提示
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)

        # 5. UI 優化
        # self.setCaretForegroundColor(Qt.blue)  # 游標顏色
        self.setUtf8(True)  # 支援中文

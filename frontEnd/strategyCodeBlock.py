from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QFrame


class PythonEditor(QsciScintilla):
    """
    PythonEditor
    一個基於 QsciScintilla 的 Python 程式碼編輯器，具有 VS Code 經典配色主題。
    功能特性：
        - VS Code 風格的語法高亮（關鍵字、註解、字串、數字等）
        - 行號顯示與程式碼摺疊功能
        - 自訂選擇顏色與光標樣式
        - 縮排參考線與制表符設定
        - UTF-8 編碼支持
        - 無邊框設計以提供沈浸式編輯體驗
    配色方案（VS Code Dark Theme）：
        - 背景色：#1E1E1E（深灰）
        - 前景色：#D4D4D4（淺灰）
        - 關鍵字：#569CD6（亮藍）
        - 註解：#6A9955（綠色）
        - 字串：#CE9178（橘紅）
        - 數字：#B5CEA8（淡綠）
        - 函數名：#DCDCAA（淡黃）
    參數：
        parent (QWidget, optional): 父元件。預設為 None
    屬性：
        lexer (QsciLexerPython): Python 語法高亮器
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # 定義 VS Code 經典配色
        colorBackground = QColor("#1E1E1E")
        colorForeground = QColor("#D4D4D4")
        colorKeyword = QColor("#569CD6")    # 亮藍色
        colorComment = QColor("#6A9955")    # 綠色
        colorString = QColor("#CE9178")     # 橘紅
        colorNumber = QColor("#B5CEA8")     # 淡綠
        colorMargin = QColor("#1E1E1E")
        colorLineNumber = QColor("#858585")

        # 1. 語法高亮 (Lexer) 設定
        lexer = QsciLexerPython(self)

        # 核心修復：設定關鍵字與常用樣式的顏色
        lexer.setDefaultFont(QFont("Consolas", 12))
        lexer.setDefaultPaper(colorBackground)
        lexer.setDefaultColor(colorForeground)

        # 設定特定語法樣式 (VS Code Style)
        # for, if, def...
        lexer.setColor(colorKeyword, QsciLexerPython.Keyword)
        lexer.setColor(colorComment, QsciLexerPython.Comment)       # # 註解
        lexer.setColor(colorString, QsciLexerPython.DoubleQuotedString)
        lexer.setColor(colorString, QsciLexerPython.SingleQuotedString)
        lexer.setColor(colorNumber, QsciLexerPython.Number)
        lexer.setColor(QColor("#DCDCAA"), QsciLexerPython.FunctionMethodName)

        self.setLexer(lexer)

        # 2. 邊欄 (Margin) 與行號優化
        # 去除邊界白線：將所有 Margin 背景色同步
        for i in range(5):  # Scintilla 通常有 5 個 margin
            self.setMarginMarkerMask(i, 0)
            self.setMarginWidth(i, 0)

        # 重新設定行號 Margin (Index 0)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsBackgroundColor(colorMargin)
        self.setMarginsForegroundColor(colorLineNumber)
        self.setMarginsFont(QFont("Consolas", 10))

        # 重新設定摺疊 Margin (Index 2)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setFoldMarginColors(colorMargin, colorMargin)  # 移除摺疊區白線

        # 3. 功能行為
        self.setUtf8(True)
        self.setSelectionBackgroundColor(QColor("#264F78"))
        self.setCaretForegroundColor(QColor("#AEAFAD"))  # 光標改為淺灰色
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2A2D2E"))
        self.setIndentationGuides(True)
        self.setIndentationGuidesBackgroundColor(QColor("#404040"))

        # 4. 微調間距 (視覺沈浸感關鍵)
        self.setExtraAscent(4)
        self.setExtraDescent(4)
        self.setTabWidth(4)

        # 5. 移除外框線
        self.setFrameShape(QFrame.Shape.NoFrame)

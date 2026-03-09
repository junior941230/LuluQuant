from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QFrame


class PythonEditor(QsciScintilla):
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

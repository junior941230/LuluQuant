from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QFrame
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs


class PythonEditor(QsciScintilla):
    """
    PythonEditor
    專門用來編寫 Python / Backtrader 策略的編輯器
    功能：
        - VS Code Dark 風格高亮
        - Python 語法高亮
        - Backtrader 常用 API 自動補全
        - 行號、摺疊、自動縮排、括號匹配
        - 當輸入 . 或英文字時可顯示提示
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # =========================
        # 1. VS Code 經典配色
        # =========================
        colorBackground = QColor("#1E1E1E")
        colorForeground = QColor("#D4D4D4")
        colorKeyword = QColor("#569CD6")
        colorComment = QColor("#6A9955")
        colorString = QColor("#CE9178")
        colorNumber = QColor("#B5CEA8")
        colorClassName = QColor("#4EC9B0")
        colorFunctionName = QColor("#DCDCAA")
        colorDecorator = QColor("#C586C0")
        colorOperator = QColor("#D4D4D4")
        colorIdentifier = QColor("#9CDCFE")
        colorMargin = QColor("#1E1E1E")
        colorLineNumber = QColor("#858585")
        colorCaretLine = QColor("#2A2D2E")
        colorSelection = QColor("#264F78")
        colorMatchedBraceBg = QColor("#3C3C3C")
        colorMatchedBraceFg = QColor("#FFD700")

        fontMain = QFont("Consolas", 12)
        fontMargin = QFont("Consolas", 10)

        # =========================
        # 2. Lexer 設定
        # =========================
        self.lexer = QsciLexerPython(self)
        self.lexer.setDefaultFont(fontMain)
        self.lexer.setDefaultPaper(colorBackground)
        self.lexer.setDefaultColor(colorForeground)

        # 所有 style 先套統一字型與背景
        for style in range(128):
            try:
                self.lexer.setFont(fontMain, style)
                self.lexer.setPaper(colorBackground, style)
            except Exception:
                pass

        # Python 語法樣式顏色
        self.lexer.setColor(colorForeground, QsciLexerPython.Default)
        self.lexer.setColor(colorComment, QsciLexerPython.Comment)
        self.lexer.setColor(colorComment, QsciLexerPython.CommentBlock)

        self.lexer.setColor(colorNumber, QsciLexerPython.Number)

        self.lexer.setColor(colorString, QsciLexerPython.DoubleQuotedString)
        self.lexer.setColor(colorString, QsciLexerPython.SingleQuotedString)
        self.lexer.setColor(
            colorString, QsciLexerPython.TripleSingleQuotedString)
        self.lexer.setColor(
            colorString, QsciLexerPython.TripleDoubleQuotedString)
        self.lexer.setColor(colorString, QsciLexerPython.SingleQuotedFString)
        self.lexer.setColor(colorString, QsciLexerPython.DoubleQuotedFString)
        self.lexer.setColor(
            colorString, QsciLexerPython.TripleSingleQuotedFString)
        self.lexer.setColor(
            colorString, QsciLexerPython.TripleDoubleQuotedFString)

        self.lexer.setColor(colorKeyword, QsciLexerPython.Keyword)
        self.lexer.setColor(
            colorKeyword, QsciLexerPython.HighlightedIdentifier)

        self.lexer.setColor(colorClassName, QsciLexerPython.ClassName)
        self.lexer.setColor(colorFunctionName,
                            QsciLexerPython.FunctionMethodName)
        self.lexer.setColor(colorDecorator, QsciLexerPython.Decorator)
        self.lexer.setColor(colorOperator, QsciLexerPython.Operator)
        self.lexer.setColor(colorIdentifier, QsciLexerPython.Identifier)

        self.setLexer(self.lexer)

        # =========================
        # 3. 行號與摺疊
        # =========================
        for i in range(5):
            self.setMarginMarkerMask(i, 0)
            self.setMarginWidth(i, 0)

        # 行號 margin
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginsBackgroundColor(colorMargin)
        self.setMarginsForegroundColor(colorLineNumber)
        self.setMarginsFont(fontMargin)

        # 摺疊 margin
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setFoldMarginColors(colorMargin, colorMargin)

        # =========================
        # 4. 編輯器行為
        # =========================
        self.setUtf8(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(colorMatchedBraceBg)
        self.setMatchedBraceForegroundColor(colorMatchedBraceFg)

        self.setSelectionBackgroundColor(colorSelection)
        self.setSelectionForegroundColor(QColor("#FFFFFF"))

        self.setCaretForegroundColor(QColor("#AEAFAD"))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(colorCaretLine)
        self.setCaretWidth(2)

        self.setIndentationGuides(True)
        self.setIndentationGuidesBackgroundColor(QColor("#404040"))
        self.setIndentationGuidesForegroundColor(QColor("#404040"))

        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationWidth(4)
        self.setBackspaceUnindents(True)
        self.setTabIndents(True)

        self.setExtraAscent(4)
        self.setExtraDescent(4)

        self.setFrameShape(QFrame.Shape.NoFrame)

        # =========================
        # 5. 自動補全 / 提示
        # =========================
        self._init_autocomplete()

    def _init_autocomplete(self):
        """
        建立 Backtrader / Python 常用補全詞庫
        """
        self.api = QsciAPIs(self.lexer)

        # -------------------------
        # Python 常用
        # -------------------------
        python_words = [
            "import", "from", "as", "class", "def", "return", "if", "elif", "else",
            "for", "while", "break", "continue", "try", "except", "finally",
            "with", "pass", "lambda", "yield", "True", "False", "None",
            "print(", "len(", "range(", "enumerate(", "sum(", "min(", "max(",
            "int(", "float(", "str(", "list(", "dict(", "set(", "tuple("
        ]

        # -------------------------
        # Backtrader 常用
        # -------------------------
        bt_words = [
            "import backtrader as bt",
            "bt.Strategy",
            "bt.Cerebro()",
            "bt.feeds.PandasData",
            "bt.feeds.YahooFinanceData",
            "bt.indicators",
            "bt.ind",
            "bt.talib",
            "bt.Order.Market",
            "bt.Order.Limit",
            "bt.Order.Stop",
            "bt.Order.StopLimit",

            "bt.ind.SMA",
            "bt.ind.EMA",
            "bt.ind.RSI",
            "bt.ind.MACD",
            "bt.ind.ATR",
            "bt.ind.BollingerBands",
            "bt.ind.CrossOver",
            "bt.ind.Highest",
            "bt.ind.Lowest",
            "bt.ind.WeightedMovingAverage",

            "params = (('period', 20),)",
            "lines = ('signal',)",

            "def __init__(self):",
            "def next(self):",
            "def notify_order(self, order):",
            "def notify_trade(self, trade):",
            "def stop(self):",
            "def prenext(self):",
            "def nextstart(self):",

            "self.datas[0]",
            "self.data",
            "self.data0",
            "self.data1",
            "self.data.open[0]",
            "self.data.high[0]",
            "self.data.low[0]",
            "self.data.close[0]",
            "self.data.volume[0]",
            "self.data.datetime.date(0)",
            "self.data.datetime.datetime(0)",

            "self.open",
            "self.high",
            "self.low",
            "self.close",
            "self.volume",

            "self.position",
            "self.position.size",
            "self.order",
            "self.buy()",
            "self.sell()",
            "self.close()",
            "self.buy_bracket()",
            "self.cancel(order)",

            "self.broker",
            "self.broker.getcash()",
            "self.broker.getvalue()",
            "self.broker.setcash(100000.0)",
            "self.broker.setcommission(commission=0.001)",

            "self.log(txt)",
            "self.params.period",
            "self.p.period",

            "order.isbuy()",
            "order.issell()",
            "order.executed.price",
            "order.executed.size",
            "order.executed.value",
            "order.executed.comm",
            "order.status",

            "trade.isclosed",
            "trade.pnl",
            "trade.pnlcomm",
        ]

        # -------------------------
        # 策略模板常用片段
        # -------------------------
        snippets = [
            "class MyStrategy(bt.Strategy):",
            "class MyStrategy(bt.Strategy):\n    params = (('period', 20),)\n",
            "def log(self, txt):\n    dt = self.datas[0].datetime.date(0)\n    print(f'{dt} {txt}')\n",
            "def __init__(self):\n    self.dataclose = self.datas[0].close\n    self.order = None\n",
            "def next(self):\n    if self.order:\n        return\n",
            "if not self.position:",
            "else:",
            "if self.position.size > 0:",
            "self.sma = bt.ind.SMA(self.data.close, period=self.p.period)",
            "self.crossover = bt.ind.CrossOver(self.data.close, self.sma)",
            "if self.crossover > 0:\n    self.buy()\n",
            "elif self.crossover < 0:\n    self.close()\n",
        ]

        for word in python_words + bt_words + snippets:
            self.api.add(word)

        self.api.prepare()

        # 啟用自動補全
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1)   # 輸入 1 個字就可提示
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionUseSingle(
            QsciScintilla.AutoCompletionUseSingle.AcusNever)

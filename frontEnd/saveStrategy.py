from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel


class SaveStrategyDialog(QDialog):
    """
    SaveStrategyDialog - 策略名稱儲存對話框
    此對話框用於提示使用者輸入策略名稱，並提供確定和取消按鈕。
    Attributes:
        label (QLabel): 提示標籤，顯示"請輸入策略名稱："
        nameInput (QLineEdit): 文字輸入框，用於接收使用者輸入的策略名稱
        okButton (QPushButton): 確定按鈕，點擊後會執行accept()動作
        cancelButton (QPushButton): 取消按鈕，點擊後會執行reject()動作
    Methods:
        __init__(parent=None):
            初始化對話框，設定父視窗並呼叫setupUi()進行UI設置
        setupUi():
            設置對話框的UI元件，包括：
            - 設定視窗標題為"儲存策略"
            - 設定固定寬度為200像素
            - 建立主佈局並添加提示標籤、文字輸入框
            - 建立按鈕佈局並添加確定和取消按鈕
            - 連接按鈕的clicked訊號到accept和reject槽函數
        getName():
            傳回使用者在nameInput文字框中輸入的策略名稱
            Returns:
                str: 使用者輸入的策略名稱文字
    Usage:
        dialog = SaveStrategyDialog()
        if dialog.exec_() == QDialog.Accepted:
            strategy_name = dialog.getName()
            # 使用輸入的策略名稱進行後續操作
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("儲存策略")
        self.setFixedWidth(200)

        # 主佈局
        layout = QVBoxLayout()

        # 提示標籤與輸入框
        self.label = QLabel("請輸入策略名稱：")
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("")

        layout.addWidget(self.label)
        layout.addWidget(self.nameInput)

        # 按鈕佈局
        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton("確定")
        self.cancelButton = QPushButton("取消")

        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        # 訊號與槽連接
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def getName(self):
        return self.nameInput.text()

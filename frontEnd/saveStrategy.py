from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel


class SaveStrategyDialog(QDialog):
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

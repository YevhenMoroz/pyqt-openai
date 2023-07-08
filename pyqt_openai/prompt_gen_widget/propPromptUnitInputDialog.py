import re

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QFrame, QPushButton, QHBoxLayout, QWidget

from pyqt_openai.pgsql import PGDatabase


class PropPromptUnitInputDialog(QDialog):
    def __init__(self, db: PGDatabase, id, parent=None):
        super().__init__(parent)
        self.__initVal(db, id)
        self.__initUi()

    def __initVal(self, db, id):
        self.__db = db
        self.__id = id

    def __initUi(self):
        self.setWindowTitle('New Prompt')
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.__newName = QLineEdit()
        self.__newName.textChanged.connect(self.__setAccept)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.__okBtn = QPushButton('OK')
        self.__okBtn.clicked.connect(self.accept)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.addWidget(self.__okBtn)
        lay.addWidget(cancelBtn)
        lay.setAlignment(Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        okCancelWidget = QWidget()
        okCancelWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(self.__newName)
        lay.addWidget(sep)
        lay.addWidget(okCancelWidget)

        self.setLayout(lay)

    def getPromptName(self):
        return self.__newName.text()

    def __setAccept(self, text):
        m = text.strip()
        names = [obj[1] for obj in self.__db.selectPropPromptAttribute(self.__id)]
        f = (True if m else False) and text not in names
        self.__okBtn.setEnabled(f)

import json
from translate import translate
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel, QMainWindow, QSizePolicy, \
    QStyle, QHBoxLayout
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QMovie, Qt, QBitmap
import threading


class Window(threading.Thread):
    def __init__(self):
        super().__init__()
        file = QFile("ui/i18n.ui")
        file.open(QFile.ReadOnly)
        file.close()
        self.ui = QUiLoader().load(file)
        self.initLoading()
        self.initEvent()

    def showLoading(self):
        self.ui.loadingPanel.show()

    def hideLoading(self):
        self.ui.loadingPanel.hide()

    def initLoading(self):
        self.ui.loadingPanel = QWidget(self.ui.container)
        self.ui.loadingPanel.setWindowTitle("Loading Widget")
        self.ui.loadingPanel.setGeometry(0, 0, 500, 800)
        self.hideLoading()
        self.ui.loadingLayout = QHBoxLayout(self.ui.loadingPanel)
        # 创建一个标签用于显示加载动画
        self.ui.loadingMovieLabel = QLabel()
        # 创建一个QMovie对象并加载GIF动画
        self.ui.loadingMovie = QMovie("static/images/loading.gif")  # 替换为你的GIF文件路径
        self.ui.loadingMovieLabel.setMovie(self.ui.loadingMovie)
        self.ui.loadingMovieLabel.setScaledContents(True)
        self.ui.loadingMovieLabel.setStyleSheet(
            "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;background:white")
        self.ui.loadingLayout.addWidget(self.ui.loadingMovieLabel)
        self.ui.loadingTextLabel = QLabel("翻译中...")
        self.ui.loadingLayout.addWidget(self.ui.loadingTextLabel)
        self.ui.loadingLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.loadingMovie.start()
        self.ui.loadingPanel.setStyleSheet("background-color:rgba(255,255,255,.7)")

    def initEvent(self):
        self.ui.inputTextEdit.textChanged.connect(self.onInputTextEdit)
        self.ui.outputTextEdit.textChanged.connect(self.onOutputTextEdit)
        self.ui.translateBtn.clicked.connect(self.onTranslateBtnClick)

    def onInputTextEdit(self):
        pass

    def onOutputTextEdit(self):
        pass

    def translateTask(self):
        input_json = json.loads(self.ui.inputTextEdit.toPlainText())
        translate(input_json)
        self.ui.outputTextEdit.setPlainText(json.dumps(input_json, indent=2, ensure_ascii=False))

    def onTranslateBtnClick(self):
        # self.showLoading()
        self.translateTask()
        # self.hideLoading()
        pass


if __name__ == "__main__":
    app = QApplication()
    mainWindow = Window()
    mainWindow.ui.show()
    app.exec()

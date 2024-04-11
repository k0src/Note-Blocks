import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QAction, QCursor, QMouseEvent

class NoteNode(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 120)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gray; border: 2px solid black;")
        self.draggable = False
        self.offset = QPoint()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggable:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = False

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Canvas")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        self.title_label = QLabel("New Canvas")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        self.title_label.setMouseTracking(True)
        self.title_label.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.title_label and event.type() == event.Type.MouseButtonDblClick:
            self.editTitle()
        return super().eventFilter(obj, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        new_note_action = menu.addAction("New Note")
        
        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        
        copy_action = menu.addAction("Copy")
        cut_action = menu.addAction("Cut")
        paste_action = menu.addAction("Paste")

        

        new_note_action.triggered.connect(self.createNewNote)
        copy_action.triggered.connect(self.copyActionTriggered)
        cut_action.triggered.connect(self.cutActionTriggered)
        paste_action.triggered.connect(self.pasteActionTriggered)

        action = menu.exec(self.mapToGlobal(event.pos()))

    def createNewNote(self):
        cursor_pos = QCursor.pos()
        note_node = NoteNode(self)
        note_node.move(cursor_pos)
        note_node.show()

    def copyActionTriggered(self):
        print("Copy")

    def cutActionTriggered(self):
        print("Cut")

    def pasteActionTriggered(self):
        print("Paste")

    def editTitle(self):
        self.title_edit = QLineEdit(self.title_label.text())
        self.title_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_edit.setStyleSheet("font-size: 24px;")
        self.title_edit.returnPressed.connect(self.updateTitle)
        self.layout().replaceWidget(self.title_label, self.title_edit)
        self.title_edit.selectAll()
        self.title_edit.setFocus()

    def updateTitle(self):
        new_title = self.title_edit.text()
        self.layout().replaceWidget(self.title_edit, self.title_label)
        self.title_label.setText(new_title)
        self.title_edit.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
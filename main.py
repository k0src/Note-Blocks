import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QMenu, QDialog, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QCursor, QMouseEvent

class NoteNode(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 120)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #858585; border: 2px solid black;")
        self.draggable = False
        self.offset = QPoint()
        self.text_content = ""

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = False

    def setTextContent(self, text):
        self.text_content = text

class NoteEditWindow(QDialog):
    noteSaved = pyqtSignal(str)

    def __init__(self, text_content="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Note")
        self.setFixedSize(500, 600)
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel("Note:")
        layout.addWidget(self.title_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setText(text_content)
        layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveNote)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def saveNote(self):
        text = self.text_edit.toPlainText()
        self.noteSaved.emit(text)
        self.close()

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
        self.note_nodes = []

    def eventFilter(self, obj, event):
        if obj == self.title_label and event.type() == event.Type.MouseButtonDblClick:
            self.editTitle()
        return super().eventFilter(obj, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        new_note_action = menu.addAction("New Note")
        edit_note_action = menu.addAction("Edit Note")
        rename_note_action = menu.addAction("Rename Note")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        
        copy_action = menu.addAction("Copy")
        cut_action = menu.addAction("Cut")
        paste_action = menu.addAction("Paste")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)

        delete_action = menu.addAction("Delete Note")

        edit_note_action.triggered.connect(self.editNote)
        new_note_action.triggered.connect(self.createNewNote)
        rename_note_action.triggered.connect(self.renameNote)
        copy_action.triggered.connect(self.copyActionTriggered)
        cut_action.triggered.connect(self.cutActionTriggered)
        paste_action.triggered.connect(self.pasteActionTriggered)
        delete_action.triggered.connect(self.deleteActionTriggered)

        action = menu.exec(self.mapToGlobal(event.pos()))

    def editNote(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                edit_window = NoteEditWindow(text_content=note_node.text_content, parent=self)
                edit_window.noteSaved.connect(note_node.setTextContent)
                edit_window.exec()
                break

    def createNewNote(self):
        cursor_pos = QCursor.pos()
        note_node = NoteNode(self)
        note_node.move(cursor_pos)
        self.note_nodes.append(note_node)
        note_node.show()

    def renameNote(self):
        print("Rename Note")

    def copyActionTriggered(self):
        print("Copy")

    def cutActionTriggered(self):
        print("Cut")

    def pasteActionTriggered(self):
        print("Paste")

    def deleteActionTriggered(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                note_node.deleteLater()
                self.note_nodes.remove(note_node)
                break

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
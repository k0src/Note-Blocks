import sys
from PyQt6.QtWidgets import QApplication, QInputDialog, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QMenu, QDialog, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QCursor, QMouseEvent, QPainter

class NoteNode(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 120)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #858585; border: 2px solid black;")
        self.draggable = False
        self.offset = QPoint()
        self.text_content = ""
        self.title = ""

        self.title_label = QLabel(self.title, self)
        self.title_label.setGeometry(0, 0, self.width(), 25)
        self.title_label.setStyleSheet("color: black;")

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

    def setTitle(self, title):
        self.title = title
        self.title_label.setText(title)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawText(10, 20, self.title)

class NoteEditWindow(QDialog):
    noteSaved = pyqtSignal(str)

    def __init__(self, text_content="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Note")
        self.resize(500, 600)
        
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
        self.setWindowTitle("My Web")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        self.title_label = QLabel("My Web")
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
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("New Note")
        input_dialog.setLabelText("Enter Note Name:")
        input_dialog.move(cursor_pos)
        ok = input_dialog.exec()
        if ok:
            title = input_dialog.textValue()
            note_node = NoteNode(self)
            note_node.move(cursor_pos)
            note_node.setTitle(title)
            self.note_nodes.append(note_node)
            note_node.show()

    def renameNote(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Rename Note")
                input_dialog.setLabelText("Enter Note Name:")
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    title = input_dialog.textValue()
                    note_node.setTitle(title)
                break

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
        self.title_edit.setFixedHeight(40)
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
        self.setWindowTitle("Mind Web v0.1")

        file_menu = self.menuBar().addMenu("&File")

        new_action = QAction("&New", self)
        open_action = QAction("&Open", self)
        save_action = QAction("&Save", self)
        save_as_action = QAction("Save &As", self)

        separator = QAction(self)
        separator.setSeparator(True)
        file_menu.addAction(separator)

        exit_action = QAction("&Exit", self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        new_action.triggered.connect(self.newFile)
        open_action.triggered.connect(self.openFile)
        save_action.triggered.connect(self.saveFile)
        save_as_action.triggered.connect(self.saveAsFile)
        exit_action.triggered.connect(self.exitApp)

    def newFile(self):
        print("New")

    def openFile(self):
        print("Open")

    def saveFile(self):
        print("Save")

    def saveAsFile(self):
        print("Save As")

    def exitApp(self):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
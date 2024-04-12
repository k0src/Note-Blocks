import sys
import random
from PyQt6.QtWidgets import (QApplication, QInputDialog, QColorDialog, QMainWindow, 
                             QWidget, QVBoxLayout, QLabel, QLineEdit, QMenu, QDialog, QHBoxLayout, 
                             QTextEdit, QPushButton, QTextBrowser, QFileDialog, 
                             QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QPlainTextEdit)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QRect
from PyQt6.QtGui import QFont, QAction, QCursor, QPainter, QPen, QColor, QPalette, QPixmap, QFontDatabase

# FIX NOTES TOUCHING PROBLEM
# FIX TEXT SIZING PROBLEM

# pin method
# embed code (chnage name to sticky) - 
# embed links
# Embed files
# Save/open

# ADD STICKY CONTEXT MENU delete, opacity, move forward/backward - and raise title

class Sticky(QPlainTextEdit):
    stickies = []
    
    def __init__(self, parent=None, canvas_title_label=None):
        super().__init__(parent)
        self.canvas_title_label = canvas_title_label

        font_id = QFontDatabase.addApplicationFont("fonts/FiraCode-Medium.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(16)
            self.setFont(font)
        else:
            print("Font not found")

        self.setFixedSize(300, 300)
        self.setMinimumSize(300, 300)
        self.setMaximumSize(parent.size())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #8f8f8f; border: 2px solid black; border-color: #212121; color: black;")
        self.draggable = False

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)

        self.setGraphicsEffect(shadow_effect)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


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

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        move_foward = menu.addAction("Move Forward")
        move_backwards = menu.addAction("Move Backwards")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)

        delete_action = menu.addAction("Delete")

        move_foward.triggered.connect(self.moveFoward)
        move_backwards.triggered.connect(self.moveBackwards)
        delete_action.triggered.connect(self.deleteSticky)

        menu.exec(event.globalPos())

    def moveFoward(self):
        for sticky in self.stickies:
            if sticky.underMouse():
                sticky.raise_()
                self.canvas_title_label.raise_() 
                return
    
    def moveBackwards(self):
        for sticky in self.stickies:
            if sticky.underMouse():
                sticky.lower()
                return

    def deleteSticky(self):
        for sticky in self.stickies:
            if sticky.underMouse():
                sticky.deleteLater()
                self.stickies.remove(sticky)
                return

class ImageWidget(QWidget):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.aspect_ratio = pixmap.width() / pixmap.height()

        new_width = pixmap.width() // 2
        new_height = pixmap.height() // 2

        if new_width > 1500 or new_height > 1500:
            new_width //= 4
            new_height //= 4
        elif new_width > 3000 or new_height > 3000:
            new_width //= 8
            new_height //= 8
        elif new_width > 6000 or new_height > 6000:
            new_width //= 16
            new_height //= 16

        self.setFixedSize(new_width, new_height)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("border: 2px solid black; border-color: #212121;")
        self.draggable = False
        self.offset = QPoint()

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)

        self.setGraphicsEffect(shadow_effect)

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

class MovableTextLabel(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.label = QLabel(text, self)
        self.label.setStyleSheet("color: #c7c7c7;")

        font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Medium.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(18)
            self.label.setFont(font)
        else:
            print("Font not found")

        self.draggable = False
        self.offset = QPoint()
        self.label.adjustSize()

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

    def setText(self, text):
        self.label.setText(text)
        self.label.adjustSize()

class Subcanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(225, 225)
        self.setMinimumSize(225, 225)
        self.setMaximumSize(parent.size())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #454852; border: 2px solid black; border-color: #212121;")
        self.resizing = False
        self.resize_offset = QPoint()
        self.draggable = False

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)

        self.setGraphicsEffect(shadow_effect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            resize_handle_rect = QRect(self.width() - 10, self.height() - 10, 10, 10)
            if resize_handle_rect.contains(event.pos()):
                self.resizing = True
                self.resize_offset = event.pos()
            else:
                self.draggable = True
                self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.resizing:
            current_width = self.width()
            current_height = self.height()

            new_width = max(200, current_width + (event.pos().x() - self.resize_offset.x()))
            new_height = max(200, current_height + (event.pos().y() - self.resize_offset.y()))
            
            self.resize(new_width, new_height)
            
            self.resize_offset = event.pos()
            
        elif self.draggable:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.resizing:
                self.resizing = False
            elif self.draggable:
                self.draggable = False

class NoteNode(QWidget):
    titleChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(125, 150)
        self.setMinimumSize(125, 150)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #4e5661; border: 2px solid black; border-color: #212121;")
        self.draggable = False
        self.offset = QPoint()
        self.plain_text_content = ""
        self.markdown_content = ""
        self.title = ""
        self.title_label = QLabel(self.title, self)

        font_id = QFontDatabase.addApplicationFont("fonts/Poppins-ExtraLight.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(12)
            self.title_label.setFont(font)
        else:
            print("Font not found")

        self.title_label.setGeometry(0, 0, self.width(), 25)
        self.title_label.setStyleSheet("color: black;")

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)

        self.setGraphicsEffect(shadow_effect)

        self.line_lengths = []
        for _ in range(7):
            self.line_lengths.append(random.randint(35, 105))

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

    def setTextContent(self, plain_text_content):
        self.plain_text_content = plain_text_content

    def setTitle(self, title):
        self.title = title
        self.title_label.setText(title)
        self.titleChanged.emit(title)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawText(10, 20, self.title)

        pen = QPen(QColor("#212121")) 
        pen.setWidth(2)
        painter.setPen(pen)
        
        line_spacing = 15
        start_x = 10
        start_y = 41
        
        current_y = start_y
        for length in self.line_lengths:
            painter.drawLine(start_x, current_y, start_x + length, current_y)
            current_y += line_spacing

class NoteEditWindow(QDialog):
    noteSaved = pyqtSignal(str)

    def __init__(self, note_node, plain_text_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Note")
        self.resize(500, 600)
        self.note_node = note_node
        self.plain_text_content = plain_text_content
        self.markdown_content = ""
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel("")

        title_font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Light.ttf")

        if title_font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(title_font_id)[0]
            font = QFont(font_family)
            font.setPointSize(12)
            self.title_label.setFont(font)
        else:
            print("Font not found")

        layout.addWidget(self.title_label)

        font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Medium.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(50)
            self.setFont(font)
        else:
            print("Font not found")
        
        self.editor = QTextEdit()
        self.editor.setPlainText(self.plain_text_content)
        layout.addWidget(self.editor)

        self.preview = QTextBrowser()
        self.preview.setMarkdown(self.markdown_content)
        self.preview.hide()
        layout.addWidget(self.preview)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveNote)
        button_layout.addWidget(save_button)

        self.edit_button = QPushButton("Preview")
        self.edit_button.clicked.connect(self.toggleEditPreview)
        button_layout.addWidget(self.edit_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        self.title_label.setText(self.note_node.title)

    def toggleEditPreview(self):
        if self.editor.isVisible():
            self.preview.setMarkdown(self.editor.toPlainText())
            self.editor.hide()
            self.preview.show()
            self.edit_button.setText("Edit")
        else:
            self.preview.hide()
            self.editor.show()
            self.edit_button.setText("Preview")

    def updateTitleLabelText(self, title):
        self.title_label.setText(title)

    def saveNote(self):
        self.plain_text_content = self.editor.toPlainText()
        self.noteSaved.emit(self.plain_text_content)
        self.close()

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Medium.ttf")

        self.setWindowTitle("My Notes")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        self.title_label = QLabel("My Notes")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(22)
            self.title_label.setFont(font)
        else:
            print("Font not found")

        self.setStyleSheet("color: #c7c7c7;")
        layout.addWidget(self.title_label)
        self.title_label.setMouseTracking(True)
        self.title_label.installEventFilter(self)
        self.note_nodes = []
        self.subcanvases = []
        self.text_labels = []
        self.images = []

    def eventFilter(self, obj, event):
        if obj == self.title_label and event.type() == event.Type.MouseButtonDblClick:
            self.editTitle()
        return super().eventFilter(obj, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        new_note_action = menu.addAction("New Note")
        new_text_label_action = menu.addAction("New Text Label")
        new_image_action = menu.addAction("New Image")
        new_subcanvas_action = menu.addAction("New Block")
        new_sticky = menu.addAction("New Sticky")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)

        edit_note_action = menu.addAction("Edit")
        note_color_action = menu.addAction("Change Color")
        rename_note_action = menu.addAction("Rename")
        change_opacity_action = menu.addAction("Change Opacity")
        change_label_font_size = menu.addAction("Change Font Size")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        
        copy_action = menu.addAction("Copy")
        cut_action = menu.addAction("Cut")
        paste_action = menu.addAction("Paste")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)

        bring_to_front_action = menu.addAction("Move Foward")
        send_to_back_action = menu.addAction("Move Backwards")

        separator = QAction(self)
        separator.setSeparator(True)
        menu.addAction(separator)
        delete_action = menu.addAction("Delete")

        new_note_action.triggered.connect(self.createNewNote)
        new_text_label_action.triggered.connect(self.createNewTextLabel)
        new_image_action.triggered.connect(self.createNewImage)
        new_subcanvas_action.triggered.connect(self.createSubcanvas)
        new_sticky.triggered.connect(self.createNewSticky)

        edit_note_action.triggered.connect(self.editNote)
        rename_note_action.triggered.connect(self.renameNote)
        note_color_action.triggered.connect(self.changeNoteColor)
        change_opacity_action.triggered.connect(self.changeOpacity)
        change_label_font_size.triggered.connect(self.changeLabelFontSize)
       
        copy_action.triggered.connect(self.copyActionTriggered)
        cut_action.triggered.connect(self.cutActionTriggered)
        paste_action.triggered.connect(self.pasteActionTriggered)
        delete_action.triggered.connect(self.deleteActionTriggered)

        bring_to_front_action.triggered.connect(self.bringToFront)
        send_to_back_action.triggered.connect(self.sendToBack)

        action = menu.exec(self.mapToGlobal(event.pos()))

    def createNewNote(self):
        cursor_pos = QCursor.pos()
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("New Note")
        input_dialog.setLabelText("Enter Note Name:")
        input_dialog.resize(300, 100)
        input_dialog.move(cursor_pos)
        ok = input_dialog.exec()
        if ok:
            title = input_dialog.textValue()
            note_node = NoteNode(self)
            note_node.move(cursor_pos)
            note_node.setTitle(title)
            self.note_nodes.append(note_node)
            note_node.show()
            self.title_label.raise_()

    def createNewTextLabel(self):
        cursor_pos = QCursor.pos()
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("New Text Label")
        input_dialog.setLabelText("Enter Text:")
        input_dialog.resize(300, 100)
        input_dialog.move(cursor_pos)
        ok = input_dialog.exec()
        if ok:
            text_label = MovableTextLabel(input_dialog.textValue(), self)
            text_label.move(cursor_pos)
            self.text_labels.append(text_label)
            text_label.adjustSize()
            text_label.show()
            self.title_label.raise_()

    def createNewImage(self):
        cursor_pos = QCursor.pos()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            image_widget = ImageWidget(pixmap, self)
            self.images.append(image_widget)
            image_widget.move(cursor_pos)
            image_widget.show()
            self.title_label.raise_()

    def createNewSticky(self):
        cursor_pos = QCursor.pos()
        new_sticky = Sticky(self, canvas_title_label=self.title_label)
        new_sticky.move(cursor_pos)
        Sticky.stickies.append(new_sticky)
        new_sticky.show()
        self.title_label.raise_()

    def editNote(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                edit_window = NoteEditWindow(note_node, plain_text_content=note_node.plain_text_content, parent=self)
                edit_window.noteSaved.connect(note_node.setTextContent)
                edit_window.exec()
                break

    def renameNote(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Rename Note")
                input_dialog.setLabelText("Enter Note Name:")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    title = input_dialog.textValue()
                    note_node.setTitle(title)
                break

        for text_label in self.text_labels:
            if text_label.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Rename Text Label")
                input_dialog.setLabelText("Enter Text:")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    new_text = input_dialog.textValue()
                    text_label.setText(new_text)
                break

    def changeNoteColor(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                current_color = note_node.palette().color(QPalette.ColorRole.Window)
                color = QColorDialog.getColor(current_color, self)
                if color.isValid():
                    note_node.setStyleSheet(f"background-color: {color.name()}; border: 2px solid black; border-color: #212121;")
                    break

        for subcanvas in self.subcanvases:
            if subcanvas.underMouse():
                current_color = subcanvas.palette().color(QPalette.ColorRole.Window)
                color = QColorDialog.getColor(current_color, self)
                if color.isValid():
                    subcanvas.setStyleSheet(f"background-color: {color.name()}; border: 2px solid black; border-color: #212121;")
                    break

        for text_label in self.text_labels:
            if text_label.underMouse():
                current_color = text_label.palette().color(QPalette.ColorRole.Window)
                color = QColorDialog.getColor(current_color, self)
                if color.isValid():
                    text_label.label.setStyleSheet(f"color: {color.name()};")
                    break

    def changeOpacity(self):
        for subcanvas in self.subcanvases:
            if subcanvas.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Change Opacity")
                input_dialog.setLabelText("Opacity (1-100):")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    try:
                        opacity = int(input_dialog.textValue())
                        opacity /= 100
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(opacity)
                        subcanvas.setGraphicsEffect(opacity_effect)
                    except ValueError:
                        break
                    break
                break

        for text_label in self.text_labels:
            if text_label.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Change Opacity")
                input_dialog.setLabelText("Opacity (1-100):")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    try:
                        opacity = int(input_dialog.textValue())
                        opacity /= 100
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(opacity)
                        text_label.setGraphicsEffect(opacity_effect)
                    except ValueError:
                        break
                    break
                break

        for image in self.images:
            if image.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Change Opacity")
                input_dialog.setLabelText("Opacity (1-100):")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    try:
                        opacity = int(input_dialog.textValue())
                        opacity /= 100
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(opacity)
                        image.setGraphicsEffect(opacity_effect)
                    except ValueError:
                        break
                    break
                break
        
        for note_node in self.note_nodes:
            if note_node.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Change Opacity")
                input_dialog.setLabelText("Opacity (1-100):")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    try:
                        opacity = int(input_dialog.textValue())
                        opacity /= 100
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(opacity)
                        note_node.setGraphicsEffect(opacity_effect)
                    except ValueError:
                        break
                    break
                break

    def changeLabelFontSize(self):
        for text_label in self.text_labels:
            if text_label.underMouse():
                cursor_pos = QCursor.pos()
                input_dialog = QInputDialog(self)
                input_dialog.setWindowTitle("Change Font Size")
                input_dialog.setLabelText("Font Size (5-75):")
                input_dialog.resize(300, 100)
                input_dialog.move(cursor_pos)
                ok = input_dialog.exec()
                if ok:
                    try:
                        font_size = int(input_dialog.textValue())
                        if font_size < 5 or font_size > 75:
                            font_size = 18
                        font = text_label.label.font()
                        font.setPointSize(font_size)
                        text_label.label.setFont(font)
                    except ValueError:
                        break
                break

    def bringToFront(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                note_node.raise_()
                self.title_label.raise_()
                break

        for subcanvas in self.subcanvases:
            if subcanvas.underMouse():
                subcanvas.raise_()
                self.title_label.raise_()
                break

        for text_label in self.text_labels:
            if text_label.underMouse():
                text_label.raise_()
                self.title_label.raise_()
                break

        for image in self.images:
            if image.underMouse():
                image.raise_()
                self.title_label.raise_()
                break

    def sendToBack(self):
        for note_node in self.note_nodes:
            if note_node.underMouse():
                note_node.lower()
                break

        for subcanvas in self.subcanvases:
            if subcanvas.underMouse():
                subcanvas.lower()
                break

        for text_label in self.text_labels:
            if text_label.underMouse():
                text_label.lower()
                break

        for image in self.images:
            if image.underMouse():
                image.lower()
                break

    def createSubcanvas(self):
        cursor_pos = QCursor.pos()
        subcanvas = Subcanvas(parent=self)
        subcanvas.move(cursor_pos)
        subcanvas.lower()
        self.subcanvases.append(subcanvas)
        subcanvas.show()

        self.title_label.raise_()

    def copyActionTriggered(self):
        print("Copy")

    def cutActionTriggered(self):
        print("Cut")

    def pasteActionTriggered(self):
        print("Paste")

    def deleteActionTriggered(self):
        for subcanvas in self.subcanvases:
            if subcanvas.underMouse():
                subcanvas.deleteLater()
                self.subcanvases.remove(subcanvas)
                return

        for note_node in self.note_nodes:
            if note_node.underMouse():
                note_node.deleteLater()
                self.note_nodes.remove(note_node)
                return  
            
        for text_label in self.text_labels:
            if text_label.underMouse():
                text_label.deleteLater()
                self.text_labels.remove(text_label)
                return
            
        for image in self.images:
            if image.underMouse():
                image.deleteLater()
                self.images.remove(image)
                return

    def editTitle(self):
        self.title_edit = QLineEdit(self.title_label.text())
        self.title_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_edit.setStyleSheet("font-size: 20px;")
        self.title_edit.setFixedHeight(35)
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
        self.setWindowTitle("Note Blocks v0.1")

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

    font_id = QFontDatabase.addApplicationFont("fonts/Poppins-Medium.ttf")

    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family)
        font.setPointSize(10)
        app.setFont(font)
    else:
        print("Font not found")

    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
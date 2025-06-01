import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QBrush, QColor, QFont, QTextCursor, QIcon
from wordfrequency import WordFrequency

class SnaccPad(QtWidgets.QMainWindow):
    def __init__(self):
        super(SnaccPad, self).__init__()

        self.initUI()

    def initUI(self):

        new_action = QtWidgets.QAction(QIcon('new.png'), '&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create a new file')
        new_action.triggered.connect(self.new_file)

        save_action = QtWidgets.QAction(QIcon('save.png'), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save the current file')
        save_action.triggered.connect(self.save_file)

        open_action = QtWidgets.QAction(QIcon('open.png'), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open an existing file')
        open_action.triggered.connect(self.open_file)

        exit_action = QtWidgets.QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.close)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        self.txt = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.txt)

        self.highlighter = SnaccPadHighlighter(self.txt.document())

        self.setWindowTitle('snaccpad')
        self.setGeometry(300, 300, 300, 300)

    def new_file(self):
        self.prompt_save()
        self.txt.clear()
        self.setWindowTitle('snaccpad - New File')

    def save_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;SnaccPad Text (*.snc.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.txt.toPlainText())
            self.setWindowTitle(f'snaccpad - {file_name}')
        else:
            QtWidgets.QMessageBox.warning(self, "Save Error", "Failed to save the file.")

    def open_file(self):
        self.prompt_save()
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;SnaccPad Text (*.snc.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                self.txt.setPlainText(f.read())
            self.setWindowTitle(f'snaccpad - {file_name}')
        else:
            QtWidgets.QMessageBox.warning(self, "Open Error", "Failed to open the file.")

    def prompt_save(self):
        if self.txt.document().isModified():
            reply = QtWidgets.QMessageBox.question(self, 'Unsaved Changes', 'You have unsaved changes. Do you want to save them before closing?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if reply == QtWidgets.QMessageBox.Yes:
                self.save_file()
            elif reply == QtWidgets.QMessageBox.Cancel:
                return


class SnaccPadHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super(SnaccPadHighlighter, self).__init__(parent)

        self.thres_color = [(1000, None), (5000, QColor('gray')), (10000, QColor('red'))]
        self.alt_color = QColor('darkred')
        self.wf = WordFrequency()

        self.alt_highlight_format = QTextCharFormat()
        self.alt_highlight_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.alt_highlight_format.setUnderlineColor(self.alt_color)

        self.highlight_formats = {}
        for thresh, color in self.thres_color:
            if color is None:
                self.highlight_formats[thresh] = None
                continue
            fmt = QTextCharFormat()
            fmt.setUnderlineColor(color)
            fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            self.highlight_formats[thresh] = fmt

    def highlightBlock(self, text):
        for word in text.split():
            if not word.isalpha():
                continue

            fix = self.wf.get_frequency_index(word)
            fmt = self.alt_highlight_format
            if fix != -1:
                for thresh, color in self.thres_color:
                    if fix <= thresh:
                        print(word, fix, thresh, color)
                        fmt = self.highlight_formats[thresh]
                        break
                print(word,'\n')
            else:
                print(word, fix, "not found")
            if fmt is None:
                continue
            start_index = text.find(word)
            length = len(word)
            self.setFormat(start_index, length, fmt)




def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = SnaccPad()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


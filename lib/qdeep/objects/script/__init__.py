# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import qdeep.objects.common
from PySide import QtGui, QtCore

class Editor(qdeep.objects.common.Editor):
    objType = 'script'

    def createCentralWidget(self):
        self.textArea = QtGui.QTextEdit()
        self.textArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.textArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.textArea.document().contentsChanged.connect(
            self.documentWasModified)
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.textArea.setFont(font)
        self.textArea.setAcceptDrops(True)
        self.highlighter = Highlighter(self.textArea.document())
        self.setCentralWidget(self.textArea)

    def createActions(self):
        self.actRunScript = QtGui.QAction(
            qdeep.common.getIcon('actions', 'debug-run.png'),
            "Run Script", self,
            shortcut = "F5",
            statusTip = "Run python script",
            triggered = self.runScript)

    def createToolBars(self):
        self.scriptToolBar = self.addToolBar("Script")
        self.scriptToolBar.addAction(self.actRunScript)

    def getModified(self):
        return self.textArea.document().isModified()

    def setModified(self, value):
        self.textArea.document().setModified(value)

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot read file %s:\n%s." % (
                fileName, file.errorString()))
            return False

        instr = QtCore.QTextStream(file)
        self.textArea.setPlainText(instr.readAll())
        self.textArea.document().contentsChanged.connect(
            self.documentWasModified)

        return True

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot write file %s:\n%s." % (fileName,
                file.errorString()))
            return False

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.textArea.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setModified(False)
        self.updateWindowTitle()

        return True

    def runScript(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        nemoa.run(self.getName())
        QtGui.QApplication.restoreOverrideCursor()

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
            "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
            "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
            "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
            "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
            "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
            "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
            "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
            "\\bvolatile\\b", "\\bimport\\b", "\\bdef\\b",
            "\\bTrue\\b", "\\bFalse\\b", "\\breturn\\b"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
            for pattern in keywordPatterns]

        classFormat = QtGui.QTextCharFormat()
        classFormat.setFontWeight(QtGui.QFont.Bold)
        classFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
            classFormat))

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.red)
        self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
            singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.red)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
            quotationFormat))
        self.highlightingRules.append((QtCore.QRegExp("'.*'"),
            quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
            functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength)

import configparser
import sys
from pathlib import Path
from mainwindow import Ui_MainWindow
from treeview import Model, Delegate, Item
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = Model(self)

        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setItemDelegate(Delegate())
        self.ui.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.contextMenu)
        self.ui.pushButton.clicked.connect(self.insertRow)
        self.ui.pushButton_2.clicked.connect(self.delItem)

        ini_file = Path('settings.ini')
        if ini_file.exists():
            config = configparser.ConfigParser()
            config.read(ini_file)
            columns = []
            for option in [ 'column'+str(i) for i in range(1000) ]:
                if not config.has_option( 'columns', option ):
                    continue
                columns.append( config.get( 'columns', option ) )
            self.model.addColumns(columns)

    def contextMenu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction('Add', self.insertRow)
        self.menu.addAction('Delete', self.delItem)
        self.menu.exec_( self.focusWidget().mapToGlobal(point) )
 
    def insertRow(self):
        indexes = self.ui.treeView.selectedIndexes()
        
        if len(indexes) == 0:
            self.model.addItem()
            return
        
        indexes2 = []
        for index in indexes:
            if not index.row() in [ index2.row() for index2 in indexes2 if index2.parent() == index.parent() ]:
                indexes2.append(index)
        
        for index in indexes2:
            self.model.addItem(index)

    def delItem(self):
        indexes = self.ui.treeView.selectedIndexes()
        if len(indexes) == 0:
            return

        indexes2 = []
        for index in indexes:
            if not index.row() in [ index2.row() for index2 in indexes2 if index2.parent() == index.parent() ]:
                indexes2.append(index)
        
        for index in indexes2:
            self.model.removeItem(index)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec_()
 
if __name__ == '__main__':
    main()
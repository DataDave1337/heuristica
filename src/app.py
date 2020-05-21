import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QAction
from PySide2.QtCore import qApp
from plot_data import load_data, scatter_rule
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class MainWindow(QMainWindow):

    def plot_scatter(self):
        rule_attr = 'petal width (cm)'
        attr_min = 1.5
        attr_max = None
        self.scatter_cols = ['sepal length (cm)',
            'sepal width (cm)',
            'petal length (cm)',
            'petal width (cm)']
        df = load_data()
        scatter_plot = scatter_rule(df, self.scatter_cols, rule_attr, attr_min, attr_max)

        return scatter_plot.fig

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setWindowTitle("Heuristic Generator")
        
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)
        fig = self.plot_scatter()
        self.canvas = FigureCanvas(fig)
        self.addToolBar(NavigationToolbar(self.canvas, self))

        self.canvas.updateGeometry()
        self.layout.addWidget(self.canvas)
        self.setFixedSize(geometry.width() * 0.7, geometry.height() * 0.8)

        # List Widgets
        list_box = QtWidgets.QHBoxLayout()
        list1 = QtWidgets.QListWidget()

        list1.addItems(self.scatter_cols)
        list2 = QtWidgets.QListWidget()
        list_box.addWidget(list1)
        button_layout = QtWidgets.QVBoxLayout()
        mButtonToSelected = QtWidgets.QPushButton(">>")
        mBtnMoveToAvailable = QtWidgets.QPushButton(">")
        mBtnMoveToSelected = QtWidgets.QPushButton("<")
        mButtonToAvailable = QtWidgets.QPushButton("<<")

        button_layout.addWidget(mButtonToSelected)
        button_layout.addWidget(mBtnMoveToAvailable)
        button_layout.addWidget(mBtnMoveToSelected)
        button_layout.addWidget(mButtonToAvailable)
        list_box.addLayout(button_layout)
        list_box.addWidget(list2)
        self.layout.addLayout(list_box)
        # self.layout.addWidget(self.dropdown2)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
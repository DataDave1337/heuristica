import sys
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QAction
from PySide2.QtCore import qApp
from plot_data import load_data, scatter_rule
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from rule_part_widget import RulePartWidget
from rule_table_model import RuleTableModel

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


        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QHBoxLayout(self._main)

        self.setup_ui()

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.resize(geometry.width() * 0.7, geometry.height() * 0.8)

    def setup_ui(self):

        left_col = self.setup_left_col()
        right_col = self.setup_right_col()

        self.layout.addLayout(left_col)
        self.layout.addLayout(right_col)

    def setup_left_col(self):
        left_col_layout = QtWidgets.QVBoxLayout()

        fig = self.plot_scatter()
        canvas = FigureCanvas(fig)
        self.addToolBar(NavigationToolbar(canvas, self))

        canvas.updateGeometry()

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
        button_layout.addStretch(stretch=1)
        button_layout.addWidget(mButtonToSelected)
        button_layout.addWidget(mBtnMoveToAvailable)
        button_layout.addWidget(mBtnMoveToSelected)
        button_layout.addWidget(mButtonToAvailable)
        button_layout.addStretch(stretch=1)
        list_box.addLayout(button_layout)
        list_box.addWidget(list2)

        left_col_layout.addWidget(canvas)
        left_col_layout.addLayout(list_box)

        return left_col_layout

    def setup_right_col(self):

        # rule table
        table = QtWidgets.QTableView()

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        model = RuleTableModel(data)
        table.setModel(model)

        right_col_layout = QtWidgets.QVBoxLayout()
        right_col_layout.addWidget(table, stretch=1)
        right_col_layout.addStretch()
        right_col_layout.addWidget(RulePartWidget())
        right_col_layout.addWidget(RulePartWidget())
        right_col_layout.addWidget(RulePartWidget())
        right_col_layout.addWidget(RulePartWidget())
        right_col_layout.addWidget(RulePartWidget())

        add_rule_btn = QtWidgets.QPushButton('Add Rule part')
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch(stretch=1)
        btn_layout.addWidget(add_rule_btn)
        btn_layout.addStretch(stretch=1)

        right_col_layout.addLayout(btn_layout)

        return right_col_layout

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
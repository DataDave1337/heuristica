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
from plot_attr_selection_widget import PlotAttrSelectionWidget

class MainWindow(QMainWindow):
    
    MAX_RULE_PARTS = 7

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

        self.rule_parts = []

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

        self.layout.addWidget(left_col, stretch=2)
        self.layout.addLayout(right_col, stretch=1)

    def setup_left_col(self):

        col_box = QtWidgets.QGroupBox('Rule and data visualization')
        left_col_layout = QtWidgets.QVBoxLayout()

        fig = self.plot_scatter()
        canvas = FigureCanvas(fig)
        self.addToolBar(NavigationToolbar(canvas, self))

        canvas.updateGeometry()

        plot_attr_selection = PlotAttrSelectionWidget(parent=self, attributes=self.scatter_cols)

        left_col_layout.addWidget(canvas)
        left_col_layout.addWidget(plot_attr_selection)
        col_box.setLayout(left_col_layout)
        return col_box

    def add_rule_part(self):

        n_rule_parts = len(self.rule_parts)
        if n_rule_parts < self.MAX_RULE_PARTS:
            rule_part = RulePartWidget(rule_number=n_rule_parts+1)
            self.rule_parts.append(rule_part)
            self.rule_part_layout.insertWidget(n_rule_parts, rule_part)

    def setup_right_col(self):

        right_col_layout = QtWidgets.QVBoxLayout()
        statistics_box = QtWidgets.QGroupBox('Rule statistics')
        statistics_layout = QtWidgets.QVBoxLayout()
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
        statistics_layout.addWidget(table)
        statistics_box.setLayout(statistics_layout)

        rule_part_box = QtWidgets.QGroupBox('Rule definition')
        self.rule_part_layout = QtWidgets.QVBoxLayout()
        self.add_rule_part()
        add_rule_btn = QtWidgets.QPushButton('Add Rule part')
        add_rule_btn.clicked.connect(self.add_rule_part)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch(stretch=1)
        btn_layout.addWidget(add_rule_btn)
        btn_layout.addStretch(stretch=1)
        self.rule_part_layout.addLayout(btn_layout)
        self.rule_part_layout.addStretch(stretch=1)
        rule_part_box.setLayout(self.rule_part_layout)

        right_col_layout.addWidget(statistics_box, stretch=1)
        right_col_layout.addWidget(rule_part_box, stretch=1)

        return right_col_layout

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
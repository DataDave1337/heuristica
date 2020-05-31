from PySide2 import QtWidgets, QtGui, QtCore

class PlotAttrSelectionWidget(QtWidgets.QWidget):

    change_listener = []

    def __init__(self, parent=None, attributes=['feature a', 'feature b', 'feature c'], rule_number=-1):
        QtWidgets.QWidget.__init__(self, parent)
                # List Widgets

        list_box = QtWidgets.QHBoxLayout()

        label_ign = QtWidgets.QLabel('Ignored Attributes:')
        self.list_ign = QtWidgets.QListWidget()
        self.list_ign.addItems(attributes)
        
        list_ign_layout = QtWidgets.QVBoxLayout()
        list_ign_layout.addWidget(label_ign)
        list_ign_layout.addWidget(self.list_ign)

        self.list_plot = QtWidgets.QListWidget()
        list_plot_layout = QtWidgets.QVBoxLayout()
        label_plot = QtWidgets.QLabel('Plotted Attributes:')
        list_plot_layout.addWidget(label_plot)
        list_plot_layout.addWidget(self.list_plot)

        button_layout = QtWidgets.QVBoxLayout()
        self.btn_moveall2plot = QtWidgets.QPushButton(">>")
        self.btn_move2plot = QtWidgets.QPushButton(">")
        self.btn_move2ign = QtWidgets.QPushButton("<")
        self.btn_moveall2ign = QtWidgets.QPushButton("<<")

        button_layout.addSpacing(30)
        button_layout.addWidget(self.btn_moveall2plot)
        button_layout.addWidget(self.btn_move2plot)
        button_layout.addWidget(self.btn_move2ign)
        button_layout.addWidget(self.btn_moveall2ign)
        button_layout.addStretch(stretch=1)

        self.btn_up = QtWidgets.QPushButton("Up")
        self.btn_down = QtWidgets.QPushButton("Down")

        btn_up_down_layout = QtWidgets.QVBoxLayout()
        btn_up_down_layout.addSpacing(30)
        btn_up_down_layout.addStretch(stretch=1)
        btn_up_down_layout.addWidget(self.btn_up)
        btn_up_down_layout.addWidget(self.btn_down)
        btn_up_down_layout.addStretch(stretch=1)

        list_box.addLayout(list_ign_layout)
        list_box.addLayout(button_layout)
        list_box.addLayout(list_plot_layout)
        list_box.addLayout(btn_up_down_layout)

        self.setLayout(list_box)
        
        self.connections()
        self.set_button_status()

    def registerChangeListener(self, func):
        self.change_listener.append(func)

    def get_plot_attr(self):
        return [self.list_plot.item(i).text() for i in range(self.list_plot.count())]

    def move_all2plot(self):
        while self.list_ign.count() > 0:
            item = self.list_ign.takeItem(0)
            self.list_plot.addItem(item)
        self.set_button_status()

    def move_all2ignore(self):
        while self.list_plot.count() > 0:
            item = self.list_plot.takeItem(0)
            self.list_ign.addItem(item)
        self.set_button_status()
    
    def move_sel2plot(self):
        item = self.list_ign.takeItem(self.list_ign.currentRow())
        self.list_plot.addItem(item)
        self.set_button_status()

    def move_sel2ignore(self):
        item = self.list_plot.takeItem(self.list_plot.currentRow())
        self.list_ign.addItem(item)
        self.set_button_status()

    def button_up(self):
        row = self.list_plot.currentRow()
        new_row = row - 1
        item = self.list_plot.takeItem(row)
        self.list_plot.insertItem(new_row, item)
        self.list_plot.setCurrentRow(new_row)
        self.list_plot.repaint()

    def button_down(self):
        row = self.list_plot.currentRow()
        new_row = row + 1
        item = self.list_plot.takeItem(row)
        self.list_plot.insertItem(new_row, item)
        self.list_plot.setCurrentRow(new_row)
        self.list_plot.repaint()
    
    def selection_empty(self, list_widget):
        return len(list_widget.selectedItems()) == 0
    
    def list_empty(self, list_widget):
        return list_widget.count() == 0

    def _call_listener(self):
        for f in self.change_listener:
            f()

    def set_button_status(self):
        self.btn_up.setDisabled(self.selection_empty(self.list_plot) or
                                   (self.list_plot.currentRow() == 0))
        self.btn_down.setDisabled(self.selection_empty(self.list_plot) or
                                   (self.list_plot.currentRow() == self.list_plot.count()-1))
        
        self.btn_move2plot.setDisabled(self.selection_empty(self.list_ign) or self.list_empty(self.list_ign))
        self.btn_moveall2plot.setDisabled(self.list_empty(self.list_ign))
        self.btn_move2ign.setDisabled(self.selection_empty(self.list_plot) or self.list_empty(self.list_plot))
        self.btn_moveall2ign.setDisabled(self.list_empty(self.list_plot))

        # print(f'Plot ATTR {self.get_plot_attr()}')
        
        for btn in [self.btn_move2plot,
                    self.btn_moveall2plot,
                    self.btn_move2ign,
                    self.btn_moveall2ign,
                    self.btn_up,
                    self.btn_down]:
            btn.repaint()

    def connections(self):
        # update button status
        self.list_ign.itemSelectionChanged.connect(self.set_button_status)
        self.list_plot.itemSelectionChanged.connect(self.set_button_status)

        self.btn_moveall2plot.clicked.connect(self.move_all2plot)
        self.btn_move2plot.clicked.connect(self.move_sel2plot)
        self.btn_move2ign.clicked.connect(self.move_sel2ignore)
        self.btn_moveall2ign.clicked.connect(self.move_all2ignore)

        self.btn_up.clicked.connect(self.button_up)
        self.btn_down.clicked.connect(self.button_down)

        # item inserted or deleted signal
        list_model = self.list_plot.model()
        list_model.rowsInserted.connect(self._call_listener)
        list_model.rowsRemoved.connect(self._call_listener)



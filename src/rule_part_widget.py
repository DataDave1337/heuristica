from PySide2 import QtWidgets, QtGui, QtCore

class RulePartWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, options=['feature a', 'feature b', 'feature c'], rule_number=-1):
        QtWidgets.QWidget.__init__(self, parent)

        self.layout = QtWidgets.QHBoxLayout(self)

        # combobox
        combo_box = QtWidgets.QComboBox()
        for option in options:
            combo_box.addItem(option)
        # create widgets
        self.min_box = QtWidgets.QDoubleSpinBox()
        self.max_box = QtWidgets.QDoubleSpinBox()

        
        # add to layout
        if rule_number == -1:
            self.layout.addWidget(QtWidgets.QLabel('Rule Part X', self))
        else:
            self.layout.addWidget(QtWidgets.QLabel(f'Rule Part {rule_number}', self))
        self.layout.addWidget(combo_box)
        self.layout.addWidget(QtWidgets.QLabel('between', self))
        self.layout.addWidget(self.min_box)
        self.layout.addWidget(QtWidgets.QLabel('and', self))
        self.layout.addWidget(self.max_box)
from PySide2 import QtWidgets, QtGui, QtCore

class RulePartWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, feature_ranges={'feature X': [0, 100]}, rule_number=-1):
        QtWidgets.QWidget.__init__(self, parent)

        self.layout = QtWidgets.QHBoxLayout(self)

        # combobox
        self.combo_box = QtWidgets.QComboBox()
        self.feature_ranges = feature_ranges
        self.features = list(self.feature_ranges.keys())
        print(self.features)
        for feature in self.features:
            self.combo_box.addItem(feature)
        # create widgets
        feat_range = self.feature_ranges[self.features[0]]
        self.min_box = QtWidgets.QDoubleSpinBox()
        self.min_box.valueChanged.connect(self._min_box_changed)
        self.max_box = QtWidgets.QDoubleSpinBox()
        self.max_box.valueChanged.connect(self._max_box_changed)

        self.min_box.setRange(*feat_range)
        self.max_box.setRange(*feat_range)

        self.min_box.setValue(feat_range[0])
        self.max_box.setValue(feat_range[1])
    
        # add to layout
        if rule_number == -1:
            self.layout.addWidget(QtWidgets.QLabel('Rule Part X', self))
        else:
            self.layout.addWidget(QtWidgets.QLabel(f'Rule Part {rule_number}', self))
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(QtWidgets.QLabel('between', self))
        self.layout.addWidget(self.min_box)
        self.layout.addWidget(QtWidgets.QLabel('and', self))
        self.layout.addWidget(self.max_box)

        self.combo_box.activated.connect(self.feature_change)

    def feature_change(self):
        print('Current Feature:', self.combo_box.currentText())
        selected_feature = self.combo_box.currentText()
        feat_range = self.feature_ranges[selected_feature]
        self.min_box.setRange(*feat_range)
        self.max_box.setRange(*feat_range)
        self.min_box.setValue(feat_range[0])
        self.max_box.setValue(feat_range[1])
        
    def _min_box_changed(self, val):
        selected_feature = self.combo_box.currentText()
        feat_range = self.feature_ranges[selected_feature]
        # limit by chosen minimum
        self.max_box.setRange(val, feat_range[1])

    def _max_box_changed(self, val):
        selected_feature = self.combo_box.currentText()
        feat_range = self.feature_ranges[selected_feature]
        # limit by chosen minimum
        self.min_box.setRange(feat_range[0], val)

    def get_rule(self):
        
        selected_feature = self.combo_box.currentText()
        min_val = self.min_box.value()
        max_val = self.max_box.value()
        
        return {'feature': selected_feature, 'range': [min_val, max_val]}


    

        # TODO on Spinbox change, set minimum and maximum

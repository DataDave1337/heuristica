import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

class RuleTableWidget(QtWidgets.QTableWidget):
    def __init__(self, dataframe, parent=None):
        shp = dataframe.shape
        super(RuleTableWidget, self).__init__(shp[0], shp[1])
        self._data = dataframe
        self._init_ui()


    def _init_ui(self):
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        cols = self._data.columns.tolist()
        self.setHorizontalHeaderLabels(cols)
        # ignore index
        # row_ids = self._data.index.tolist()
        # self.setVerticalHeaderLabels(row_ids)
        last_row_color = QtGui.QBrush(QtGui.QColor.fromRgb(230,230,230))
        for i, (idx, row) in enumerate(self._data.iterrows()):
            row_list = row.tolist()
            for j, entry in enumerate(row_list):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(entry))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.setItem(i, j, item)
                # Total column Background Color
                if i == len(self._data) - 1:
                    item.setBackground(last_row_color)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.setShowGrid(True)



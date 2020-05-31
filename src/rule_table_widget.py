import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

class RuleTableWidget(QtWidgets.QTableWidget):
    def __init__(self, dataframe, parent=None):
        shp = dataframe.shape
        super(RuleTableWidget, self).__init__(shp[0], shp[1])
        self._data = dataframe

        cols = dataframe.columns.tolist()
        self.setHorizontalHeaderLabels(cols)
        self.update_table(dataframe)

        # ignore index
        # row_ids = data.index.tolist()
        # self.setVerticalHeaderLabels(row_ids)
    
    def update_table(self, data):
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        last_row_color = QtGui.QBrush(QtGui.QColor.fromRgb(230,230,230))
        # update shape
        row_count = self.rowCount()
        col_count = self.columnCount()

        shp = data.shape
        if row_count != shp[0]:
            self.setRowCount(shp[0])
        if col_count != shp[1]:
            self.setColumnCount(shp[1])        


        for i, (idx, row) in enumerate(data.iterrows()):
            row_list = row.tolist()
            for j, entry in enumerate(row_list):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(entry))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.setItem(i, j, item)
                # Total column Background Color
                if i == len(data) - 1:
                    item.setBackground(last_row_color)

        # self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.horizontalHeader().repaint()
        self.setShowGrid(True)





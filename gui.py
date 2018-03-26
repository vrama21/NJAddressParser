from PyQt5 import QtWidgets, QtCore
import pandas as pd
import os
import sys

os.chdir(os.getcwd() + '\CSV')


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


if __name__ == '__main__':
    df = pd.read_csv('Pleasantville.csv', converters={'Zip Code': lambda x: str(x)})
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QTableView()
    model = PandasModel(df)
    view.setModel(model)
    view.show()

    sys.exit(app.exec_())


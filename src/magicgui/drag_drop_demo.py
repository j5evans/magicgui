import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class TableDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Table Demo')
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget()
        self.setCentralWidget(self.table)

        self.initTable()

    def initTable(self):
        headers = ['Name', 'Age', 'Gender']
        data = [
            ['Carlvin', 22, 'Male'],
            ['Jared', 22, 'Male'],
            ['Graham', 22, 'Male'],
            ['James', 22, 'Male'],
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

        # this is the part where the drag/drop is being enabled
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.horizontalHeader().setSectionsMovable(True)
        self.table.horizontalHeader().setDragEnabled(True)
        self.table.horizontalHeader().setDragDropMode(QTableWidget.InternalMove)

    def dropEvent(self, event):
        if event.source() == self.table:
            super().dropEvent(event)
        else:
            if event.isAccepted():
                event.ignore()
                return
            if event.source() != self.table:
                return
            if event.dropAction() != Qt.MoveAction:
                return

            source_index = self.table.horizontalHeader().logicalIndexAt(event.source().pos())
            target_index = self.table.horizontalHeader().logicalIndexAt(event.pos())

            # this is where the columns are being swapped
            self.swapColumns(source_index, target_index)

            event.setDropAction(Qt.MoveAction)
            event.accept()

    def swapColumns(self, source_index, target_index):
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text())
            data.append(row_data)

        headers[source_index], headers[target_index] = headers[target_index], headers[source_index]
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = QTableWidgetItem(data[row][col])
                self.table.setItem(row, col, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TableDemo()
    demo.show()
    sys.exit(app.exec_())
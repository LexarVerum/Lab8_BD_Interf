import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox)
from config import host, user, passw, db_name, porte


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Students")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database=db_name,
                                     user=user,
                                     password=passw,
                                     host=host,
                                     port=porte)

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Students")
        self.monday_gbox = QGroupBox("Monday")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.monday_gbox)
        self._create_monday_table()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)
        self.shedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(3)
        self.monday_table.setHorizontalHeaderLabels(["full_name", "passport", "group_numb"])
        self._update_monday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM student")

        records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.monday_table.setCellWidget(i, 3, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))
            self.monday_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum, day):
        row = list()

        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except: row.append(None)
        try:
            self.cursor.execute("UPDATE SQL запрос на изменение одной строки в базе данных", (row[0],))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        self._update_monday_table()


if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
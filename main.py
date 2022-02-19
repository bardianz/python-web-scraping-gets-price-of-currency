
from tkinter import E
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
import sys
import os


def unicode_number_covertor(number):
    mylist = []
    for char in number:
        if char.isnumeric():
            mylist.append(unidecode(char))
        else:
            mylist.append(char)
    return ''.join(mylist)


def rial_to_toman_convertor(number):
    number = number[:-1]  # remove last char

    char_list = []
    for i in number:  # remove comma
        if i != ',':
            char_list.append(i)

    char_list.reverse()
    counter = 0

    new_list = []

    for char in char_list:
        new_list.append(char)
        counter += 1
        if counter % 3 == 0 and counter != len(char_list):
            new_list.append(",")
    new_list.reverse()
    return ''.join(new_list)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

def get_data():
    url = 'https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    table_row = table.tbody.find("tr")

    data_list = []
    for td in table_row:
        data_list.append(td.find_next("td").text)
    last_price = rial_to_toman_convertor(data_list[0])
    last_change_time = unicode_number_covertor(data_list[9])

    text_last_price = "قیمت دلار = " + last_price
    text_last_change_time = "آخرین آپدیت در = " + last_change_time

    print(last_price)
    print(last_change_time)


app = QApplication(sys.argv)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 342)
        self.setWindowIcon(QtGui.QIcon(resource_path('./assets/icon.ico')))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 211, 20))
        self.label.setObjectName("label")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(510, 30, 93, 28))
        self.refreshBtn.setObjectName("refreshBtn")
        self.refreshBtn.clicked.connect(self.get_data)
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitBtn.setGeometry(QtCore.QRect(410, 30, 93, 28))
        self.exitBtn.clicked.connect(QApplication.instance().quit)
        self.exitBtn.setObjectName("exitBtn")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, 79, 591, 181))
        self.groupBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(280, 50, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code Light")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.last_change = QtWidgets.QLabel(self.groupBox)
        self.last_change.setGeometry(QtCore.QRect(160, 130, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.last_change.setFont(font)
        self.last_change.setTextFormat(QtCore.Qt.PlainText)
        self.last_change.setAlignment(QtCore.Qt.AlignCenter)
        self.last_change.setObjectName("last_change")
        self.price = QtWidgets.QLineEdit(self.groupBox)
        self.price.setGeometry(QtCore.QRect(60, 50, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.price.setFont(font)
        self.price.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.price.setAlignment(QtCore.Qt.AlignCenter)
        self.price.setObjectName("price")
        self.log = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(10, 270, 591, 61))
        self.log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.log.setObjectName("log")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "نمایشگر لحظه ای قیمت دلار"))
        self.label.setText(_translate("MainWindow", "منبع قیمت: https://www.tgju.org"))
        self.refreshBtn.setText(_translate("MainWindow", "رفرش"))
        self.exitBtn.setText(_translate("MainWindow", "خروج"))
        self.groupBox.setTitle(_translate("MainWindow", "قیمت ارز"))
        self.label_2.setText(_translate("MainWindow", "قیمت لحظه‌ای دلار:"))
        self.last_change.setText(_translate("MainWindow", ""))
        self.price.setText(_translate("MainWindow", ""))
        self.get_data()
        
   
    
    def get_data(self):
        self.log.appendPlainText('تلاش برای ورود ...')
        try:
            url = 'https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1'
            page = requests.get(url)
        except:
            self.log.appendPlainText('خطایی زخ داد')
            return
        self.log.appendPlainText('دریافت اطلاعات با موفقیت انجام شد')
        soup = BeautifulSoup(page.text, 'html.parser')

        self.log.appendPlainText('درحال پیدا کردن قیمت دلار ...')

        table = soup.find('table')
        table_row = table.tbody.find("tr")

        data_list = []
        
        for td in table_row:
            data_list.append(td.find_next("td").text)

        if data_list: # if list is not empty

            last_price = rial_to_toman_convertor(data_list[0])
            last_change_time = unicode_number_covertor(data_list[9])

            text_last_change_time = "آخرین آپدیت در " + last_change_time
            self.price.setText(last_price)
            self.last_change.setText(text_last_change_time)
            self.log.appendPlainText('با موفقیت پیدا شد')

            print(last_price)
            print(last_change_time)
        else:
            self.log.appendPlainText('پیدا نشد')

class RunApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(RunApp, self).__init__(parent)
        self.setupUi(self)


def main():
    import sys
    app = QApplication(sys.argv)
    form = RunApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()


# class GUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("نمایشگر قیمت دلار")
#         self.setFixedWidth(300)
#         self.setFixedHeight(300)
#         self.initUI()

#     def initUI(self):
#         label1 = QLabel('Center', self)
#         label1.setMargin(20)
#         label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         label1.setText(text_last_price)
#         label1.move(60, 40)

#         label2 = QLabel(self)
#         label2.setText(text_last_change_time)
#         label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
#         label2.setMargin(20)
#         label2.move(50, 60)

#         btn = QPushButton('خروج', self)
#         btn.clicked.connect(QApplication.instance().quit)
#         btn.move(90, 150)


# window = GUI()
# window.show()
# sys.exit(app.exec())

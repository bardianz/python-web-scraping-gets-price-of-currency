
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

last_price = ''


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
    return(last_price)


app = QApplication(sys.argv)



class User_Price_Calculator_Ui(object):
    dollar_price = '0'
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowIcon(QtGui.QIcon(resource_path('./assets/icon.ico')))
        # Dialog.setEnabled(True)
        Dialog.resize(500, 200)
        Dialog.setMinimumSize(QtCore.QSize(500, 200))
        Dialog.setMaximumSize(QtCore.QSize(500, 200))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        Dialog.setFont(font)
        Dialog.setWindowTitle("تبدیل قیمت دلار به تومان")
        self.label3 = QtWidgets.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(200, 29, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label3.setFont(font)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setObjectName("label3")
        self.btn_user_price = QtWidgets.QPushButton(Dialog)
        self.btn_user_price.setGeometry(QtCore.QRect(190, 80, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_user_price.setFont(font)
        self.btn_user_price.setObjectName("btn_user_price")
        self.btn_user_price.clicked.connect(self.calculate_user_price)
        self.user_dollar_price = QtWidgets.QLineEdit(Dialog)
        self.user_dollar_price.setGeometry(QtCore.QRect(62, 30, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_dollar_price.setFont(font)
        self.user_dollar_price.setText("")
        self.user_dollar_price.setAlignment(QtCore.Qt.AlignCenter)
        self.user_dollar_price.setObjectName("user_dollar_price")
        self.user_toman_result = QtWidgets.QLineEdit(Dialog)
        self.user_toman_result.setGeometry(QtCore.QRect(110, 130, 113, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_toman_result.setFont(font)
        self.user_toman_result.setText("")
        self.user_toman_result.setAlignment(QtCore.Qt.AlignCenter)
        self.user_toman_result.setReadOnly(True)
        self.user_toman_result.setObjectName("user_toman_result")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(230, 130, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label3.setText(_translate("Dialog", "قیمت کالا را به دلار وارد کنید:"))
        self.btn_user_price.setText(_translate("Dialog", "محاسبه"))
        self.user_dollar_price.setPlaceholderText(_translate("Dialog", "قیمت به دلار"))
        self.label.setText(_translate("Dialog", "قیمت کالا به تومان"))
        self.get_data_from_function()
    
    def get_data_from_function(self):
        self.dollar_price = get_data()
        new_list = []
        for char in self.dollar_price:
            if char.isnumeric():
                new_list.append(char)
        self.dollar_price = ""
        for char in new_list:
            self.dollar_price += char
        

    


    def calculate_user_price(self):
        user_price = self.user_dollar_price.text()

        if user_price.isnumeric():
            pass
        else:
            self.user_toman_result.setText("فقط عدد!")
            return
        
        
        result = str(int(user_price) * int(self.dollar_price)) 
        self.user_toman_result.setText(rial_to_toman_convertor(result+'0'))




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.setFixedWidth(650)
        self.setFixedHeight(350)
        self.setWindowIcon(QtGui.QIcon(resource_path('./assets/icon.ico')))
        MainWindow.resize(650, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 211, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.refreshBtn = QtWidgets.QPushButton(self.centralwidget)
        self.refreshBtn.setGeometry(QtCore.QRect(540, 20, 93, 28))
        self.refreshBtn.setObjectName("refreshBtn")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(9, 60, 631, 191))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(300, 50, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code Light")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.last_change = QtWidgets.QLabel(self.groupBox)
        self.last_change.setGeometry(QtCore.QRect(180, 130, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.last_change.setFont(font)
        self.last_change.setTextFormat(QtCore.Qt.PlainText)
        self.last_change.setAlignment(QtCore.Qt.AlignCenter)
        self.last_change.setObjectName("last_change")
        self.price = QtWidgets.QLineEdit(self.groupBox)
        self.price.setGeometry(QtCore.QRect(70, 50, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.price.setFont(font)
        self.price.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.price.setText("")
        self.price.setAlignment(QtCore.Qt.AlignCenter)
        self.price.setReadOnly(True)
        self.price.setObjectName("price")
        self.log = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(10, 260, 631, 81))
        self.log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.log.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.log.setUndoRedoEnabled(False)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.calculate_price = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_price.setGeometry(QtCore.QRect(380, 20, 151, 28))
        self.calculate_price.setObjectName("calculate_price")
        self.calculate_price.clicked.connect(self.calculate_user_price)
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitBtn.setGeometry(QtCore.QRect(280, 20, 93, 28))
        self.exitBtn.setObjectName("exitBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.exitBtn.clicked.connect(QApplication.instance().quit)
        self.refreshBtn.clicked.connect(self.get_data)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.refreshBtn, self.calculate_price)
        MainWindow.setTabOrder(self.calculate_price, self.exitBtn)
        MainWindow.setTabOrder(self.exitBtn, self.price)
        MainWindow.setTabOrder(self.price, self.log)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "نمایشگر لحظه ای قیمت دلار"))
        self.label.setText(_translate(
            "MainWindow", "منبع قیمت: https://www.tgju.org"))
        self.refreshBtn.setText(_translate("MainWindow", "رفرش"))
        self.exitBtn.setText(_translate("MainWindow", "خروج"))
        self.groupBox.setTitle(_translate("MainWindow", "قیمت ارز"))
        self.label_2.setText(_translate("MainWindow", "قیمت لحظه‌ای دلار:"))
        self.last_change.setText(_translate("MainWindow", ""))
        self.price.setText(_translate("MainWindow", ""))
        self.calculate_price.setText(_translate("MainWindow", "محاسبه قیمت یک کالا"))
        self.exitBtn.setText(_translate("MainWindow", "خروج"))
        self.get_data()

    def get_data(self):
        self.refreshBtn.setText("رفرش...")
        self.log.appendPlainText('_____________________________________\n')
        self.log.appendPlainText('در حال آماده سازی برای شروع استخراج اطلاعات ...')
        try:
            url = 'https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1'
            page = requests.get(url)
            self.log.appendPlainText('دریافت اطلاعات انجام شد')
            soup = BeautifulSoup(page.text, 'html.parser')

            self.log.appendPlainText('درحال پیدا کردن قیمت دلار ...')

            table = soup.find('table')
            table_row = table.tbody.find("tr")            
        except:
            self.log.appendPlainText('خطایی زخ داد')
            return


        data_list = []

        for td in table_row:
            data_list.append(td.find_next("td").text)

        if data_list:  # if list is not empty

            last_price = rial_to_toman_convertor(data_list[0])
            last_change_time = unicode_number_covertor(data_list[9])

            text_last_change_time = "آخرین تغییر در " + last_change_time
            self.price.setText(last_price)
            self.last_change.setText(text_last_change_time)
            self.log.appendPlainText('با موفقیت پیدا شد')

            print(last_price)
            print(last_change_time)

            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            last_refrsh = "آخرین رفرش : "+ current_time
            print(last_refrsh)
            self.log.appendPlainText(last_refrsh)
        else:
            self.log.appendPlainText('پیدا نشد')
        self.refreshBtn.setText("رفرش")
        self.log.moveCursor(QtGui.QTextCursor.End)

    def calculate_user_price(self):
        Dialog = QtWidgets.QDialog()
        ui = User_Price_Calculator_Ui()
        ui.setupUi(Dialog)
        Dialog.exec_()



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

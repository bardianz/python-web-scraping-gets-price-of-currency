from multiprocessing.connection import Connection
import sys,os,requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from PyQt5 import QtGui, QtWidgets, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

def is_float_digit(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


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



def connection_checker():
    url = "http://www.google.com"
    timeout = 3
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False


class Main_Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Ui, self).__init__()

        uic.loadUi(resource_path('./ui/mainwindow.ui'), self)
        self.setFixedWidth(650)
        self.setFixedHeight(340)
        self.setWindowIcon(QtGui.QIcon(resource_path('./assets/icon.ico')))
        self.refreshBtn.clicked.connect(self.get_data)
        self.btn_calculate.clicked.connect(self.calculate_user_price)
        self.exitBtn.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.tabWidget.setCurrentIndex(0)
        self.log.append("???????????? ???? ???????????? ???????? ????")           

        self.show()
        self.get_data()
    
    def calculate_user_price(self):
        # self.log.append("\n???? ?????? ???????? ?????????? ????????..." )
        self.log.append("<font color='black'><black>\n???? ?????? ???????? ?????????? ????????...</font>")

        QApplication.setOverrideCursor(Qt.WaitCursor)
        dollar_price = self.price.text()
        new_list = []
        for char in dollar_price:
            if char.isnumeric():
                new_list.append(char)
        dollar_price = ""
        for char in new_list:
            dollar_price += char




        if is_float_digit(dollar_price) == False:
            self.log.append("<font color='red'><red>?????????? ???? ?????????? ???????? ???? ??????</font>")           
            return

        user_price = self.user_dollar_price.text()

        if is_float_digit(user_price):
            result = str(int(float(user_price) * float(dollar_price))) 
            result_text = "%s ???????? ?????????? ?????? ???? %s ??????????" % (user_price, rial_to_toman_convertor(result+'0'))
            self.log.append("<font color='green'><red>"+result_text+"</font>")

            self.user_toman_result.setText(rial_to_toman_convertor(result+'0'))
        else:
            self.user_toman_result.setText("")
            # self.log.append("???????? ?????? ?????? ???????? ????????")
            self.log.append("<font color='red'><red>???????? ?????? ?????? ???????? ????????</font>")

        self.log.moveCursor(QtGui.QTextCursor.End)
        QApplication.restoreOverrideCursor()




    def get_data(self):
        self.progressBar.show()
        self.progressBar.setValue(0)
        self.refreshBtn.setText("????????...")
        self.progressBar.setValue(15)

        # self.log.append("\n")        
        # self.log.append('\n???? ?????? ?????????? ???????? ???????? ???????? ?????????????? ?????????????? ...')
        self.log.append("<font color='black'><black>\n???? ?????? ?????????? ???????? ???????? ???????? ?????????????? ?????????????? ...</font>")           

        
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if not connection_checker():
            self.log.append("<font color='red'><red>?????????????? ?????? ????????????</font>")
        else:
            try:
                url = 'https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1'
                page = requests.get(url)
                self.log.append('???????????? ?????????????? ?????????? ????')
                soup = BeautifulSoup(page.text, 'html.parser')
                self.progressBar.setValue(25)

                self.log.append("<font color='black'><black>?????????? ???????? ???????? ???????? ???????? ...</font>")           
                table = soup.find('table')
                table_row = table.tbody.find("tr")  
                self.progressBar.setValue(50)
            
            except:
                self.log.append("<font color='red'><red>?????????? ???? ??????</font>")
                return


            data_list = []

            for td in table_row:
                data_list.append(td.find_next("td").text)
                self.progressBar.setValue(60)
            
            if data_list and data_list[0] !="" :  # if list is not empty
                
                last_price = rial_to_toman_convertor(data_list[0])
                last_change_time = unicode_number_covertor(data_list[9])

                text_last_change_time = "?????????? ?????????? ???? " + last_change_time
                self.price.setText(last_price)
                self.last_change.setText(text_last_change_time)
                self.log.append("<font color='black'><black>???? ???????????? ???????? ????</font>")           

                self.progressBar.setValue(80)

                print(last_price)
                print(last_change_time)

                from datetime import datetime
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                last_refrsh = "?????????? ???????? : "+ current_time
                print(last_refrsh)
                self.log.append("<font color='black'><black>"+last_refrsh+"</font>")           

                # self.log.append(last_refrsh)
                self.progressBar.setValue(90)

            else:
                self.log.append("<font color='red'><red>?????????? ???? ??????</font>")
                self.log.append("<font color='red'><red>???????? ??????</font>")
                self.progressBar.setStyleSheet("QProgressBar::chunk "
                            "{"
                            "background-color: red;"
                            "}")
                self.progressBar.setValue(10)
        self.progressBar.setValue(100)
        self.refreshBtn.setText("????????")        
        self.log.moveCursor(QtGui.QTextCursor.End)
        QApplication.restoreOverrideCursor()
        self.progressBar.hide()

    
  
app = QtWidgets.QApplication(sys.argv)
window = Main_Ui()
app.exec_()
# -*- coding: utf-8 -*-

import sys
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QComboBox, QPushButton
from PyQt5.QtGui import QPixmap, QFont


class NBRBApi(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("img/belarus_round.png"))
        logo_label.move(0, 0)

        self.days()
        self.month()
        self.year()
        self.load_result_image()

        ok_button = QPushButton('OK', self)
        ok_button.resize(50, 21)
        ok_button.move(220, 200)
        ok_button.clicked.connect(self.make_request)

        self.setFixedSize(300, 400)
        self.setWindowTitle("История курса рубля")
        self.show()

    def days(self):
        """
        Выпадающий список дней.
        """
        self.days_combo = QComboBox(self)
        day_label = QLabel("День", self)
        day_label.move(20, 170)

        for day in range(1, 31):
            self.days_combo.addItem('%d' % day)

        self.days_combo.move(20, 200)

    def month(self):
        """
        Выпадающий список месяцев.
        """

        self.month_combo = QComboBox(self)
        month_label = QLabel("Месяц", self)
        month_label.move(80, 170)

        for month_num in range(1, 13):
            self.month_combo.addItem('%d' % month_num)

        self.month_combo.move(80, 200)

    def year(self):
        """
        Выпадающий список годов.
        """

        self.year_combo = QComboBox(self)
        year_label = QLabel("Год", self)
        year_label.move(140, 170)

        for year_num in range(2005, 2018):
            self.year_combo.addItem('%d' % year_num)

        self.year_combo.move(140, 200)

    def load_result_image(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(18)

        dollar_label = QLabel(self)
        dollar_label.setPixmap(QPixmap("img/dollar.png"))
        dollar_label.move(50, 240)

        self.dollar_value = QLabel("0 руб.", self)
        self.dollar_value.setFont(font)
        self.dollar_value.move(140, 263)

        euro_label = QLabel(self)
        euro_label.setPixmap(QPixmap("img/euro.png"))
        euro_label.move(50, 300)

        self.euro_value = QLabel("0 руб.", self)
        self.euro_value.setFont(font)
        self.euro_value.move(140, 320)

    def make_request(self):
        day_value = self.days_combo.currentText()
        month_value = self.month_combo.currentText()
        year_value = self.year_combo.currentText()

        result = self.get_result(year_value, month_value, day_value)

        self.dollar_value.setText("{0} BYN.".format(result['usd']))
        self.dollar_value.adjustSize()

        self.euro_value.setText("{0} BYN.".format(result['eur']))
        self.euro_value.adjustSize()

    def get_result(self, year, month, day):
        """
        Выполняет запрос к API Нац. банка РБ.

        :param day: Выбранный день.
        :param month: Выбранный номер месяца.
        :param year: Выбранный код
        :return: dict
        """
        result = {
            'usd': 0,
            'eur': 0,
        }

        try:
            # Выполняем запрос к API.
            get_request = requests.get(
                "http://www.nbrb.by/API/ExRates/Rates?onDate={0}-{1}-{2}&Periodicity=0".format(year, month, day)
            )
            json = get_request.json()
            for cur in json:
                if cur["Cur_Abbreviation"] == "USD":
                    result['usd'] = cur['Cur_OfficialRate']
                elif cur["Cur_Abbreviation"] == "EUR":
                    result['eur'] = cur['Cur_OfficialRate']
        except:
            result['usd'] = 'Not Found'
            result['eur'] = 'Not Found'

        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    money = NBRBApi()
    sys.exit(app.exec_())
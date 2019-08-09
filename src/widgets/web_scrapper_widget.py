"""
WebScrapper widget implementation
"""

import datetime
from collections import defaultdict

import json
import requests
import dill as pickle
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import pyqtSignal

import pandas as pd
from src.utils import utils

class WebScrapperWidget(QWidget):
    """
    WebScrapper class docstring
    """

    close_web_scrapper_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(WebScrapperWidget, self).__init__(parent)

        self.filename = utils.get_absolute_resource_path("resources/csv_data/log_data.csv")

        self.title_label = QLabel(text='WebScrapper Widget')
        self.login_label = QLabel(text='Login:')
        self.password_label = QLabel(text='Passowrd:')

        self.login_textbox = QLineEdit(text='wilton.souza')
        self.password_textbox = QLineEdit('Wf0691@2019.1-2')
        self.password_textbox.setEchoMode(QLineEdit.Password)

        self.login_and_sync_button = QPushButton('Login and Sync', self)
        self.login_and_sync_button.clicked.connect(self.scrapp_data)

        self.widget_layout = QGridLayout()
        self.widget_layout.addWidget(self.title_label, 0, 0, 1, 3)
        self.widget_layout.addWidget(self.login_label, 1, 0)
        self.widget_layout.addWidget(self.login_textbox, 1, 1, 1, 2)
        self.widget_layout.addWidget(self.password_label, 2, 0)
        self.widget_layout.addWidget(self.password_textbox, 2, 1, 1, 2)
        self.widget_layout.addWidget(self.login_and_sync_button, 3, 0, 1, 3)

        self.setLayout(self.widget_layout)

    def scrapp_data(self):
        """
        Method to scrapp the data from de Kairos
        """

        data_file = open(self.filename, "w")
        headers = "year,month,week,dow,day,work_day,work_in,status_one,lunch_in,status_two,lunch_out,"\
                  "status_three,work_out,total_time\n"
        data_file.write(headers)

        login_data = {'LogOnModel.UserName' : self.login_textbox.text() + "@compasso.com.br",
                      'LogOnModel.Password' : self.password_textbox.text()}

        def get_start_end_dates(year_input, week_input):
            """
            Method to return the fist and last date from a given week from a given year
            """
            date_input = datetime.date(year_input, 1, 1)
            if date_input.weekday() <= 3:
                date_input = date_input - datetime.timedelta(date_input.weekday())
            else:
                date_input = date_input + datetime.timedelta(7-date_input.weekday())
            delta = datetime.timedelta(days=(week_input-1)*7)
            return date_input + delta, date_input + delta + datetime.timedelta(days=6)

        def sort_dates_list(input_list):
            """
            Method to sort a list of dates with the "yyyy-xx-xx" format
            """
            splitup = input_list.split('-')
            return splitup[0], splitup[1], splitup[2]

        def nested_dict():
            """
            Method to create nested dicts
            """
            return defaultdict(nested_dict)

        with requests.Session() as session:
            kairos_url = "https://www.dimepkairos.com.br/Dimep/Account/LogOn?ReturnUrl=%2FDimep"
            login_request = session.get(kairos_url)
            login_request = session.post(kairos_url, data=login_data)
            user_id = login_request.url[login_request.url.rfind("/")+1:]
            # print(login_request.url)
            print(user_id)
            contatos_url = "https://www.dimepkairos.com.br/Dimep/Pessoas/UserProfilePessoas/" + str(user_id)
            request_two = session.get(contatos_url)
            contatos_page_html = request_two.content
            page_soup = BeautifulSoup(contatos_page_html, 'html.parser')
            conteudo_profile = page_soup.findAll("div", {"class":"ConteudoUserProfile"})
            conteudo_labels = conteudo_profile[0].findAll("label", {"class":"FormText"})
            admission_date = conteudo_labels[13].text.strip()[3:]
            print(admission_date)
            pedidos_url = "https://www.dimepkairos.com.br/Dimep/PedidosJustificativas/Index/" + str(user_id)
            request_three = session.get(pedidos_url)
            pedidos_page_html = request_three.content
            page_soup_3 = BeautifulSoup(pedidos_page_html, 'html.parser')
            options = page_soup_3.findAll("option")
            values = []
            periods = []
            for option in options:
                periods.append(option.text.strip()[6:13])
                values.append(option.get('value'))
            values[:] = [value for value in values if not len(value) == 0]
            periods[:] = [period for period in periods if not period == 'one']
            necessary_data = values[periods.index(admission_date):]
            final_dict = {}
            ordered_dates = []
            for value in necessary_data:
                print(value)
                periodo_pedidos_url = "https://www.dimepkairos.com.br/Dimep/PedidosJustificativas/Index/" +\
                                       str(user_id) + "?per=" + value
                print(periodo_pedidos_url)
                request_four = session.get(periodo_pedidos_url)
                pedidos_periodo_html = request_four.content
                page_soup_4 = BeautifulSoup(pedidos_periodo_html, 'html.parser')
                linhas = page_soup_4.findAll("tr", {"class":"ramoRow"})
                for linha in reversed(linhas):
                    data = linha.findAll("td")[0].text.strip()[4:15]
                    data = data.split("/")[2] + '-' + data.split("/")[1] + "-" + data.split("/")[0]
                    time = linha.findAll("td")[1].text.strip()
                    final_dict.setdefault(data, []).append(time)
                    if data not in ordered_dates:
                        ordered_dates.append(data)
            ordered_dates = sorted(ordered_dates, key=sort_dates_list)
            first_day = get_start_end_dates(datetime.datetime.strptime(ordered_dates[0], "%Y-%m-%d").date().year,
                                            datetime.datetime.strptime(ordered_dates[0], "%Y-%m-%d").date().\
                                            isocalendar()[1])[0]
            last_day = get_start_end_dates(datetime.datetime.strptime(ordered_dates[-1], "%Y-%m-%d").date().year,
                                           datetime.datetime.strptime(ordered_dates[-1], "%Y-%m-%d").date().\
                                           isocalendar()[1])[1]
            full_datelist = [str(i) for i in pd.date_range(first_day, last_day).tolist()]
            full_datelist = [date.split(" ")[0] for date in full_datelist]
            full_datelist = sorted(full_datelist, key=sort_dates_list)
            for date in full_datelist:
                if date not in final_dict:
                    final_dict[date] = ['00:00', '00:00', '00:00', '00:00']
            for date in final_dict:
                while len(final_dict[date]) < 4:
                    final_dict[date].append('00:00')
            # data_dict = defaultdict(nested_dict)
            data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
            for value in full_datelist:
                current_date = datetime.date(int(value.split('-')[0]), int(value.split('-')[1]),
                                             int(value.split('-')[2]))
                day = int(value.split('-')[2])
                month = int(value.split('-')[1])
                year = int(value.split('-')[0])
                date = value.split('-')[2] + '/' + value.split('-')[1]
                __, week, dow = current_date.isocalendar()
                if '00:00' in final_dict[value]:
                    total_time = '00:00'
                else:
                    total_time = utils.total_worked_time(input_list=final_dict[value])
                # print(total_time)
                value_one = ''
                value_two = ''
                value_three = ''
                value_four = ''
                work_day = False
                if total_time == '00:00':
                    value_one = 'background-color : gray'
                    value_two = 'background-color : gray'
                    value_three = 'background-color : gray'
                    value_four = 'color : gray'
                    work_day = False
                    # data_file.write(str(year) + ',' + str(month) + ',' + str(week) + ',' + str(dow) + ',' + date +
                    #  ',' +
                    #                 'False' + ',' + final_dict[value][0] + ',' + 'gray' + ',' + final_dict[value][1] +
                    #                 ',' + 'gray' + ',' + final_dict[value][2] + ',' + 'gray' + ',' +
                    #                 final_dict[value][3] + ',' + total_time + '\n')
                else:
                    value_one, value_two, value_three = utils.get_ij_status(final_dict[value])
                    # print(final_dict[value])
                    value_four = utils.get_work_time_status(final_dict[value])
                    work_day = True
                    # data_file.write(str(year) + ',' + str(month) + ',' + str(week) + ',' + str(dow) + ',' + date +
                    #  ',' +
                    #               'True' + ',' + final_dict[value][0] + ',' + value_one + ',' + final_dict[value][1] +
                    #                ',' + value_two + ',' + final_dict[value][2] + ',' + value_three + ',' +
                    #                 final_dict[value][3] + ',' + total_time + '\n')
                if data_dict[year][month]['total_time']:
                    data_dict[year][month]['total_time'] = utils.sum_times(data_dict[year][month]['total_time'],
                                                                           total_time)
                else:
                    data_dict[year][month]['total_time'] = total_time
                data_dict[year][month][day]['date'] = date
                data_dict[year][month][day]['day_of_week'] = dow
                data_dict[year][month][day]['week'] = week
                data_dict[year][month][day]['work_day'] = work_day
                data_dict[year][month][day]['times_list'] = final_dict[value]
                data_dict[year][month][day]['ij_status'] = [value_one, value_two, value_three]
                data_dict[year][month][day]['total_time'] = total_time
                data_dict[year][month][day]['total_status'] = value_four
            with open(utils.get_absolute_resource_path('resources/csv_data/log_data.pkl'), 'wb') as pickle_file:
                pickle.dump(data_dict, pickle_file, pickle.HIGHEST_PROTOCOL)
            pickle_file.close()
            with open('data.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4)
            json_file.close()
            # with open(utils.get_absolute_resource_path('resources/csv_data/log_data.json'), 'w') as json_file:
            #     json.dump(data_dict, json_file)
            # json_file.close()

            # data_file.close()

"""
WebScrapper widget implementation
"""

import datetime
from collections import defaultdict

import json
import requests
import dill as pickle
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

import pandas as pd
from src.utils import utils


class ScrapperThread(QThread):
    """
    QThread to run the web scrapper on the app background
    """
    progress_step = pyqtSignal(bool)
    finish_signal = pyqtSignal(bool)
    successful_signal = pyqtSignal(bool)
    failure_signal = pyqtSignal(str)
    scrapper_status = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ScrapperThread, self).__init__(parent)

        self.login_val = None
        self.password_val = None

    def set_user_data(self, login, password):
        """
        Method to set the user login and password
        """
        self.login_val = login
        self.password_val = password

    def run(self):
        """
        Class to run the webscrapper thread
        """
        login_data = {'LogOnModel.UserName' : self.login_val + "@compasso.com.br",
                      'LogOnModel.Password' : self.password_val}
        try:
            with requests.Session() as session:
                self.scrapper_status.emit("Scrapping Started!")
                kairos_url = "https://www.dimepkairos.com.br/Dimep/Account/LogOn?ReturnUrl=%2FDimep"
                login_request = session.get(kairos_url)
                login_request = session.post(kairos_url, data=login_data)
                user_id = login_request.url[login_request.url.rfind("/")+1:]
                self.progress_step.emit(True)
                print(user_id)
                contatos_url = "https://www.dimepkairos.com.br/Dimep/Pessoas/UserProfilePessoas/" + str(user_id)
                request_two = session.get(contatos_url)
                contatos_page_html = request_two.content
                page_soup = BeautifulSoup(contatos_page_html, 'html.parser')
                conteudo_profile = page_soup.findAll("div", {"class":"ConteudoUserProfile"})
                conteudo_labels = conteudo_profile[0].findAll("label", {"class":"FormText"})
                admission_date = conteudo_labels[13].text.strip()[3:]
                print(admission_date)
                self.progress_step.emit(True)
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
                self.progress_step.emit(True)
                self.scrapper_status.emit("Buscando dados no Kairos")
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
                    self.progress_step.emit(True)
                ordered_dates = sorted(ordered_dates, key=utils.sort_dates_list)
                first_day = utils.get_start_end_dates(datetime.datetime.strptime(ordered_dates[0],
                                                                                 "%Y-%m-%d").date().year,
                                                      datetime.datetime.strptime(ordered_dates[0], "%Y-%m-%d").date().\
                                                      isocalendar()[1])[0]
                last_day = utils.get_start_end_dates(datetime.datetime.strptime(ordered_dates[-1],
                                                                                "%Y-%m-%d").date().year,
                                                     datetime.datetime.strptime(ordered_dates[-1], "%Y-%m-%d").date().\
                                                     isocalendar()[1])[1]
                full_datelist = [str(i) for i in pd.date_range(first_day, last_day).tolist()]
                full_datelist = [date.split(" ")[0] for date in full_datelist]
                full_datelist = sorted(full_datelist, key=utils.sort_dates_list)
                for date in full_datelist:
                    if date not in final_dict:
                        final_dict[date] = ['00:00', '00:00', '00:00', '00:00']
                for date in final_dict:
                    while len(final_dict[date]) < 4:
                        final_dict[date].append('00:00')
                data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
                total_times_list = []
                counter = 0
                self.scrapper_status.emit("Organizando dados obtidos")
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
                        total_time = utils.total_worked_time(final_dict[value])
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
                    else:
                        value_one, value_two, value_three = utils.get_ij_status(final_dict[value])
                        value_four = utils.get_work_time_status(final_dict[value])
                        work_day = True
                    if data_dict[year][month]['total_time']:
                        data_dict[year][month]['total_time'] = utils.sum_times(data_dict[year][month]['total_time'],
                                                                               total_time)
                    else:
                        data_dict[year][month]['total_time'] = total_time
                    if data_dict[year][month]['month_work_days'] and work_day:
                        data_dict[year][month]['month_work_days'] += 1
                    elif not data_dict[year][month]['month_work_days'] and work_day:
                        data_dict[year][month]['month_work_days'] = 1
                    elif not data_dict[year][month]['month_work_days'] and not work_day:
                        data_dict[year][month]['month_work_days'] = 0
                    total_workable = utils.mult_time('08:00', data_dict[year][month]['month_work_days'])
                    data_dict[year][month]['hours_bank'] = utils.sub_times(total_workable,
                                                                           data_dict[year][month]['total_time'])
                    data_dict[year][month][day]['date'] = date
                    data_dict[year][month][day]['day_of_week'] = dow
                    data_dict[year][month][day]['week'] = week
                    data_dict[year][month][day]['work_day'] = work_day
                    data_dict[year][month][day]['times_list'] = final_dict[value]
                    data_dict[year][month][day]['ij_status'] = [value_one, value_two, value_three]
                    data_dict[year][month][day]['total_time'] = total_time
                    data_dict[year][month][day]['total_status'] = value_four

                total_workable = utils.mult_time('08:00', counter)
                total_worked = utils.sum_times_list(total_times_list)
                data_dict['total_work_days'] = counter
                data_dict['hours_bank'] = utils.sub_times(total_workable, total_worked)
                with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.pkl', 'wb') as pickle_file:
                    pickle.dump(data_dict, pickle_file, pickle.HIGHEST_PROTOCOL)
                pickle_file.close()
                with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.json', 'w') as json_file:
                    json.dump(data_dict, json_file, indent=4)
                json_file.close()
                self.scrapper_status.emit("Processo finalizado!")
                self.progress_step.emit(True)
                self.successful_signal.emit(True)
        except:
            msg = "Erro de conexão! Tente novamente mais tarde"
            self.scrapper_status.emit(msg)
            self.failure_signal.emit(msg)
        self.finish_signal.emit(True)

class WebScrapperWidget(QWidget):
    """
    WebScrapper class docstring
    """
    close_web_scrapper_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(WebScrapperWidget, self).__init__(parent)

        self.title_lbl = QLabel(text='WebScrapper Widget')
        self.login_lbl = QLabel(text='Login:')
        self.password_lbl = QLabel(text='Password:')

        self.login_val = QLineEdit()
        self.password_val = QLineEdit()
        self.password_val.setEchoMode(QLineEdit.Password)

        self.sync_btn = QPushButton('Login and Sync', self)
        self.sync_btn.clicked.connect(self.scrapp_data)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setEnabled(False)

        self.scrapping_status = QLabel()

        self.scrapper_thread = ScrapperThread()
        self.scrapper_thread.finish_signal.connect(self.sync_end)
        self.scrapper_thread.progress_step.connect(self.update_progress_bar)
        self.scrapper_thread.successful_signal.connect(self.sync_end)
        self.scrapper_thread.failure_signal.connect(self.sync_failed)
        self.scrapper_thread.scrapper_status.connect(self.sync_status_text)

        self.widget_layout = QGridLayout()
        self.widget_layout.addWidget(self.title_lbl, 0, 0, 1, 3)
        self.widget_layout.addWidget(self.login_lbl, 1, 0)
        self.widget_layout.addWidget(self.login_val, 1, 1, 1, 2)
        self.widget_layout.addWidget(self.password_lbl, 2, 0)
        self.widget_layout.addWidget(self.password_val, 2, 1, 1, 2)
        self.widget_layout.addWidget(self.sync_btn, 3, 0, 1, 3)
        self.widget_layout.addWidget(self.progress_bar, 4, 0, 1, 3)
        self.widget_layout.addWidget(self.scrapping_status, 5, 0, 1, 3)

        self.setLayout(self.widget_layout)

    def scrapp_data(self):
        """
        Method to start the scrapper thread
        """
        self.sync_btn.setEnabled(False)
        self.progress_bar.setEnabled(True)
        self.progress_bar.setValue(1)
        login = self.login_val.text()
        password = self.password_val.text()
        self.scrapper_thread.set_user_data(login, password)
        self.scrapper_thread.start()

    def update_progress_bar(self, value):
        """
        Method to update the progress bar value
        """
        if value:
            new_val = float(self.progress_bar.value()) + 17 if float(self.progress_bar.value()) + 17 < 100 else 100
            self.progress_bar.setValue(new_val)

    def sync_status_text(self, text):
        """
        Method to sync the webscrapper thread actions with the status text
        """
        self.scrapping_status.setText(text)

    def sync_failed(self, text):
        """
        Method to be executed when the webscrapper thread fails
        """
        print(text)

    def sync_end(self):
        """
        Method to be executed after the web scrapping is done
        """
        self.sync_btn.setEnabled(True)
        self.progress_bar.setEnabled(False)

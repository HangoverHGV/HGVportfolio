import os
import requests
import json
from . import string_to_date
import pdfkit
import pandas as pd
import calendar
import jinja2
import shutil

#  For WINDOWS
# path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

class Connect:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.response = requests.get(self.url, auth=(self.user, self.password))
        self.json_file = json.dumps(self.response.json(), indent=4)

    def create_json(self):
        return self.json_file

    def load_json(self):
        json_load = json.loads(self.json_file)['data']
        return json_load


def create_folder(dir_path):
    work_dir = os.getcwd()
    dir_path = work_dir + '/website/' + dir_path
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def delete_folder(dir_path):
    work_dir = os.getcwd()
    dir_path = work_dir + '/website/' + dir_path
    shutil.rmtree(dir_path)



def export(input_path, output_path):
    work_dir = os.getcwd()
    create_folder('ZIP')
    input_path = work_dir + '/website/' + input_path
    output_path = work_dir + '/website/ZIP/' + output_path
    archive = shutil.make_archive(output_path, 'zip', input_path)
    delete_folder('PDF')
    delete_folder('HTML')
    delete_folder('Report')

    return archive

template_loader = jinja2.FileSystemLoader('.')
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template('website/templates/template.html')

url_schedules = 'https://api.oberplan.com/v1/schedules/'

def Schedules(user, password):
    if os.path.exists('website/ZIP'):
        delete_folder('ZIP')
    create_folder('Report')
    create_folder('HTML')
    create_folder('PDF')
    schedules_obj = Connect(url_schedules, user, password)
    schedules = schedules_obj.load_json()
    return schedules


def reports(schedules, user, password, year, month):
    url_electricieni = f'https://api.oberplan.com/v1/schedules/{schedules}/resources?offset=0&limit=0'
    url_programari = f'https://api.oberplan.com/v1/schedules/{schedules}/bookings?offset=0&limit=0'

    electricieni_obj = Connect(url_electricieni, user, password)
    programari_obj = Connect(url_programari, user, password)

    electricieni = electricieni_obj.load_json()
    programari = programari_obj.load_json()

    num_days = calendar.monthrange(year, month)[1]
    days = [f"{year}-{month:02d}-{day:02d}" for day in range(1, num_days + 1)]

    for e in electricieni:
        cost_center = []
        if 'z.' not in e['name']:
            i = 0
            for p in programari:
                if e['id'] == p['resource_id']:
                    if p['title'] not in cost_center and p['title'].lower() != 'zi libera' and p[
                        'title'].lower() != 'zile ev' and p['title'].lower() != 'nu' \
                            and p['title'].lower() != 'co' and p['title'].lower() != 'co  cote' and p['title'].lower() != 'cote':
                        cost_center.append(p['title'])

            df = pd.DataFrame(columns=days, index=cost_center)

            for p in programari:
                if e['id'] == p['resource_id']:
                    date_formatting = string_to_date.remaining_days(p['start'], p['end'])
                    if date_formatting['start_month'] == month or date_formatting['end_month'] == month:
                        if p['title'] in cost_center:
                            folder_name = calendar.month_abbr[month]
                            create_folder(f'Report/{folder_name}')
                            if date_formatting['start_date'] == date_formatting['end_date']:
                                df.loc[p['title'], date_formatting['start_date']] = string_to_date.hours_stayed(
                                    p['start'], p['end'])
                            else:
                                between = string_to_date.days_between(p['start'], p['end'], month)
                                for b in between:
                                    df.loc[p['title'], b] = 8
            xlsx_name = f'website/Report/{folder_name}/{e["name"]}.xlsx'
            df.to_excel(xlsx_name)


def co_generator(schedules, user, password, month):
    url_electricieni = f'https://api.oberplan.com/v1/schedules/{schedules}/resources?offset=0&limit=0'
    url_programari = f'https://api.oberplan.com/v1/schedules/{schedules}/bookings?offset=0&limit=0'

    electricieni_obj = Connect(url_electricieni, user, password)
    programari_obj = Connect(url_programari, user, password)

    electricieni = electricieni_obj.load_json()
    programari = programari_obj.load_json()


    for e in electricieni:
        if 'z.' not in e['name']:
            for p in programari:
                date_formatting = string_to_date.remaining_days(p['start'], p['end'])
                if date_formatting['start_month'] == month:
                    if e['id'] == p['resource_id'] and 'co' in p['title'].lower() and p['title'].lower() != 'COTE'.lower():
                        days = date_formatting['delta_days'] + 1
                        folder_date = date_formatting['folder_name']
                        context = {
                            'name': e['name'],
                            'start': date_formatting['start_date'],
                            'end': date_formatting['end_date'],
                            'total': str(days)
                        }
                        folder_name = f'{folder_date}'
                        create_folder(f'HTML/{folder_name}')
                        create_folder(f'PDF/{folder_name}')

                        html = template.render(context)
                        html_name = f"website/HTML/{folder_name}/{e['name']}_{folder_date}.html"
                        with open(html_name, 'w') as f:
                            f.write(html)

                        pdf_name = f"website/PDF/{folder_name}/{e['name']}_{folder_date}.pdf"
                        # pdfkit.from_file(html_name, pdf_name, configuration=config) # For WINDOWS
                        pdfkit.from_file(html_name, pdf_name)




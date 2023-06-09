from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta
import converter
import string
import random
from pypdf import PdfMerger
import calendar
import io

from data import obf_1
from snippets import *

import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teste2', methods = ['POST'])
def teste2():
    if request.method == 'POST':
        return request.form

@app.route('/resultado', methods = ['POST'])
def resultado():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        serie = request.form['serie']
        olimpiada = request.form['olimpiada']
        hours = []

        for i in range(1, 8):
            counts = 0
            for j in range(1, 11):
                cell_id = f'{i}_{j}'
                cell_value = request.form.get(cell_id)
                if cell_value == 'on':
                    counts += 1
            hours.append(counts)
    
    date_until_obf = 60 # Test value
    olimpiada = obf_1

    schedule = generate_schedule(hours, olimpiada, date_until_obf)
    files = generate_files(schedule, date_until_obf)
    import pdfkit
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") 
    pdfkit.from_string(files[0], 'out.pdf', configuration=config)

    #final = parse_to_pdf(files, name)

    #return send_file(final)
    
@app.route('/teste')
def teste():
    return f'''
        dirname: {os.path.abspath(os.path.dirname(__file__))}
        cwd: {os.getcwd()}
        ls: {os.listdir()}
    '''

class Circ():
    def __init__(self, n):
        self.n = n
        self.queue = [None] * n
        self.head = self.tail = -1

    def enqueue(self, data):
        if (self.tail + 1) % self.n == self.head:
            print("Full\n")
        elif self.head == -1:
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.n
            self.queue[self.tail] = data

    def dequeue(self):
        if (self.head == -1):
            print("Empty\n")
        elif self.head == self.tail:
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.n
            return temp

    def printCirc(self): 
        if(self.head == -1):
            print("Empty\n")
        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=" ")
            print()
        else:
            for i in range(self.head, self.n):
                print(self.queue[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.queue[i], end=" ")
            print()


def generate_schedule(availability, olympiad, distance):    
    distance_iterable = distance
    subjects = len(olympiad)
    
    queue = Circ(subjects)
    
    for i in olympiad.values():
        queue.enqueue(i)

    schedule = []

    while distance_iterable:
        week_day = (datetime.now().weekday() + (distance - distance_iterable)) % 7

        if availability[week_day]:

            topic = queue.dequeue()

            if topic[-1][1] < availability[week_day]:
                schedule.append('{}${}'.format(topic[-1][0], topic[-1][1]))
                # schedule.append('{}'.format(topic[-1][0]))
                topic.pop()

            elif topic[-1][1] == availability[week_day]:
                schedule.append('{}${}'.format(topic[-1][0], topic[-1][1])) 
                # schedule.append('{}'.format(topic[-1][0]))
                topic.pop()
        
            else:
                schedule.append('{}${}'.format(topic[-1][0], availability[week_day]))
                # schedule.append('{}'.format(topic[-1][0]))
                topic[-1][1] -= availability[week_day]

            if len(topic) > 0: 
                queue.enqueue(topic)
            else:
                items = [queue.dequeue() for i in range(queue.n)]
                queue = Circ(queue.n - 1)
                for i in items: queue.enqueue(i)
        else:
            schedule.append("")
        
        distance_iterable -= 1

    return schedule

def generate_files(schedule, distance, date_format = '%m/%d/%Y'):

    today = datetime.now()
    delta = timedelta(days = 1)
    distance_iterable = distance

    months, year = [], today.year
    topics = {}

    date = today
    while distance_iterable:
        if date.month not in months:
            months.append(date.month)
        topics[date.strftime(date_format)] = schedule[distance - distance_iterable]
        date += delta
        distance_iterable -= 1

    files = []

    for month in months:
        current_file = [begin_calendar.format(calendar.month_name[month], year)]
        current_file.append(calendar_start_week)
    
        date = datetime(year, month, 1)
        first_weekday = date.weekday()
    
        current_file.append(calendar_day_inactive * first_weekday)

        while date.month == month:
            try:
                topic = topics[date.strftime(date_format)].split('$')
                current_text = calendar_text.format(topic[0], ' ' + topic[1] + 'h' if len(topic) - 1 else '') 
            except KeyError:
                current_text = ''
        
            current_file.append(calendar_day.format(date.day, current_text))

            date += delta

            if date.weekday() == 0:
                current_file.append(calendar_end_week)
                current_file.append(calendar_start_week)
    
        current_file.append(calendar_day_inactive * (6 - (date - delta).weekday()))
        current_file.append(calendar_end_week)
        current_file.append(end_calendar)
        files.append(''.join(current_file))

    return files

def get_random_string(length):
    random.seed(datetime.now().timestamp())
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def parse_to_pdf(files, name):
    n = len(files)
    root = os.path.abspath(os.path.dirname(__file__))
    names = []

    for i in range(n):
        is_used = True
        while is_used:
            temp = get_random_string(16)
            temp_file = temp + '.html'
            if temp_file not in os.listdir('user_files'):
                is_used = False
                names.append(temp)

        with io.open('{}/user_files/{}.html'.format(root, temp), 'w', encoding = 'utf8') as f:
            f.write(files[i])
            f.close()

        converter.convert('file://'+'{}/user_files/{}.html'.format(root, temp), '{}/user_files/{}.pdf'.format(root, temp), print_options = {
            'paperHeight': 7.6,
            'paperWidth': 11.7,
            'printBackground': True,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
            'marginTop': 0
        })

    merger = PdfMerger()

    for pdf in ['{}/user_files/{}.pdf'.format(root, i) for i in names]:
        merger.append(pdf)

    is_used = True
    while is_used:
            final = get_random_string(8)
            final_file = final + '.pdf'
            if final_file not in os.listdir('user_files'):
                is_used = False

    merger.write('{}/user_files/{}.pdf'.format(root, final))
    merger.close()

    return '{}/user_files/{}.pdf'.format(root, final)


# calcular dias até a OBF (tem q adicionar pra outras olimpiadas)

# OBF_data = datetime.date(year=2023, month=9, day=21) # aqui define a data da obf
# today = datetime.date.today()
 
# global dias_ate_OBF

# dias_ate_OBF = (OBF_data - today).days # aqui retorna o numero de dias

if __name__ == '__main__':
    app.run(debug = True)
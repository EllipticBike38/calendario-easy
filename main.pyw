import datetime
import os
import sys
import zoneinfo
from tkinter import *
from tkinter import ttk
from typing import Callable
import pathlib
import numpy as np
import threading
import calendar
from functools import partial


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build,  Resource
from googleapiclient.errors import HttpError
from tkcalendar import Calendar
import configparser
config = configparser.ConfigParser()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email', 'openid']

calendarId = ''

service = ...
creds = None

login = None
top = None
root = ...
welcome = ...
date = ...
monday, sunday = ..., ...
now = datetime.datetime.now()
week = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì"]
holidays = [
    '2023-01-01',
    '2023-01-06',
    '2023-02-21',
    '2023-04-09',
    '2023-04-10',
    '2023-04-25',
    '2023-05-01',
    '2023-06-02',
    '2023-08-15',
    '2023-11-01',
    '2023-12-08',
    '2023-12-25',
    '2023-12-26',
    '2023-12-31',
]
week_vars = ...
months2023 = ...
selected_month = now.month
retry = True
user_info = {}
nome_mese_var = ...
f_p_tot = (20, 52)


def main():
    global retry
    while retry:
        retry = False
        auth()
    print("esco")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(pathlib.Path(__file__).parent)

    return os.path.join(base_path, relative_path)


def auth():
    global creds, welcome, date, monday, sunday, now, week, week_vars, root, login, retry, part_times_vars, user_info, nome_mese_var

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if creds and creds.valid:
        try:
            service2 = build('oauth2', 'v2', credentials=creds,
                             static_discovery=False)
            user_info = service2.userinfo().get().execute()
        except:
            ...
            # TODO mostra popup di errore e chiudi tuttoc

        root = Tk()
        try:
            root.iconbitmap(resource_path('static\img\head.ico'))
        except:
            root.iconbitmap(resource_path('static\img\head2.ico'))
        root.title("CalendarPlan")

        # Import the tcl file
        root.tk.call('source', resource_path('themes/forest-dark.tcl'))

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')

        retry = False
        welcome = StringVar(
            value=f"Bentornato {user_info.get('given_name', '')} ({user_info.get('email', '')})")
        date = StringVar(value="test")

        week_vars = [StringVar(value="A") for _ in week]

        mainfrm = ttk.Frame(root, padding=10)
        mainfrm.grid(sticky='nwse')

        cal_frm = ttk.Frame(mainfrm, padding=10)
        # cal_frm.pack(side='right')
        cal_frm.grid(column=1, row=0, sticky='nwse')

        #
        #
        #
        #
        #
        nome_mese_var = StringVar(value='')
        nome_mese = Label(cal_frm, textvariable=nome_mese_var)
        cal_griglia = Frame(cal_frm)
        nome_mese.grid(row=0)
        cal_griglia.grid(row=1)
        # def crea_calendario(month:int, yy=2023):
        #     global nome_mese_var
        #     nome_mese_var.set(calendar.month_name[month])
        #     start_weekday, days=calendar.monthrange(yy, month)
        #     weeks=len(calendar.monthcalendar(yy, month))

        #     monthFrame:dict=months2023[month-1].events
        #     for nn,day in enumerate('LMMGVSD'):
        #         Label(cal_griglia, text=day, padx=20).grid(column=nn, row=0)
        #     print('eventi di', calendar.month_name[month], monthFrame)
        #     for day in range(days):
        #         weekday=(day+start_weekday)%7
        #         week=(day+start_weekday)//7+1
        #         # print(weekday,':',day)
        #         day=day+1
        #         bgcolor=None
        #         fontcolor=None

        #         match monthFrame.get(day,['A',8])[0]:
        #                 case 'A':
        #                     bgcolor='#821'
        #                     fontcolor='#000'
        #                 case 'Sw':
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'
        #                     ...
        #                 case 'Ps':
        #                     ...
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'
        #                 case 'Tr':
        #                     ...
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'
        #                 case 'Fe':
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'
        #                     ...
        #                 case 'Mt':
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'
        #                     ...
        #                 case 'Pe':
        #                     ...
        #                     # bgcolor='#999'
        #                     # fontcolor='#000'

        #         if weekday in (6,5):
        #             bgcolor='#999'
        #             fontcolor='#000'
        #         Label(cal_griglia, text=day, padx=20, pady=20, bg=bgcolor,fg=fontcolor).grid(column=weekday, row=week, sticky=NSEW)

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        frm = ttk.Frame(mainfrm, padding=10)
        # frm.pack(side='left')
        frm.grid(column=0, row=0, sticky='nwse')

        welcome_label = ttk.Label(frm, textvariable=welcome)
        welcome_label.grid(row=0, columnspan=5, sticky='w')
        ttk.Button(frm, textvariable=date, command=open_calendar,
                   style="").grid(column=0, row=1, columnspan=5, pady=5)
        Calendar(frm, selectmode="day", year=now.year,
                 month=now.month, day=now.day)
        ttk.Label(frm, text="DATEPICKER")
        states = ["A", "Sw", "Ps", "Tr", "Fe", 'Mt', 'Pe']

        week = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì"]
        labels = [ttk.Labelframe(frm, text=day.capitalize()) for day in week]
        week_vars = [StringVar(value="A") for _ in week]
        menus = [ttk.OptionMenu(labels[ii], week_vars[ii], states[0],
                                *states, direction="below") for ii in range(5)]
        part_times_vars = [BooleanVar(value=False) for _ in week]
        part_times = [ttk.Checkbutton(
            labels[ii], variable=part_times_vars[ii], text='4h') for ii in range(5)]

        for ii in range(5):
            labels[ii].grid(column=ii, row=2, padx=10)
            menus[ii].configure(width=5)
            menus[ii].pack(padx=15, pady=5)
            part_times[ii].pack(padx=15, pady=5, side='left')
        # TODO creazione labelframe mensile ( in una funzione) con tutti i valori a 0
        # TODO popolatore label dato il mese
        # h lavorate 0 | h ps 3 | g fe 6
        # % sw/tot   1 | h sw 4 | h pe 7
        # h rimaste  2 | h tr 5 | g mt 8.

        class month_labelframe():

            frame: ttk.Labelframe
            date: datetime.date
            events: dict = dict()

            def __init__(self, date: datetime.date = None, master=None) -> None:
                self.date = date
                self.frame = ttk.Labelframe(master,
                                            text=date.strftime("%B") if self.date else 'Mese')
                str_labels = [
                    'ore lavorative',
                    '% smartworking',
                    'ore rimanenti',
                    'ore in sede',
                    'ore in smart',
                    'ore di trasferta',
                    'giorni di ferie',
                    'ore di permesso',
                    'giorni di malattia'
                ]
                self.labels = [
                    Label(self.frame, text=s, justify='left') for s in str_labels
                ]
                self.vars = [
                    StringVar(value='0', name=s+date.strftime("%m%y")) for s in str_labels
                ]
                # TODO list comprehension
                self.labels_n = [
                    Label(self.frame, textvariable=self.vars[ii]) for ii in range(9)
                ]
                [label.grid(column=0, row=nn, sticky='w')
                 for nn, label in enumerate(self.labels)]
                [label.grid(column=1, row=nn, padx=5)
                 for nn, label in enumerate(self.labels_n)]

            def crea_calendario(self, event=None):
                month = self.date.month
                yy = self.date.year
                global nome_mese_var
                nome_mese_var.set(calendar.month_name[month])
                start_weekday, days = calendar.monthrange(yy, month)
                weeks = len(calendar.monthcalendar(yy, month))
                buttons = []
                monthFrame: dict = months2023[month-1].events
                for child in cal_griglia.grid_slaves():
                    child.destroy()
                for nn, day in enumerate('LMMGVSD'):
                    Label(cal_griglia, text=day, padx=20).grid(
                        column=nn, row=0)
                print('eventi di', calendar.month_name[month], monthFrame)
                for day in range(days):
                    weekday = (day+start_weekday) % 7
                    week = (day+start_weekday)//7+1
                    # print(weekday,':',day)
                    day = day+1
                    bgcolor = None
                    fontcolor = None
                    bgtoday = '#313131'
                    match monthFrame.get(day, ['A', 8])[0]:
                        case 'A':
                            bgcolor = '#e73318'
                            fontcolor = '#fff'
                        case 'Sw':
                            bgcolor = '#279cff'
                            fontcolor = '#fff'
                            if monthFrame.get(day, ['A', 8])[1] < 5:
                                fontcolor = 'red'
                            ...
                        case 'Ps':
                            ...
                            bgcolor = '#00ff96'
                            fontcolor = '#fff'
                            if monthFrame.get(day, ['A', 8])[1] < 5:
                                fontcolor = 'red'
                        case 'Tr':
                            ...
                            bgcolor = '#279cff'
                            fontcolor = '#fff'
                        case 'Fe':
                            bgcolor = '#f0da0f'
                            fontcolor = '#fff'
                            ...
                        case 'Mt':
                            bgcolor = '#f0da0f'
                            fontcolor = '#fff'
                            ...
                        case 'Pe':
                            ...
                            bgcolor = '#f0da0f'
                            fontcolor = '#fff'

                    if not np.is_busday([datetime.date(yy, month, day)], (1, 1, 1, 1, 1, 0, 0), holidays):
                        bgcolor = '#999'
                        fontcolor = '#fff'

                    if now.month == month:
                        if day < now.day:
                            bgtoday = '#888'
                        if day == now.day:
                            bgtoday = '#ffb200'
                    buttons.append(Label(cal_griglia, bg=bgcolor,
                                   fg=fontcolor, font='Helvetica 12 bold'))
                    buttons[day-1].grid(column=weekday,
                                        padx=2, pady=2, row=week, sticky=NSEW)
                    Label(buttons[-1], text=day, padx=20, pady=20, bg=bgtoday, fg=fontcolor,
                          font='Helvetica 12 bold').pack(padx=2, pady=2, fill=BOTH)

                    callback = partial(lambda day, yy, month, event: date_formatter(
                        datetime.date(yy, month, day)), day, yy, month)
                    set_child_bind(buttons[day-1], "<Button-1>", callback)
                    # master.bind("<Button-1>", lambda event: print(datetime.date(yy,month, day).isoformat()))

            def update_values(self, service=None):
                service_bool = True
                first_day = datetime.date(self.date.year, self.date.month, 1)
                first_day_after = datetime.date(
                    self.date.year if (self.date.month % 12) else self.date.year+1, (self.date.month % 12)+1, 1)
                last_day = first_day_after-datetime.timedelta(days=1)
                if not service:
                    service_bool = False
                    service = build('calendar', 'v3', credentials=creds,
                                    static_discovery=False)

                # Call the Calendar API
                min_date = datetime.datetime.combine(
                    first_day,
                    datetime.time()).isoformat() + 'Z'
                max_date = datetime.datetime.combine(
                    first_day_after,
                    datetime.time()).isoformat() + 'Z'

                nums = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                #! ORE LAVORATIVE

                nums[0] = np.busday_count(begindates=first_day, enddates=first_day_after, weekmask=(
                    1, 1, 1, 1, 1, 0, 0), holidays=holidays)*4

                events_result = service.events().list(calendarId=calendarId, timeMin=min_date,
                                                      timeMax=max_date, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = [ee for ee in events_result.get('items', []) if ee.get(
                    'description', '') == f"AutoCalendar {config['Settings']['company']}"]
                if not events:
                    print(
                        f'nessun evento a', calendar.month_name[self.date.month])

                ans = dict()
                # Prints the start and name of the next 10 events
                for event in events:
                    start = event['start'].get(
                        'dateTime', event['start'].get('date'))
                    time = (datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end'].get(
                        'date'))) - datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))).seconds/3600
                    start = datetime.date.fromisoformat(start.split('T')[0])
                    name = event['summary'].split(' - ')[0]
                    ans[start.day] = (name, time)
                    if time > 4:
                        time -= .75
# states = ["A", "Sw", "Ps", "Tr", "Fe"]
                    match name:
                        case 'A':
                            ...
                        case 'Sw':
                            nums[4] += time
                        case 'Ps':
                            nums[3] += time
                        case 'Tr':
                            nums[5] += time
                        case 'Fe':
                            nums[6] += time
                        case 'Mt':
                            nums[8] += time
                        case 'Pe':
                            nums[7] += time
                nums[1] = f'{(nums[4]*100)//nums[0]}%'
                nums[2] = nums[0]-sum(nums[3:])
                nums[6] = int(nums[6]/4)
                nums[8] = int(nums[8]/4)

                #     ans.append({
                #         'day': start.isoformat(),
                #         'name': name,
                #         'id': event['id'],
                #         '4h': time <= 4
                #     })
                #     print(start, name, time)
                #     print((start-monday).days)

                # if not service_bool:
                #     tuple(week_vars[xx].set('A') for xx in range(5) if xx not in uptdated)
                # print(ans)
                for n in range(9):
                    self.vars[n].set(nums[n])
                self.events = ans
                return ans

            def call_fun(self):

                self.update_values()
                if self.date.month == selected_month:
                    self.crea_calendario()

        #
        #
        #
        #
        #
        #
        #
        #
        ttk.Button(frm, text="CONFERMA", command=continue_button).grid(
            column=1, row=5, columnspan=1, pady=5)
        show_months_var = StringVar(value="MOSTRA 2023")

        service = build('calendar', 'v3', credentials=creds,
                        static_discovery=False)

        open_or_create_calendar(service)
        months = Frame(frm)
        months.grid(column=0, row=3, columnspan=5, pady=5)

        year = ttk.Labelframe(frm, text='2023', labelanchor='n')
        year.grid(column=0, row=4, columnspan=5, pady=5, sticky='nswe')

        var_ferie = StringVar(value=f'0/{f_p_tot[0]}')
        var_perms = StringVar(value=f'0/{f_p_tot[1]}')
        Label(year, text='Computo ferie', padx=5,
              justify=CENTER).pack(side='left')
        Label(year, textvariable=var_ferie, padx=5,
              justify=CENTER).pack(side='left')
        Label(year, textvariable=var_perms, padx=5,
              justify=CENTER).pack(side='right')
        Label(year, text='Computo Permessi', padx=5,
              justify=CENTER).pack(side='right')

        global months2023
        months2023 = [month_labelframe(datetime.date(
            2023, ii, 1), months) for ii in range(1, 13)]

        def update_ferie_perms(year: list[month_labelframe]=months2023):
            ferie = sum(int(month.vars[6].get()) for month in year)
            permessi = sum(int(float(month.vars[7].get())) for month in year)
            var_ferie.set(f'{ferie}/{f_p_tot[0]}')
            var_perms.set(f'{permessi}/{f_p_tot[1]}')

        thisMonth = datetime.date.today().month-1
        for jj, mm in enumerate(months2023[thisMonth:thisMonth+4] if thisMonth < 12 else months2023[-4:]):
            mm.frame.grid(sticky='nswe', column=jj %
                          4, row=jj//4, padx=5, pady=5)

        def toggle_months():
            global months2023
            if show_months_var.get() == "MOSTRA 2023":
                show_months_var.set("NASCONDI 2023")
                for jj, mm in enumerate(months2023):
                    mm.frame.grid(sticky='nswe', column=jj %
                                  4, row=jj//4, padx=5, pady=5)
            else:
                show_months_var.set("MOSTRA 2023")
                for jj, mm in enumerate(months2023):
                    mm.frame.grid_forget()
                for jj, mm in enumerate(months2023[thisMonth:thisMonth+4] if thisMonth < 12 else months2023[-4:]):
                    mm.frame.grid(sticky='nswe', column=jj %
                                  4, row=jj//4, padx=5, pady=5)

        ttk.Button(frm, textvariable=show_months_var, command=toggle_months).grid(
            column=3, row=5, columnspan=3, pady=5)
        def thread_m():
            global months2023
            t:list[threading.Thread]=[]
            for mm in months2023:
                t.append(threading.Thread(target=mm.call_fun))
                t[-1].start()
                set_child_bind(mm.frame, "<Button-1>", mm.crea_calendario)
            for tt in t:
                tt.join()
            update_ferie_perms(months2023)
            
        thread_v=threading.Thread(target=thread_m)
        
        thread_v.start()
        today = datetime.date.today()

        # months2023[1].frame.grid(column=3, row=3, columnspan=2, pady=5)
        # months2023[1].update_values()
        date_formatter(datetime.date.today())
        root.mainloop()
        ...
    else:
        ...
        login = Tk()
        try:
            login.iconbitmap(resource_path('static\img\head.ico'))
        except:
            login.iconbitmap(resource_path('static\img\head2.ico'))
        login.title("CalendarPlan - Login")
        # Import the tcl file
        login.tk.call('source', resource_path('themes/forest-dark.tcl'))

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')

        frame = ttk.Frame(login, padding=10)
        frame.grid()
        login_label = ttk.Label(
            frame, text="Benvenuto, esegui l'accesso da google")
        login_label.grid(row=0, columnspan=3)
        ttk.Button(frame, text="login", command=login_button).grid(
            column=1, row=1,  pady=5)

        login.mainloop()


def login_button():
    global creds, login, retry

    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                resource_path('credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                retry = True
                login.destroy()
        except:
            retry = True


def continue_button():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    global creds, monday, sunday, months2023
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service: Resource = build(
            'calendar', 'v3', credentials=creds, static_discovery=False)
        events = get_week_events(service)
        event: Callable[[str, datetime.date, bool], dict] = lambda tipo, day, parttime: {
            'summary': f"{tipo} - {config['Settings']['company']}",
            'location': config['Settings']['companyAddress'],
            'description': f"AutoCalendar {config['Settings']['company']}",
            'start': {
                'dateTime': datetime.datetime(day.year, day.month, day.day, 8, 30, 0, tzinfo=zoneinfo.ZoneInfo(config['Settings']['timeZone'])).isoformat(),
                'timeZone': config['Settings']['timeZone'],
            },
            'end': {
                'dateTime':  datetime.datetime(day.year, day.month, day.day, 12 if parttime else 17, 30 if parttime else 15, 0, tzinfo=zoneinfo.ZoneInfo(config['Settings']['timeZone'])).isoformat(),
                'timeZone': config['Settings']['timeZone'],
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60*12},
                ],
            },
        }
        # print(event)
        for ii in range(5):

            insert_event(event(week_vars[ii].get(
            ), monday+datetime.timedelta(ii), part_times_vars[ii].get()), events, service.events())

        # event = service.events().insert(calendarId='mycalendar', body=event).execute()
        months = {monday.month-1, sunday.month-1}
        for jj in list(months):
            # print('MESE: ',jj)
            threading.Thread(target=months2023[jj].call_fun).start()

    except HttpError as error:
        print('An error occurred: %s' % error)


def date_formatter(my_day):
    global monday, sunday
    monday = my_day-datetime.timedelta(my_day.weekday())
    sunday = my_day+datetime.timedelta(6-my_day.weekday())
    date.set(f"{monday.strftime('%d/%m/%Y')} - {sunday.strftime('%d/%m/%Y')}")
    get_week_events()


def insert_event(event: dict, events: list, service):
    if events:
        for ee in events:
            if ee['day'] == event['start']['dateTime'].split('T')[0]:
                service.delete(calendarId=calendarId,
                               eventId=ee['id']).execute()
    if event['summary'].split(' - ')[0] != 'A':
        service.insert(calendarId=calendarId, body=event).execute()


def open_or_create_calendar(service):
    global calendarId
    calendarName = config['Settings']['company'].lower()
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        page_token = calendar_list.get('nextPageToken')
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'].lower() == calendarName:
                calendarId = calendar_list_entry['id']
                page_token = None
                return
        if not page_token:
            break
    calendar = {
        'summary': calendarName,
        'timeZone': config['Settings']['timeZone']
    }
    calendarId = service.calendars().insert(body=calendar).execute()['id']


def get_week_events(service=None):
    global week_vars, part_times_vars, calendarId
    service_bool = True
    if not service:
        service_bool = False
        service = build('calendar', 'v3', credentials=creds,
                        static_discovery=False)
    # Call the Calendar API
    min_date = datetime.datetime.combine(
        monday, datetime.time()).isoformat() + 'Z'
    max_date = datetime.datetime.combine(
        sunday, datetime.time()).isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendarId, timeMin=min_date,
                                          timeMax=max_date, singleEvents=True,
                                          orderBy='startTime').execute()
    events = [ee for ee in events_result.get('items', []) if ee.get(
        'description', '') == f"AutoCalendar {config['Settings']['company']}"]
    if not events:
        # print(
        #     f'No upcoming events found for "AutoCalendar {config["Settings"]["company"]}".')
        ...
    uptdated = set()
    ans = []
    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        time = (datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end'].get(
            'date'))) - datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))).seconds/3600
        start = datetime.date.fromisoformat(start.split('T')[0])
        name = event['summary'].split(' - ')[0]
        if not service_bool:
            week_vars[(start-monday).days].set(name)
            part_times_vars[(start-monday).days].set(time < 5)
            uptdated.add((start-monday).days)
        ans.append({
            'day': start.isoformat(),
            'name': name,
            'id': event['id'],
            '4h': time <= 4
        })
        # print(start, name, time)
        # print((start-monday).days)

    if not service_bool:
        tuple(week_vars[xx].set('A') for xx in range(5) if xx not in uptdated)
    return ans


def set_child_bind(widget, event, callback):
    widget.bind(event, callback)
    for child in widget.children.values():
        set_child_bind(child, event, callback)


def open_calendar():
    ...
    global top
    if top:
        top.destroy()
    top = Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = Calendar(top, selectmode="day", year=monday.year,
                   month=monday.month, day=monday.day)
    cal.pack(padx=10, pady=10)
    cal.pack(fill="both", expand=True)

    def date_pick():
        my_day: datetime.date = cal.selection_get()
        date_formatter(my_day=my_day)
        top.destroy()
    ttk.Button(top, text="ok", command=date_pick).pack()


if __name__ == '__main__':
    print(config.sections())
    config.read(resource_path('user.ini'))
    print(config.sections())
    main()

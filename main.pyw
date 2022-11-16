import datetime
import os
import sys
import zoneinfo
from tkinter import *
from tkinter import ttk
from typing import Callable

import openpyxl
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build,  Resource
from googleapiclient.errors import HttpError
from tkcalendar import Calendar, DateEntry
import configparser
config = configparser.ConfigParser()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email', 'openid']

calendarId = ''

service = ...
creds = None

login = None
top=None
root = ...
welcome = ...
date = ...
monday, sunday = ..., ...
now = datetime.datetime.now()
week = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì"]
week_vars = ...
retry = True
user_info = {}

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
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def auth():
    global creds, welcome, date, monday, sunday, now, week, week_vars, root, login, retry, part_times_vars, user_info

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if creds and creds.valid:
        try:
            service2 = build('oauth2', 'v2', credentials=creds, static_discovery=False)
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
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        welcome_label = ttk.Label(frm, textvariable=welcome)
        welcome_label.grid(row=0, columnspan=5, sticky='w')
        ttk.Button(frm, textvariable=date, command=open_calendar,
                   style="").grid(column=0, row=1, columnspan=5, pady=5)
        Calendar(frm, selectmode="day", year=now.year,
                 month=now.month, day=now.day)
        ttk.Label(frm, text="DATEPICKER")
        states = ["A", "Sw", "Ps", "Tr", "Fe"]

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

        ttk.Button(frm, text="CONFIRM", command=continue_button).grid(
            column=1, row=3, columnspan=3, pady=5)
            
        service = build('calendar', 'v3', credentials=creds, static_discovery=False)
        open_or_create_calendar(service)
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
    global creds, monday, sunday
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    try:
        service: Resource = build('calendar', 'v3', credentials=creds, static_discovery=False)
        events = get_week_events(service)
        event: Callable[[str, datetime.date, bool], dict] = lambda tipo, day, parttime: {
            'summary': f"{tipo} - {config['Settings']['company']}",
            'location': config['Settings']['companyAddress'],
            'description': f"AutoCalendar  {config['Settings']['company']}",
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
        print(event)
        for ii in range(5):

            insert_event(event(week_vars[ii].get(
            ), monday+datetime.timedelta(ii), part_times_vars[ii].get()), events, service.events())
            print(event(week_vars[ii].get(), monday +
                  datetime.timedelta(ii), part_times_vars[ii].get()))
        # event = service.events().insert(calendarId='mycalendar', body=event).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


def date_formatter(my_day):
    global monday, sunday
    monday = my_day-datetime.timedelta(my_day.weekday())
    sunday = my_day+datetime.timedelta(6-my_day.weekday())
    date.set(f"{monday.strftime('%d/%m/%Y')} - {sunday.strftime('%d/%m/%Y')}")
    print(date.get())
    get_week_events()


def insert_event(event: dict, events: list, service):
    if events:
        for ee in events:
            if ee['day'] == event['start']['dateTime'].split('T')[0]:
                service.delete(calendarId=calendarId, eventId=ee['id']).execute()
    if event['summary'].split(' - ')[0] != 'A':
        service.insert(calendarId=calendarId, body=event).execute()

def open_or_create_calendar(service):
    global calendarId
    calendarName=config['Settings']['company'].lower()
    page_token=None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        page_token = calendar_list.get('nextPageToken')
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'].lower() == calendarName:
                calendarId=calendar_list_entry['id']
                page_token=None
                return
        if not page_token:
            break
    calendar = {
    'summary': calendarName,
    'timeZone': config['Settings']['timeZone']
    }
    print(calendar)
    calendarId = service.calendars().insert(body=calendar).execute()['id']

    

def get_week_events(service=None):
    global week_vars, part_times_vars, calendarId
    service_bool = True
    if not service:
        service_bool = False
        service = build('calendar', 'v3', credentials=creds, static_discovery=False)
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
        print('No upcoming events found.')
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
        print(start, name, time)
        print((start-monday).days)

    if not service_bool:
        tuple(week_vars[xx].set('A') for xx in range(5) if xx not in uptdated)
    print(ans)
    return ans


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
        dd, mm, yy = cal.get_date().split("/")
        my_day = datetime.date(int(f"20{yy}"), int(mm), int(dd))
        date_formatter(my_day=my_day)
        top.destroy()
    ttk.Button(top, text="ok", command=date_pick).pack()

if __name__=='__main__':
    print(config.sections())
    config.read(resource_path('user.ini'))
    print(config.sections())
    main()

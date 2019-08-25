# verne-power-monitor-server

Collects and visualizes power monitor logs. See [todo.txt](todo.txt) for a list of outstanding tasks.

- [Setup (local)](#setup-local)
- [Apps](#apps)

## Setup (local)
Instructions are for a Unix system. Commands must be run from the repository base directory.
- `python3 -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `python manage.py migrate`
- (optional) `python manage.py createsuperuser`
- `python manage.py runserver`

## Apps
- [powermonitor](apps/powermonitor): The base app for the project. Contains project-wide code, including the settings and urls files.
- [powerlog](apps/powerlog): Contains code relating to power logs, which provide historical records of power status as reported by sensors.
- [sensor](apps/sensor): Contains code relating to sensors, which are individual devices which log power status.

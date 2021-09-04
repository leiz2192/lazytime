#!/usr/bin/env python
# encoding=utf-8

import time
import datetime
import threading
from borax.calendars.lunardate import LunarDate
import PySimpleGUI as sg

def get_lazy_time():
    prefix = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
    today = LunarDate.today()
    suffix = "{}月{} {}{}年".format(today.cn_month, today.cn_day, today.gz_year, today.animal)
    return "{} {}".format(prefix, suffix)

def update_lazy_time(window):
    while True:
        time.sleep(10)
        window["lazy_time"].update(get_lazy_time())

class UpdateLazyTime(threading.Thread):
    def __init__(self, window):
        super(UpdateLazyTime, self).__init__()
        self._stop = False
        self._window = window

    def run(self) -> None:
        while True:
            time.sleep(1)
            if self._stop:
                break
            self._window["lazy_time"].update(get_lazy_time())

    def stop(self):
        self._stop = True

def main():
    print("Hello LazyTime")

    sg.theme('Reddit')
    layout = [[sg.Text(get_lazy_time(), font=("Microsoft YaHei", 10), key="lazy_time", enable_events=True)]]
    window = sg.Window('', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True, margins=(0,0), alpha_channel=0.6)
    uthread = UpdateLazyTime(window)
    uthread.start()

    last_time = None
    while True:
        event, values = window.read()
        print(datetime.datetime.now().isoformat(), event, values)
        if event != "lazy_time":
            continue
        if last_time and (datetime.datetime.now() - last_time).seconds < 1:
            break
        last_time = datetime.datetime.now()

    uthread.stop()
    window.close()


if __name__ == "__main__":
    main()

from datetime import datetime

from kivy.lang import Builder
from kivy.config import Config

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.picker import MDDatePicker
from kivy.storage.jsonstore import JsonStore


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.icon = "ressources/img/logo_pure.png"
        self.title = "Waha"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        super().__init__(**kwargs)

    def set_birthday(self, date):
        JsonStore('data/info.json').put("info", birthday=date.strftime('%Y:%m:%d'))
        print(date)
        return date

    def show_birthday_date_picker(self):
        try:
            init_date = datetime.strptime(JsonStore('data/info.json').get("info")["birthday"], '%Y:%m:%d')
        except KeyError:
            init_date = datetime.strptime("2000:01:01", '%Y:%m:%d').date()

        date_dialog = MDDatePicker(
            callback=self.set_birthday,
            year=init_date.year,
            month=init_date.month,
            day=init_date.day,
            min_date=datetime.strptime("1990:01:01", '%Y:%m:%d').date(),
            max_date=datetime.strptime("2010:01:01", '%Y:%m:%d').date()
        )
        date_dialog.open()


MainApp().run()

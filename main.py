from datetime import datetime

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Screen(BoxLayout):
    def set_birthday(self, date):
        JsonStore('data/info.json').put("info", birthday=date.strftime('%Y:%m:%d'))
        self.ids["birthday"].text = date.strftime('%d/%m/%Y')
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


class MainApp(MDApp):
    def build(self):
        self.icon = "ressources/img/logo_pure.png"
        self.title = "Waha"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        Window.size = (360, 640)


if __name__ == '__main__':
    app = MainApp()
    app.run()

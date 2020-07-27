from datetime import datetime

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class NameDialog(BoxLayout):
    pass


class ClassDialog(BoxLayout):
    pass


class Waha(BoxLayout):
    def update_info(self):
        name_item = self.ids["name"]
        birthday_item = self.ids["birthday"]
        class_item = self.ids["class"]
        try:
            infos = JsonStore('data/info.json').get("info")
        except KeyError: return
        try:
            name_item.secondary_text = infos["first_name"]
        except KeyError:
            pass
        try:
            name_item.tertiary_text = infos["family_name"]
        except KeyError:
            pass
        try:
            birthday_item.secondary_text = datetime.strptime(infos["birthday"], '%Y:%m:%d').strftime('%d/%m/%Y')
        except KeyError:
            pass
        try:
            class_item.secondary_text = infos["class"]
        except KeyError:
            pass

    def set_birthday(self, date):
        JsonStore('data/info.json').put("info", birthday=date.strftime('%Y:%m:%d'))
        birthday_item = self.ids["birthday"]
        birthday_item.secondary_text = date.strftime('%d/%m/%Y')
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

    def open_name_popup(self):
        dialog = MDDialog(
            title="Changer de nom:",
            type="custom",
            content_cls=NameDialog(),
            buttons=[
                MDFlatButton(
                    text="ANNULER"
                ),
                MDFlatButton(
                    text="OK"
                ),
            ],
        )
        dialog.open()

    def open_class_popup(self):
        dialog = MDDialog(
            title="Changer de classe:",
            type="custom",
            content_cls=ClassDialog(),
            buttons=[
                MDFlatButton(
                    text="ANNULER"
                ),
                MDFlatButton(
                    text="OK"
                ),
            ],
        )
        dialog.open()


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

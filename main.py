from datetime import datetime

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
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


class Waha(GridLayout):
    dialog = None

    def update_info(self):
        store = JsonStore('storage/info.json')

        if store.exists('name'):
            self.ids["name"].secondary_text = store.get("name")["first_name"]
            self.ids["name"].tertiary_text = store.get("name")["family_name"]

        if store.exists('birthday'):
            self.ids["birthday"].secondary_text = datetime.strptime(store.get("birthday")["date"], '%Y:%m:%d').strftime('%d/%m/%Y')

        if store.exists('class'):
            self.ids["class"].secondary_text = store.get("class")["value"]

    def set_birthday(self, date):
        JsonStore('storage/info.json').put("birthday", date=date.strftime('%Y:%m:%d'))
        self.update_info()
        return date

    def show_birthday_date_picker(self):
        try:
            init_date = datetime.strptime(JsonStore('storage/info.json').get("birthday")["date"], '%Y:%m:%d')
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
        self.dialog = MDDialog(
            title="Changer de nom:",
            type="custom",
            content_cls=NameDialog(),
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="OK",
                    on_release=self.set_name
                ),
            ],
            size_hint_x=0.8
        )
        self.dialog.open()

    def set_name(self, *args):
        first_name = self.dialog.content_cls.ids["first_name_input"].text.capitalize()
        family_name = self.dialog.content_cls.ids["family_name_input"].text.upper()
        if len(first_name) > 0: JsonStore('storage/info.json').put("name", first_name=first_name, family_name=family_name)
        self.dialog_close()
        self.update_info()

    def open_class_popup(self):
        self.dialog = MDDialog(
            title="Changer de classe:",
            type="custom",
            content_cls=ClassDialog(),
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="OK",
                    on_release=self.set_class
                ),
            ],
            size_hint_x=0.8
        )
        self.dialog.open()

    def set_class(self, *args):
        JsonStore('storage/info.json').put("class", value=self.dialog.content_cls.ids["class_input"].text.upper()[0:4])
        self.dialog_close()
        self.update_info()

    def dialog_close(self, *args):
        if self.dialog:
            self.dialog.dismiss(force=True)


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

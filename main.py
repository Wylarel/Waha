import random
import string
import webbrowser
from datetime import datetime

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.picker import MDDatePicker


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class NameDialog(BoxLayout):
    pass


class ClassDialog(BoxLayout):
    pass


class NoteListItem(OneLineIconListItem):
    icon = "trash-can"


class HomeScreen(Screen):
    pass


class ScheduleScreen(Screen):
    pass


class NotesScreen(Screen):
    note_to_delete = "new"
    notelist_items = {}
    dialog = None

    def update_notelist(self):
        """
            Met à jour la liste des notes dans l'onglet notes
        """
        store = JsonStore('notes.json')
        notelist = self.ids["notelist"]
        for widget in self.notelist_items:
            notelist.remove_widget(widget)
        self.notelist_items = {}

        for note in store.keys():
            widget = NoteListItem(text=str(store.get(note).get("text")))
            notelist.add_widget(widget)
            self.notelist_items[widget] = note

    def delete_note(self, *args):
        """
            Supprime la note self.note_to_delete, qui est définie par la prochaine fonction
        """
        JsonStore('notes.json').delete(self.notelist_items.get(self.note_to_delete))
        self.dialog_close()
        self.update_notelist()

    def open_note_delete_confirmation_popup(self, *args):
        """
            Ouvre une popup de confirmation pour confirmer la suppression d'une note
        """
        self.note_to_delete = args[0]
        self.dialog = MDDialog(
            title="Voullez vous vraiment supprimer cette note ?",
            text="Vous ne pourrez pas la restaurer",
            type="custom",
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="CONFIRMER",
                    on_release=self.delete_note
                ),
            ],
            size_hint_x=0.8
        )
        self.dialog.open()

    def dialog_close(self):
        """
            Ferme n'importe quel dialogue ouvert
        """
        if self.dialog:
            self.dialog.dismiss(force=True)


class EditnoteScreen(Screen):
    current_note = "new"

    def load_note(self, *args):
        """
            Ouvre une note pour l'éditer
        """
        store = JsonStore('notes.json')
        notelist_items = app.root.get_widget_of_id("notesscreen").notelist_items
        if args[0] in notelist_items.keys():
            note_to_load = notelist_items.get(args[0])
        else:
            note_to_load = ''.join(random.choice(string.ascii_lowercase) for i in range(32))
        if note_to_load in store.keys():
            self.ids["note_textfield"].text = store.get(note_to_load).get("text")
        else:
            self.ids["note_textfield"].text = ""

        app.root.ids["screen_manager"].current = "editnote"
        self.current_note = note_to_load

    def save_note(self):
        """
            Sauvegarde une note
        """
        text = self.ids["note_textfield"].text
        if text.replace(" ", "") == "": return
        store = JsonStore('notes.json')
        store.put(self.current_note, text=text)


class InfoScreen(Screen):
    dialog = None

    def update_info(self):
        """
            Met à jour les informations dans l'onglet "Infos"
        """
        store = JsonStore('info.json')

        if store.exists('name'):
            self.ids["name"].secondary_text = store.get("name")["first_name"]
            self.ids["name"].tertiary_text = store.get("name")["family_name"]

        if store.exists('birthday'):
            self.ids["birthday"].secondary_text = datetime.strptime(store.get("birthday")["date"], '%Y:%m:%d').strftime('%d/%m/%Y')

        if store.exists('class'):
            self.ids["class"].secondary_text = store.get("class")["value"]

    def set_birthday(self, date):
        """
            Définis la date d'anniversaire
        """
        JsonStore('info.json').put("birthday", date=date.strftime('%Y:%m:%d'))
        self.update_info()
        return date

    def show_birthday_date_picker(self):
        """
            Ouvre la popup pour choisir la date d'anniversaire
        """
        try:
            init_date = datetime.strptime(JsonStore('info.json').get("birthday")["date"], '%Y:%m:%d')
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
        """
            Ouvre une popup pour choisir un nom
        """
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
        """
            Définis un nouveau nom
        """
        first_name = self.dialog.content_cls.ids["first_name_input"].text.capitalize()
        family_name = self.dialog.content_cls.ids["family_name_input"].text.upper()
        if len(first_name) > 0: JsonStore('info.json').put("name", first_name=first_name, family_name=family_name)
        self.dialog_close()
        self.update_info()

    def open_class_popup(self):
        """
            Ouvre une popup pour changer de classe
        """
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
        """
            Définis une nouvelle classe
        """
        JsonStore('info.json').put("class", value=self.dialog.content_cls.ids["class_input"].text.upper()[0:4])
        self.dialog_close()
        self.update_info()

    def dialog_close(self, *args):
        """
            Ferme n'importe quel dialogue ouvert
        """
        if self.dialog:
            self.dialog.dismiss(force=True)


class BugreportScreen(Screen):
    pass


class Waha(MDGridLayout):
    def update_info(self):
        self.ids["infoscreen"].update_info()

    def update_notelist(self):
        self.ids["notesscreen"].update_notelist()

    def get_widget_of_id(self, *args):
        return self.ids[args[0]]


class MainApp(MDApp):
    def build(self):
        self.icon = "ressources/img/logo_pure.png"
        self.title = "Waha"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        for file in ["home", "schedule", "notes", "info", "bugreport"]:
            Builder.load_file(f"kv/{file}.kv".format(file=file))
        return Builder.load_file("kv/main.kv")

    def open_link(self, link: str):
        """
            Ouvre un lien hyper-texte dans le navigateur ou application préféré.e
        """
        webbrowser.open(link)


if __name__ == '__main__':
    app = MainApp()
    app.run()

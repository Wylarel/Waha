from kivy.lang import Builder
from kivy.config import Config

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.icon = "ressources/img/logo_pure.png"
        self.title = "Waha"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        super().__init__(**kwargs)


MainApp().run()

import sqlite3
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from Constants import WIDTH, HEIGHT, user


class OrdererScreen(Screen):
    def __init__(self, **kwargs):
        super(OrdererScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        label = Label(text="Ваш объект", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                      pos_hint={'x': 0.1, 'y': 0.5})

        connection = sqlite3.connect("objects.sqlite")
        cursor = connection.cursor()
        request = """
                SELECT title, address, contact_person_fio, contact_person_post, contact_person_number
                FROM objects
                WHERE orderer = ?
                """
        result = cursor.execute(request, user).fetchall()
        print(result)

        layout.add_widget(label)

        self.add_widget(layout)

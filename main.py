from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from screeninfo import get_monitors


monitors = get_monitors()
primary_monitor = monitors[0]

WIDTH = primary_monitor.width
WIDTH -= WIDTH * 0.5

HEIGHT = primary_monitor.height
HEIGHT -= HEIGHT * 0.4

Window.left = ((WIDTH // 0.5) - WIDTH) // 2
Window.top = ((HEIGHT // 0.6) - HEIGHT) // 2

user = "basic"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        button = Button(text='Войти', size=(0.3 * WIDTH, 0.2 * HEIGHT), size_hint=(None, None),
                        pos_hint={'x': 0.36, 'top': 0.4})
        button.bind(on_press=self.open_selection_screen)
        layout.add_widget(button)

        self.add_widget(layout)

    def open_selection_screen(self, instance):
        self.manager.current = 'selection'


class SelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectionScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        options_layout = FloatLayout()
        option1_label = Label(text="Заказчик", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                              pos_hint={'x': 0.1, 'y': 0.5})
        self.option1 = CheckBox(group='options', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0.13, 'y': 0.4})

        option2_label = Label(text="Мастер", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                              pos_hint={'x': 0.45, 'y': 0.5})
        self.option2 = CheckBox(group='options', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0.48, 'y': 0.4})

        option3_label = Label(text="Администратор", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                              pos_hint={'x': 0.8, 'y': 0.5})
        self.option3 = CheckBox(group='options', size_hint=(None, None), size=(50, 50), pos_hint={'x': 0.82, 'y': 0.4})

        self.login_input = TextInput(hint_text='Введите логин', multiline=False, size_hint=(None, None),
                                     size=(0.4 * WIDTH, 0.1 * HEIGHT),
                                     pos_hint={'x': 0.3, 'y': 0.8})

        self.password_input = TextInput(hint_text='Введите пароль', multiline=False, password=True,
                                        size_hint=(None, None),
                                        size=(0.4 * WIDTH, 0.1 * HEIGHT), pos_hint={'x': 0.3, 'y': 0.68})

        enter_button = Button(text='Вход', size=(0.3 * WIDTH, 0.15 * HEIGHT), size_hint=(None, None),
                              pos_hint={'x': 0.35, 'y': 0.2})
        enter_button.bind(on_press=self.enter)

        back_button = Button(text='Назад', size=(0.1 * WIDTH, 0.1 * HEIGHT), size_hint=(None, None),
                             pos_hint={'x': 0.02, 'y': 0.88})
        back_button.bind(on_press=self.back_to_main)

        options_layout.add_widget(option1_label)
        options_layout.add_widget(self.option1)
        options_layout.add_widget(option2_label)
        options_layout.add_widget(self.option2)
        options_layout.add_widget(option3_label)
        options_layout.add_widget(self.option3)

        layout.add_widget(self.login_input)
        layout.add_widget(self.password_input)
        layout.add_widget(options_layout)
        layout.add_widget(enter_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def enter(self, instance):
        global user
        connection = sqlite3.connect("users.sqlite")
        cursor = connection.cursor()
        login = self.login_input.text
        user = login
        password = self.password_input.text
        print(login, password)
        request = """
                SELECT password, post
                FROM users
                WHERE login = ?
                """
        result = cursor.execute(request, login).fetchall()
        print(result)
        if result and result[0][0] == password:
            if self.option1.active:
                if result[0][1].lower() == "заказчик":
                    self.open_orderer()
            elif self.option2.active:
                if result[0][1].lower() == "мастер":
                    self.open_master()
            elif self.option3.active:
                if result[0][1].lower() == "администратор":
                    self.open_admin()
        else:
            raise KeyError
        connection.close()
        pass

    def back_to_main(self, instance):
        self.manager.current = 'main'

    def open_orderer(self):
        self.manager.current = 'orderer'

    def open_master(self):
        self.manager.current = 'master'

    def open_admin(self):
        self.manager.current = 'admin'


class OrdererScreen(Screen):
    def __init__(self, **kwargs):
        global user
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
        # result = cursor.execute(request, (user)).fetchall()
        # print(result)

        layout.add_widget(label)

        self.add_widget(layout)


class MasterScreen(Screen):
    def __init__(self, **kwargs):
        global user
        super(MasterScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        button = Button(text="Оформить заявку", size_hint=(None, None), size=(0.3 * WIDTH, 0.3 * HEIGHT),
                        pos_hint={'x': 0.3, 'y': 0.5})

        connection = sqlite3.connect("objects.sqlite")
        cursor = connection.cursor()
        request = """
                SELECT title, address, contact_person_fio, contact_person_post, contact_person_number
                FROM objects
                WHERE orderer = ?
                """
        # result = cursor.execute(request, (user)).fetchall()
        # print(result)

        layout.add_widget(button)

        self.add_widget(layout)


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        global user
        super(AdminScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        button1 = Button(text="Работы", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                         pos_hint={'x': 0.2, 'y': 0.5})
        button2 = Button(text="Заявки", size_hint=(None, None), size=(0.1 * WIDTH, 0.1 * HEIGHT),
                         pos_hint={'x': 0.7, 'y': 0.5})

        connection = sqlite3.connect("objects.sqlite")
        cursor = connection.cursor()
        request = """
                SELECT title, address, contact_person_fio, contact_person_post, contact_person_number
                FROM objects
                WHERE orderer = ?
                """
        # result = cursor.execute(request, (user)).fetchall()
        # print(result)

        layout.add_widget(button1)
        layout.add_widget(button2)

        self.add_widget(layout)


class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SelectionScreen(name='selection'))
        sm.add_widget(OrdererScreen(name='orderer'))
        sm.add_widget(MasterScreen(name='master'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

    def on_start(self):
        self.root_window.size = (WIDTH, HEIGHT)


if __name__ == '__main__':
    TestApp().run()


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout


class MyApp(App):

    def build(self):
        menu_screen = MenuScreen()
        return menu_screen


class MenuScreen(AnchorLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # BoxLayout для главного экрана
        self.bl_main = BoxLayout(orientation='vertical')

        # Создаем AnchorLayout для заголовка и добавляем это в bl_main
        self.al_l_main = AnchorLayout(anchor_x="center", anchor_y="top")
        self.al_l_main.add_widget(Label(text="       Ударения\nПодготовка к ЕГЭ"))

        self.bl_main.add_widget(self.al_l_main)

        # BoxLayout для кнопок
        self.bl_buttons_main = BoxLayout(orientation='vertical', size_hint=(0.7, 0.9), spacing=15)

        # Кнопка для начала игры
        self.start_button = Button(text='Тренировка')
        self.start_button.bind(on_press=self.start_game)

        # Добавление кнопок в bl_buttons_main
        self.bl_buttons_main.add_widget(self.start_button)
        self.bl_buttons_main.add_widget(Button(text='Результаты'))
        self.bl_buttons_main.add_widget(Button(text='Выход', on_press=self.button_exit_app))

        # Метки для отступа
        self.bl_buttons_main.add_widget(Label())
        self.bl_buttons_main.add_widget(Label())

        # Создаем AnchorLayout для bl_buttons_main и добавляем это в bl_main
        self.al_b_main = AnchorLayout(anchor_x="center", anchor_y="bottom")

        self.al_b_main.add_widget(self.bl_buttons_main)

        self.bl_main.add_widget(self.al_b_main)

        # Добавляем bl_main в MenuScreen
        self.add_widget(self.bl_main)

    def start_game(self, *args):
        # Создаем экран игры и добавляем его в качестве дочернего виджета
        game_screen = GameScreen()
        self.parent.add_widget(game_screen)

        # Удаляем экран меню
        self.parent.remove_widget(self)

    def button_exit_app(self, instance):
        # Закрываем приложение
        App.get_running_app().stop()


class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Кнопка "Новая игра"
        self.restart_game_button = Button(text="Начать заново")
        self.restart_game_button.bind(on_press=self.restart_game)

        self.back_menu_button = Button(text="Вернуться в меню")
        self.back_menu_button.bind(on_press=self.back_menu)

        # Создаем вертикальный BoxLayout
        self.orientation = 'vertical'

        # Метка для отображения вопроса
        self.label_question = Label(text="", font_size=30)
        self.add_widget(self.label_question)

        # BoxLayout для кнопок вариантов ответа
        self.box_buttons = BoxLayout(spacing=35, size_hint_y=.75, size_hint_x=1, height=100, padding=40)
        self.add_widget(self.box_buttons)

        # Ссписок вопросов и ответов для игры
        self.questions = [
            ("АЭРОПОРТЫ", "О", "н"),
            ("БАНТЫ", "А", "Ы"),
            ("БОРОДУ", "О(1 СЛОГ)", "У"),
            ("БУХГАЛТЕРОВ", "А", "У"),
            ("ВОДОПРОВОД", "О(ПОСЛЕДНИЙ СЛОГ)", "О(3 СЛОГ)"),
            ("ГАЗОПРОВОД", "О(ПОСЛЕДНИЙ СЛОГ)", "О(3 СЛОГ)"),
            ("ГРАЖДАНСТВО", "А(2 СЛОГ)", "О"),
            ("ДЕФИС", "И", "Е"),
            ("ДЕШЕВИЗНА", "И", "А"),
            ("ДИСПАНСЕР", "Е", "В"),
            ("ДОГОВОРЁННОСТЬ", "О(3 СЛОГ)", "Ё"),
            ("ДОКУМЕНТ", "Е", "О"),
            ("ДОСУГ", "У", "О"),
            ("ЕРЕТИК", "И", "Е(2 СЛОГ)"),
            ("ЖАЛЮЗИ", "И", "А"),
            ("ЗНАЧИМОСТЬ", "А", "И"),
            ("ИКСЫ", "И", "Ы"),
            ("КАТАЛОГ", "О", "А(2 СЛОГ)"),
            ("КВАРТАЛ", "А(2 СЛОГ)", "А(1 СЛОГ)"),
            ("КИЛОМЕТР", "Е", "И"),
            ("КОНУСОВ", "О(1 СЛОГ)", "О(ПОСЛЕДНИЙ СЛОГ)"),
            ("ВЕРНА", "А", "Е"),
            ("ОПТОВЫЙ", "О(2 СЛОГ)", "О(1 СЛОГ)"),
            ("ЛОВКА", "А", "О"),
            ("БРАЛА", "А(2 СЛОГ)", "А(1 СЛОГ)"),
            ("ОПОШЛИТЬ", "О(2 СЛОГ)", "И"),
            ("КРАЛАСЬ", "А(1 СЛОГ)", "А(2 СЛОГ)"),
            ("НАЧАВ", "А(2 СЛОГ)", "А(1 СЛОГ)"),
            ("ВОВРЕМЯ", "О", "Е"),
            ("ДОНЕЛЬЗЯ", "Е", "О"),
            ("СОЗДАВ", "А", "О")
        ]
        random.shuffle(self.questions)
        self.questions = self.questions[:10]

        self.current_question = 0
        self.correct_answers = 0

        # Создаем кнопки и добавляем их в GridLayout
        for i in range(2):
            self.game_button = Button(text="", font_size=20)
            self.game_button.bind(on_press=self.check_answer)
            self.box_buttons.add_widget(self.game_button)

        # Показываем первый вопрос
        self.show_question()

    def show_question(self):
        question = self.questions[self.current_question]
        self.label_question.text = question[0]
        answer_options = [question[1], question[2]]
        random.shuffle(answer_options)
        for button, answer in zip(self.box_buttons.children, answer_options):
            button.text = answer

    def check_answer(self, instance):
        if instance.text == self.questions[self.current_question][1]:
            instance.background_color = (0, 1, 0, 1)
            self.correct_answers += 1
        else:
            instance.background_color = (1, 0, 0, 1)

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        # Показываем результаты и процент правильных ответов
        percentage = int(self.correct_answers / len(self.questions) * 100)
        self.clear_widgets()
        self.add_widget(Label(text="Результаты: {}% правильных ответов".format(percentage)))

        self.add_widget(self.restart_game_button)
        self.add_widget(self.back_menu_button)

    def restart_game(self, instance):
        self.clear_widgets()
        self.__init__()

    def back_menu(self, instance):
        # Создаем экран меню и добавляем его в качестве дочернего виджета
        menu_screen = MenuScreen()
        self.parent.add_widget(menu_screen)

        # Удаляем экран игры
        self.parent.remove_widget(self)


if __name__ == "__main__":
    MyApp().run()
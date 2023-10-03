# Импорт необходимых библиотек
# Import of necessary libraries
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QTextEdit


class QuestionnaireApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_questions_from_file("questions.txt")

        self.answers = [""] * len(self.questions)
        self.current_question = -1

    def initUI(self):
        self.setWindowTitle('Анкета')
        self.setGeometry(660, 340, 600, 400)
        self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.220639, y1:0.766636, x2:0.861136, y2:0.0795455, stop:0 rgba(62, 155, 240, 255), stop:1 rgba(13, 10, 255, 255));")

        # Создание элементов интерфейса
        # Creating interface elements
        self.name_label = QLabel('Введите имя и фамилию:')
        self.name_label.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);"
            "color: rgb(255, 255, 255);")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(
            "color: rgb(255, 255, 255);")


        self.next_button = QPushButton('Далее')
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.220639, y1:0.766636, x2:0.861136, y2:0.0795455, stop:0 rgba(62, 155, 240, 255), stop:1 rgba(13, 10, 255, 255));\n"
            "color: rgb(255, 255, 255);")

        self.question_label = QLabel()
        self.question_label.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);"
                                      "color: rgb(255, 255, 255);")
        self.answer_group = QButtonGroup()
        self.radio_buttons = []


        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.previous_question)
        self.back_button.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.220639, y1:0.766636, x2:0.861136, y2:0.0795455, stop:0 rgba(62, 155, 240, 255), stop:1 rgba(13, 10, 255, 255));\n"
            "color: rgb(255, 255, 255);")

        # Убираем чекбоксы с окна ввода имени
        # Remove the checkboxes from the name input box
        self.radio_buttons = [QRadioButton() for _ in range(3)]
        for radio_button in self.radio_buttons:
            radio_button.setVisible(False)
            radio_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);")
            self.answer_group.addButton(radio_button)


        # Установить их начальную видимость на False
        # Set their initial visibility to False
        for radio_button in self.radio_buttons:
            radio_button.setVisible(False)
            radio_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);")
            self.answer_group.addButton(radio_button)

        self.back_button.setVisible(False)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)

        question_layout = QVBoxLayout()
        question_layout.addWidget(self.question_label)
        for radio_button in self.radio_buttons:
            question_layout.addWidget(radio_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_input)

        # Добавление вертикальный макет с вопросом и радиокнопками
        # Adding a vertical layout with a question and radiobuttons
        main_layout.addLayout(question_layout)

        # Добавление горизонтальный макет с кнопками "Назад" и "Далее"
        # Adding a horizontal layout with "Back" and "Next" buttons
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


    def clear_radio_buttons(self):
        for radio_button in self.radio_buttons:
            radio_button.setChecked(False)
    def next_question(self):
        if self.current_question < len(self.questions):
            self.answers[self.current_question - 0] = self.get_selected_answer()
            self.current_question += 1
            if self.current_question < len(self.questions):
                # Отключаем режим эксклюзивного выбора
                # Disable exclusive selection mode
                self.answer_group.setExclusive(False)
                # Снимаем выделение с чекбоксов перед отображением следующего вопроса
                # Deselect the checkboxes before displaying the next question
                self.clear_radio_buttons()
                self.show_question()
                # Включаем режим эксклюзивного выбора обратно
                # Turn exclusive selection mode back on
                self.answer_group.setExclusive(True)
            else:
                self.save_answers()

    def previous_question(self):
        if self.current_question > 0:
            self.answers[self.current_question] = self.get_selected_answer()
            self.current_question -= 1
            # Очищаем выбор с чекбоксов
            # Clear the selection from the checkboxes
            self.clear_radio_buttons()
            self.show_question()


    # Отображаем вопросы
    # Show questions
    def show_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.setText(question_data["question"])
        self.question_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);\n"
            "color: rgb(255, 255, 255);")

        if self.current_question == -1:
            self.name_label.setVisible(True)
            self.name_input.setVisible(True)
            self.next_button.setVisible(True)
            for radio_button in self.radio_buttons:
                radio_button.setVisible(False)
            self.back_button.setVisible(False)
        else:
            self.name_label.setVisible(False)
            self.name_input.setVisible(False)
            self.next_button.setVisible(True)

            for i, radio_button in enumerate(self.radio_buttons):
                if i < len(question_data["answers"]):
                    radio_button.setText(question_data["answers"][i])
                    radio_button.setVisible(True)
                    # Снимаем выбор с чекбоксов
                    # Deselect the checkboxes
                    radio_button.setChecked(False)
                else:
                    radio_button.setVisible(False)

        if self.current_question == 1:
            self.back_button.setVisible(True)

    # Выбираем выбранные ответы
    # Chose the selected answers
    def get_selected_answer(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return f"{self.questions[self.current_question]['question']} - Вариант {i + 1} - {radio_button.text()}"
        return f"Вопрос {self.current_question + 1}: Ответ не выбран"

    def save_answers(self):
        name = self.name_input.text()
        with open(f"{name}_answers.txt", "w") as file:
            file.write(f"Имя: {name}\n")
            for i, answer in enumerate(self.answers):
                question = self.questions[i]["question"]
                answer = answer.replace(f"Вопрос {i + 1}: ", "")
                file.write(f"Вопрос {i + 1}: {answer}\n")
        self.close()

    # Загружаем вопросы и ответы с txt файла
    # Load the questions and answers from the txt file
    def load_questions_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            questions = []
            current_question = None

            for line in lines:
                line = line.strip()

                if line.startswith("Вопрос"):
                    if current_question:
                        questions.append(current_question)
                    current_question = {"question": line}
                elif line:
                    if current_question:
                        current_question.setdefault("answers", []).append(line)

            if current_question:
                questions.append(current_question)

            self.questions = questions

def main():
    app = QApplication(sys.argv)
    window = QuestionnaireApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

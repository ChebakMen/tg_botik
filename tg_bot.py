import telebot
from telebot import types
import subprocess
import os

TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
bot = telebot.TeleBot(TOKEN)

user_state = {}

lessons = {
    '1': {
        'title': 'Introduction to Python',
        'images': ['lesson_1_ter_kar_1.jpg', 'lesson_1_ter_kar_2.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_1_otv.jpg',
        'code': 'hallo word',
    },
    '2': {
        'title': 'Working with Lists in Python',
        'images': ['lesson_1_ter_kar_3.jpg', 'lesson_1_ter_kar_4.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_2_otv.jpg',
        'code': 'dogs',
    },
    '3': {
        'title': 'след хуйня',
        'images': ['lesson_1_ter_kar_3.jpg', 'lesson_1_ter_kar_4.jpg'],
        'task': 'lesson_1_task.jpg',
        'answer': 'lesson_3_otv.jpg',
        'code': 'cats', #####################################################################
    },
    # Add more lessons as needed
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Set the initial state to the first lesson (assuming 1 is the starting lesson number)
    user_state[message.chat.id] = 1

    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Начало', 'ТП', 'Как', 'Я')
    bot.send_message(message.from_user.id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Начало':
        choose_language(message)
    elif message.text == 'Как':
        show_instructions(message)
    elif message.text == 'ТП' or message.text == 'Я':
        bot.send_message(message.chat.id, "Функционал этой кнопки еще не реализован.")
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_instructions(message):
    user_state[message.chat.id] = 'show_instructions'
    instructions_text = "Для использования бота, следуйте этим шагам:\n\n1. Выберите раздел 'Начало', 'ТП', 'Как', 'Я'.\n2. Следуйте инструкциям, выбирая язык программирования и действия.\n3. Введите свой код, используя кнопку 'Ввести код'.\n4. После ввода кода, выберите 'Показать ответ' для проверки.\n5. Выберите 'Далее' для перехода к следующему уроку.\n6. В любой момент можно вернуться назад, используя кнопку 'Назад'."
    bot.send_message(message.chat.id, instructions_text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_back)

def choose_language(message):
    user_state[message.chat.id] = 'choose_language'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Python', 'C++', 'Назад')
    bot.send_message(message.chat.id, "Выбери язык программирования:", reply_markup=markup)
    bot.register_next_step_handler(message, choose_option)

def choose_option(message):
    if message.text == 'Python' or message.text == 'C++':
        user_state[message.chat.id] = 'choose_option'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_option(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option'
        lesson_number = '1'
        show_lesson(message, lesson_number)
    elif message.text == 'Выбор урока':
        show_lessons(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lessons(message):
    user_state[message.chat.id] = 'show_lessons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lesson_number, lesson_info in lessons.items():
        markup.row(f'Урок {lesson_number}: {lesson_info["title"]}')

    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_lesson)

def handle_lesson(message):
    lesson_number = message.text.split(' ')[-1]
    if lesson_number in lessons:
        show_lesson(message, lesson_number)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson(message, lesson_number):
    user_state[(message.chat.id, 'lesson_number')] = lesson_number ##############################################################
    lesson_info = lessons[lesson_number]

    bot.send_message(message.chat.id, f"Урок {lesson_number}: {lesson_info['title']}")###############################################

    for image_path in lesson_info['images']:
        if os.path.exists(image_path):
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        else:
            bot.send_message(message.chat.id, f"Image file not found: {image_path}")

    task_image = open(lesson_info['task'], 'rb')
    bot.send_photo(message.chat.id, task_image)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Ввести код', 'Далее', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_action)

def handle_action(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code)
    elif message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_next_lesson(message):
    try:
        # Получаем текущий номер урока из user_state
        current_lesson_number = int(user_state.get((message.chat.id, 'lesson_number'), 1)) 

        # Увеличиваем номер урока
        next_lesson_number = current_lesson_number + 1

        # Проверяем, существует ли информация о следующем уроке
        if str(next_lesson_number) in lessons:
            # Обновляем user_state
            user_state[(message.chat.id, 'lesson_number')] = next_lesson_number

            # Отображаем следующий урок
            show_lesson(message, str(next_lesson_number))
        else:
            bot.send_message(message.chat.id, "Урок не найден.")
            handle_back(message)

    except ValueError:
        bot.send_message(message.chat.id, "Error: Lesson number is not a valid integer.")
        handle_back(message)


def handle_user_code(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        expected_code = lesson_info.get('code')
        if expected_code is None:
            bot.send_message(message.chat.id, "Error: Expected code not found.")
            handle_back(message)
            return

        user_code = message.text

        # Compare the user's code with the expected code

        # Установка ограничения времени выполнения и объема памяти
        process = subprocess.run(['python', '-c', user_code], capture_output=True, text=True, timeout=5)
        if process.returncode != 0:
            raise Exception(f"Произошла ошибка при выполнении кода. Код завершился с кодом возврата {process.returncode}.")

        # Проверка результата выполнения кода
        if expected_code in process.stdout:
            bot.send_message(message.chat.id, "Код выполнен верно!")
            show_answer(message)
        else:
            bot.send_message(message.chat.id, "Код выполнен, но результат не соответствует ожидаемому.")
            show_buttons(message)
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "Превышено ограничение времени выполнения кода.")
        show_buttons(message)
    except Exception as e:
        # Если произошла ошибка при выполнении кода, сообщаем об этом пользователю
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении кода:\n{str(e)}")
        show_buttons(message)


def show_buttons(message):
    user_state[message.chat.id] = 'show_buttons'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать ответ', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_code)

def handle_buttons_after_code(message):
    if message.text == 'Показать ответ':
        show_answer(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_answer(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        answer_image_path = lesson_info.get('answer')
        if answer_image_path is None:
            bot.send_message(message.chat.id, "Error: Answer image not found.")
            handle_back(message)
            return

        # Replace this with your logic to show the answer image
        answer_image = open(answer_image_path, 'rb')
        bot.send_photo(message.chat.id, answer_image)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Далее', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_buttons_after_answer)

    except Exception as e:
        # Handle any exceptions that may occur during the process
        bot.send_message(message.chat.id, f"Error while showing answer:\n{str(e)}")
        handle_back(message)

def handle_buttons_after_answer(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_back(message):
    if message.chat.id in user_state:
        current_state = user_state[message.chat.id]
        user_state.pop(message.chat.id, None)

        if current_state == 'choose_language':
            handle_start(message)
        elif current_state == 'choose_option':
            choose_language(message)
        elif current_state == 'handle_option':
            choose_option(message)
        elif current_state == 'handle_action':
            handle_option(message)
        elif current_state == 'show_lessons':
            choose_option(message)
        elif current_state == 'handle_lesson':
            show_lessons(message)
        elif current_state == 'handle_next':
            handle_action(message)
        else:
            handle_start(message)
    else:
        handle_start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
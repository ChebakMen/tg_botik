import telebot
from telebot import types
import subprocess
import os
import sqlite3
import telebot

PAYMENTS_TOKEN = "1744374395:TEST:c686f7af7ceeca26bd1a"

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)

TOKEN = '6696202375:AAEacBpBfUG3t2mvfD8q8gAF807DNxI-J5w'
bot = telebot.TeleBot(TOKEN)

user_state = {}


# Подключение к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей     #########################################################    Изменил базу добавил 1 строчку
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        premka INTEGER,
        lessons INTEGER
    )
''')

# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()


lessons_cpp = { #########################################################    Нужно изменить ответы на вопросы
    '1': {
        'title': 'Introduction to C++',
        'images': ['cpp/lesson_1_ter_kar_1.jpg', 'cpp/lesson_1_ter_kar_2.jpg'],
        'task': 'cpp/lesson_1_task.jpg',
        'answer': 'cpp/lesson_1_otv.jpg',
        'code': 'Hello, World!',
    },
    '2': {
        'title': 'Working with Arrays in C++',
        'images': ['cpp/lesson_2_ter_kar.jpg'],
        'task': 'cpp/lesson_2_task.jpg',
        'answer': 'cpp/lesson_2_otv.jpg',
        'code': 'Hello, World!',
    },
    
}

lessons_py = {
    '1': {
        'title': 'Introduction to Python',
        'images': ['py/lesson_1_ter_kar.jpg'],
        'task': 'py/lesson_1_task.jpg',
        'answer': 'py/lesson_1_otv.jpg',
        'code': 'Hallo, world',
    },
    '2': {
        'title': 'Working with Lists in Python',
        'images': ['py/lesson_2_ter_kar.jpg'],
        'task': 'py/lesson_2_task.jpg',
        'answer': 'py/lesson_2_otv.jpg',
        'code': 'dogs',
    },
    '3': {
        'title': 'Python',
        'images': ['py/lesson_3_ter_kar.jpg'],
        'task': 'py/lesson_3_task.jpg',
        'answer': 'py/lesson_3_otv.jpg',
        'code': 'cats', 
    },
    
}




@bot.message_handler(commands=['start'])#
def handle_start(message):
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else message.from_user.first_name

    # Добавление нового пользователя в базу данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, premka, lessons)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, 0, 0))  # По умолчанию начинаем с первого урока
    conn.commit()
    conn.close()

    # Остальной код обработки старта
    user_state[message.chat.id] = 1
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Начало', 'ТП', 'Как', 'Я')
    bot.send_message(user_id, "Привет! Я бот для изучения языков программирования. Выбери раздел:", reply_markup=user_markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Начало':
        choose_language(message)
    elif message.text == 'Как':
        show_instructions(message)
    elif message.text == 'ТП':
        handle_buy(message)
    elif message.text == 'Я':
        handle_me(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

#Кнопка Я(информация обо мне)############################################################################    Добавил блок 
def handle_me(message):
    try:
        user_id = message.from_user.id
        first_name = message.chat.first_name
        username = message.chat.username

        bot.send_message(message.chat.id, f"{first_name} ({username})")
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT lessons FROM users WHERE user_id=?', (user_id,))
        result = cursor.fetchone()

        if result and result[0] == 0:
            bot.send_message(message.chat.id, "Вы не прошли не один урок.\n\nВаши достижения: \nПока что нет, но вы не растраивайтесь!")
            conn.close()
            return
        elif result and result[0] == 1:
            bot.send_message(message.chat.id, "Пройденно уроков: 1\n\nВаши достижения: \nНачинающий программист!")
            conn.close()
            return
        elif result and result[0] == 2:
            bot.send_message(message.chat.id, "Пройденно уроков: 2\n\nВаши достижения: \nНачинающий програмист + !")
            conn.close()
            return
        elif result and result[0] == 3:
            bot.send_message(message.chat.id, "Пройденно уроков: 3\n\nВаши достижения: \nНачинающий програмист ++")
            conn.close()
            return
        elif result and result[0] == 4:
            bot.send_message(message.chat.id, "Пройденно уроков: 3\n\nВаши достижения: \nНачинающий програмист +++")
            conn.close()
            return
        elif result and result[0] == 5:
            bot.send_message(message.chat.id, "Пройденно уроков: 3\n\nВаши достижения: \nПрограмист")
            conn.close()
            return
        

        

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка в выводе информации")



def handle_buy(message):
    try:
        user_id = message.from_user.id

        # Проверка на тестовый платеж
        if bot.token.split(':')[1] == 'TEST':
            bot.send_message(message.chat.id, "Тестовый платеж!!!")

        # Идентификатор пользователя и номер инвойса в качестве payload
        payload = f"{user_id}-{message.message_id}"

        # Проверка, оплачивал ли пользователь уже подписку
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT premka FROM users WHERE user_id=?', (user_id,))
        result = cursor.fetchone()

        if result and result[0] == 1:
            bot.send_message(message.chat.id, "Вы уже оплатили подписку.")
            conn.close()
            return

        # Отправка инвойса пользователю
        bot.send_invoice(message.chat.id,
                         title="Подписка на бота",
                         description="Активация подписки на бота на 1 месяц",
                         provider_token=PAYMENTS_TOKEN,
                         currency="rub",
                         photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                         photo_width=416,
                         photo_height=234,
                         photo_size=416,
                         is_flexible=False,
                         prices=[PRICE],
                         start_parameter="one-month-subscription",
                         invoice_payload=payload)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обработчик PreCheckoutQuery
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

# Обработчик успешного платежа
@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    try:
        user_id = message.from_user.id

        # Обработка успешного платежа
        payment_info = message.successful_payment
        amount = payment_info.total_amount // 100

        # Обновление статуса оплаты в базе данных
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET premka=1 WHERE user_id=?', (user_id,))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, f"Платёж на сумму {amount} руб. прошел успешно!!!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


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
    if message.text == 'Python':
        user_state[message.chat.id] = 'choose_option_py'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option_py)
    elif message.text == 'C++':
        user_state[message.chat.id] = 'choose_option_cpp'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Начать', 'Выбор урока', 'Назад')
        bot.send_message(message.chat.id, "Отлично! Теперь выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option_cpp)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")


def handle_option_py(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option_py'
        lesson_number = '1'
        show_lesson_py(message, lesson_number)
    elif message.text == 'Выбор урока':
        show_lesson_pys_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_pys_py(message):
    user_state[message.chat.id] = 'show_lesson_pys_py'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lesson_number, lesson_info in lessons_py.items():
        markup.row(f'Урок {lesson_number}: {lesson_info["title"]}')

    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_lesson_py)
    


def handle_lesson_py(message):

    if message.text == 'Урок 1: Introduction to Python':
        show_lesson_py(message, '1')
    elif message.text == 'Урок 2: Working with Lists in Python':
        show_lesson_py(message, '2')
    elif message.text == 'Урок 3: Python':
        show_lesson_py(message, '3')
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_py(message, lesson_number):
    
    user_state[(message.chat.id, 'lesson_number')] = lesson_number
    lesson_info = lessons_py[lesson_number]

    bot.send_message(message.chat.id, f"Урок {lesson_number}: {lesson_info['title']}")

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
    bot.register_next_step_handler(message, handle_action_py)

def handle_action_py(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action_py'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code_py)
    elif message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_next_lesson_py(message):###############################################
    try:
        # Получаем текущий номер урока из user_state
        current_lesson_number = int(user_state.get((message.chat.id, 'lesson_number'), 1)) 

        # Увеличиваем номер урока
        next_lesson_number = current_lesson_number + 1

        # Проверяем, существует ли информация о следующем уроке
        if str(next_lesson_number) in lessons_py:
            # Обновляем user_state
            user_state[(message.chat.id, 'lesson_number')] = next_lesson_number

            # Отображаем следующий урок
            show_lesson_py(message, str(next_lesson_number))
        else:
            bot.send_message(message.chat.id, "Урок не найден.")
            handle_back(message)

    except ValueError:
        bot.send_message(message.chat.id, "Error: Lesson number is not a valid integer.")
        handle_back(message)


def handle_user_code_py(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_py.get(str(lesson_number))
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
            
           
            ##################################################################################   Добавил чтобы увеличивался урок
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET lessons = lessons + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
    
            ####################################################################
            show_answer_py(message)
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
    bot.register_next_step_handler(message, handle_buttons_after_code_py)

def handle_buttons_after_code_py(message):
    if message.text == 'Показать ответ':
        show_answer_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_answer_py(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_py.get(str(lesson_number))
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
        bot.register_next_step_handler(message, handle_buttons_after_answer_py)

    except Exception as e:
        # Handle any exceptions that may occur during the process
        bot.send_message(message.chat.id, f"Error while showing answer:\n{str(e)}")
        handle_back(message)

def handle_buttons_after_answer_py(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_py(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")



#########################################################################

def handle_option_cpp(message):
    if message.text == 'Начать':
        user_state[message.chat.id] = 'handle_option_cpp'
        lesson_number = '1'
        show_lesson_cpp(message, lesson_number)
    elif message.text == 'Выбор урока':
        show_lesson_pys_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_pys_cpp(message):
    user_state[message.chat.id] = 'show_lesson_pys_cpp'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for lesson_number, lesson_info in lessons_cpp.items():
        markup.row(f'Урок {lesson_number}: {lesson_info["title"]}')

    markup.row('Назад')
    bot.send_message(message.chat.id, "Выбери урок:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_lesson_cpp)

def handle_lesson_cpp(message):
    if message.text == 'Урок 1: Introduction to C++':
        show_lesson_cpp(message, '1')
    elif message.text == 'Урок 2: Working with Arrays in C++':
        show_lesson_cpp(message, '2')  
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_lesson_cpp(message, lesson_number):
    user_state[(message.chat.id, 'lesson_number')] = lesson_number
    lesson_info = lessons_cpp[lesson_number]

    bot.send_message(message.chat.id, f"Урок {lesson_number}: {lesson_info['title']}")

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
    bot.register_next_step_handler(message, handle_action_cpp)


def handle_action_cpp(message):
    if message.text == 'Ввести код':
        user_state[message.chat.id] = 'handle_action_cpp'
        bot.send_message(message.chat.id, "Пожалуйста, введите свой код:")
        bot.register_next_step_handler(message, handle_user_code_cpp)
    elif message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_user_code_cpp(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_cpp.get(str(lesson_number))
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

        # Сравнение кода пользователя с ожидаемым кодом

        # Установка ограничения времени выполнения и объема памяти
        process = subprocess.run(['g++', '-x', 'c++', '-'], input=user_code, capture_output=True, text=True, timeout=5)
        if process.returncode != 0:
            raise Exception(f"Произошла ошибка при выполнении кода. Код завершился с кодом возврата {process.returncode}.")

        # Проверка результата выполнения кода
        if expected_code in process.stdout:
            bot.send_message(message.chat.id, "Код выполнен верно!")
            
##################################################################################   Добавил чтобы увеличивался урок
            user_id = message.from_user.id
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET lessons = lessons + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
##################################################################################   Добавил чтобы увеличивался урок
            
            show_answer_cpp(message)
        else:
            bot.send_message(message.chat.id, "Код выполнен, но результат не соответствует ожидаемому.")
            show_buttons_cpp(message)
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "Превышено ограничение времени выполнения кода.")
        show_buttons_cpp(message)
    except Exception as e:
        # Если произошла ошибка при выполнении кода, сообщаем об этом пользователю
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении кода:\n{str(e)}")
        show_buttons_cpp(message)

def show_buttons_cpp(message):
    user_state[message.chat.id] = 'show_buttons_cpp'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Показать ответ', 'Назад')
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_buttons_after_code_cpp)

def handle_buttons_after_code_cpp(message):
    if message.text == 'Показать ответ':
        show_answer_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def show_answer_cpp(message):
    try:
        lesson_number = user_state.get((message.chat.id, 'lesson_number'))
        if lesson_number is None:
            bot.send_message(message.chat.id, "Error: Lesson number not found.")
            handle_back(message)
            return

        lesson_info = lessons_cpp.get(str(lesson_number))
        if lesson_info is None:
            bot.send_message(message.chat.id, "Error: Lesson information not found.")
            handle_back(message)
            return

        answer_image_path = lesson_info.get('answer')
        if answer_image_path is None:
            bot.send_message(message.chat.id, "Error: Answer image not found.")
            handle_back(message)
            return

        # Замените это своей логикой для отображения изображения ответа
        answer_image = open(answer_image_path, 'rb')
        bot.send_photo(message.chat.id, answer_image)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Далее', 'Назад')
        bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_buttons_after_answer_cpp)

    except Exception as e:
        # Обработка любых исключений, которые могут возникнуть в процессе
        bot.send_message(message.chat.id, f"Error while showing answer:\n{str(e)}")
        handle_back(message)

def handle_buttons_after_answer_cpp(message):
    if message.text == 'Далее':
        bot.send_message(message.chat.id, "Переход к следующему уроку.")
        handle_next_lesson_cpp(message)
    elif message.text == 'Назад':
        handle_back(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки на клавиатуре.")

def handle_next_lesson_cpp(message):
    try:
        current_lesson_number = int(user_state.get((message.chat.id, 'lesson_number'), 1)) 
        next_lesson_number = current_lesson_number + 1

        if str(next_lesson_number) in lessons_cpp:
            user_state[(message.chat.id, 'lesson_number')] = next_lesson_number
            show_lesson_cpp(message, str(next_lesson_number))
        else:
            bot.send_message(message.chat.id, "Урок не найден.")
            handle_back(message)

    except ValueError:
        bot.send_message(message.chat.id, "Error: Lesson number is not a valid integer.")
        handle_back(message)

# Добавьте аналогичные функции для C++, как вы сделали для Python, с учетом особенностей каждого языка.




def handle_back(message):
    if message.chat.id in user_state:
        current_state = user_state[message.chat.id]
        user_state.pop(message.chat.id, None)

        if current_state == 'choose_language':
            handle_start(message)
        elif current_state == 'choose_option_py':
            choose_language(message)
        elif current_state == 'choose_option_cpp':
            choose_language(message)
        elif current_state == 'handle_option_py':
            choose_option(message)
        elif current_state == 'handle_option_cpp':
            choose_option(message)
        elif current_state == 'handle_action_py':
            handle_option_py(message)
        elif current_state == 'handle_action_cpp':
            handle_option_cpp(message)
        elif current_state == 'show_lesson_pys_py':
            choose_option(message)
        elif current_state == 'show_lesson_pys_cpp':
            choose_option(message)
        elif current_state == 'handle_lesson_py':
            show_lesson_pys_py(message)
        elif current_state == 'handle_lesson_cpp':
            show_lesson_pys_cpp(message)
        elif current_state == 'handle_next':
            handle_action_py(message)  # Можно заменить на handle_action_cpp, в зависимости от текущего языка
        else:
            handle_start(message)
    else:
        handle_start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
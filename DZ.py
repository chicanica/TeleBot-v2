name = 'Вероника'
age = 20

# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    bot.send_message(chat_id, text=name)
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    message = 'Привет, меня зовут ' + name + '. Мне ' + str(age) + ' лет.'
    bot.send_message(chat_id, text=message)
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    name5 = name * 5
    bot.send_message(chat_id, text=name5)
# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    proc_answer_name = lambda message: bot.send_message(chat_id, f"Привет, {message.text}!")
    my_input(bot, chat_id, "Как тебя зовут?", proc_answer_name)

# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, 'Сколько вам лет?', dz5_ResponseHandler)

def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f'Ого, тебе уже {age_int}!')

# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    proc_answer = lambda message: bot.send_message(chat_id, f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", proc_answer)

# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, proc_answer):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, proc_answer)


def my_inputInt(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,text='Можно вводить только целое число цифрами от 0 до 9. \nПопробуйте еще раз')
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)

# -----------------------------------------------------------------------
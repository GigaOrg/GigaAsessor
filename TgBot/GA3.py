import openai
import telebot
import sqlite3

# set API key for OpenAI
openai.api_key = ""

# create bot object
bot = telebot.TeleBot(token='')

# set up database connection
conn = sqlite3.connect('GDB.db', check_same_thread=False)
c = conn.cursor()

# initialize state variable
is_feedback = False

# handle '/start' command
@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    # send start message
    bot.send_message(chat_id=message.chat.id, text="👋 Я GigaAsessor на основе GPT-3.5 и я помогаю улучшить запрос. Отправь мне свой запрос, для нейросети, я его оценю и дам советы по улучшению.")

# handle user messages
@bot.message_handler(func=lambda message: True)
def process_message(message: telebot.types.Message):
    global is_feedback
    if is_feedback:
        # handle feedback
        user_id = message.from_user.id
        feedback = int(message.text)
        c.execute("UPDATE GDB SET mark=? WHERE id=?", (feedback, user_id))
        conn.commit()
        bot.send_message(chat_id=message.chat.id, text="Thanks for your feedback!")
        is_feedback = False
    else:
        # handle query
        keyword = '//'
        prompt_prefix = "Понятен ли тебе мой промпт(не твой, а мой)? Дай ему оценку(моему промпту). Что мне надо в нём исправить(укажи так, чтобы было понятно тебе), чтобы тебе было понятно, что я хочу(не ты хочешь, а я), может надо что-то уточнить(для темы промпта)? Дай на это ответ по пунктам.\n//"
        input_text = message.text
        full_prompt = prompt_prefix + input_text
        # send prompt to OpenAI API
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=full_prompt,
            max_tokens=1024,
            temperature=0.5
        )
        output_text = response.choices[0].text
        markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
        markup.add(telebot.types.KeyboardButton('0'), telebot.types.KeyboardButton('1'), telebot.types.KeyboardButton('2'))
        bot.send_message(chat_id=message.chat.id, text=output_text, reply_markup=markup)
        user_id = message.from_user.id
        c.execute("INSERT INTO GDB (id, mark, text) VALUES (?, ?, ?)", (user_id, None, input_text))
        conn.commit()
        is_feedback = True

# handle user feedback
@bot.message_handler(func=lambda message: message.text in ['0', '1', '2'])
def process_feedback(message: telebot.types.Message):
    pass  # handled in the process_message function

bot.polling(none_stop=True)


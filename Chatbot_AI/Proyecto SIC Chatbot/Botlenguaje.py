#!pip install transformers
#!pip install pyTelegramBotAPI
#!pip install torch
#!pip install accelerate
#!pip install wikipedia-api

import telebot
import transformers
import torch
import time
import pickle

# Inicializar el bot de Telegram
bot = telebot.TeleBot('5946891713:AAEqH_b0lL4d26_HfX73EvV1Ny6fsh1jhNM')

# Cargar el modelo BERT pre-entrenado
model = transformers.BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = transformers.BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Cargar el diccionario de preguntas y respuestas
try:
    with open('qa_dict.pickle', 'rb') as handle:
        qa_dict = pickle.load(handle)
except:
    qa_dict = {}

# Manejar mensajes de pregunta de Telegram
@bot.message_handler(func=lambda message: True)
def answer_question(message):

    if message.text == '/start':
        bot.reply_to(message, 'Hola, mi nombre es Serina. Soy un modelo de reconocimiento del lenguaje natural.')
        bot.send_message(message.chat.id, 'Estos son ejemplos de algunas de las opciones que puedes realizar: \n /Cita_de_asesoria \n /help')
        bot.send_message(message.chat.id, 'Sabiendo esto, dime en que te puedo ayudar?')
        return
    
    if message.text == '/help':
        #muestra la lista de comandos
        bot.reply_to(message, 'Lista de comandos: \n /start \n /help \n /Comprar \n /Contacto')
        return
    
    if message.text == '/Cita_de_asesoria':
        bot.reply_to(message, 'En esta opcion podras realizar realizarme preguntas y te ayudaré a aclarar tus dudas')
        return

    if message.text == '/Contacto':
        bot.reply_to(message, 'Creado por: ')
        return
    
    # Extraer la pregunta del mensaje
    question = message.text

    # Buscar en el diccionario si la pregunta ya ha sido respondida anteriormente
    if question in qa_dict:
        answer = qa_dict[question]
    else:
        #extraer texto de un archivo de texto
        with open('texto.txt', 'r') as file:
            text = file.read().replace('\n', '')
            
        try:
            inputs = tokenizer.encode_plus(question, text, return_tensors='pt', add_special_tokens=True)
            output = model(**inputs)
        except Exception as e:
            bot.reply_to(message, 'Lo siento, ha ocurrido un error al procesar tu pregunta')
            return

        # Obtener la respuesta
        answer_start_scores, answer_end_scores = output[:2]
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        answer = tokenizer.decode(inputs['input_ids'][0][answer_start:answer_end],skip_special_tokens=True)

        #excepcion de errores
        if answer == '[CLS]' or answer == '[SEP]':
            answer = 'No se pudo encontrar una respuesta'
        

        # Almacenar la pregunta y la respuesta en el historial
        qa_dict[question] = answer
        with open("qa_dict.pickle", "wb") as f:
            pickle.dump(qa_dict, f)

    # Enviar la respuesta al usuario
    bot.reply_to(message, answer)


# Ejecutar el bot
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
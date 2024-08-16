#!pip install transformers
#!pip install pyTelegramBotAPI
#!pip install torch
#!pip install accelerate

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

def select_shipping_plan(message):
    if message.text == 'Envio gratis' or message.text == 'envio gratis':
        bot.reply_to(message, 'Escogiste el plan de envio gratis')
        return
    elif message.text == 'Envio rapido' or message.text == 'envio rapido':
        bot.reply_to(message, 'Escogiste el plan de envio rapido')
        return
    elif message.text == 'Envio express' or message.text == 'envio express':
        bot.reply_to(message, 'Escogiste el plan de envio express')
        return

def select_consult(message):
    if message.text == 'Consulta de horarios' or message.text == 'consulta de horarios':
        bot.reply_to(message, 'Escogiste la opcion de consultar horarios')
        bot.send_photo(message.chat.id, open('imagen1.jpg', 'rb'))
        return
    elif message.text == 'Consulta de paquetes' or message.text == 'consulta de paquetes':
        bot.reply_to(message, 'Escogiste la opcion de consultar productos')
        bot.send_message(message.chat.id, 'Enviame una imagen del producto que deseas consultar')
        # aqui entra el modelo de reconocimiento de imagenes
        return
    elif message.text == 'Destinos de envio' or message.text == 'destinos de envio':
        bot.reply_to(message, 'Escogiste la opcion de consultar destinos de envio')
        bot.send_message(message.chat.id, 'Estos son los destinos de envio:')
        bot.send_photo(message.chat.id, open('imagen2.jpg', 'rb'))
        return

def price(message):
    if message.text == 'Cotizacion de envio' or message.text == 'cotizacion de envio':
        bot.reply_to(message, 'Escogiste la opcion de cotizar envio')
        bot.send_message(message.chat.id, 'Existen 3 opciones de envio: \n \n * Envio gratis \n * Envio rapido \n * Envio express')
        bot.send_message(message.chat.id, 'La opcion gratis tiene un tiempo de entrega de 3 a 5 dias habiles, la opcion rapida tiene un tiempo de entrega de 2 a 3 dias habiles y la opcion express tiene un tiempo de entrega de 1 a 2 dias habiles')
        #espera 5 segundos
        time.sleep(20)
        bot.send_message(message.chat.id, 'Te gustaria escoger alguno de estos planes? y proceder con el envio? \n \n * Si \n * No')
    elif message.text == 'Personalizado' or message.text == 'personalizado':
        bot.reply_to(message, 'Escogiste el plan personalizado')
        return
    return


# Manejar mensajes de pregunta de Telegram
@bot.message_handler(func=lambda message: True)
def answer_question(message):

    if message.text == '/start':
        bot.reply_to(message, 'Hola, mi nombre es Serina. Soy un modelo de reconocimiento del lenguaje natural.')
        bot.send_message(message.chat.id, 'Estos son ejemplos de algunas de las opciones que puedes realizar: \n \n /Asesoria \n /Envio \n /Cotizacion \n')
        bot.send_message(message.chat.id, 'Tambien puedes consultar las opciones en el menu de la ezquina inferior izquierda o con el comando /help en todo momento')
        bot.send_message(message.chat.id, 'Sabiendo esto, dime en que te puedo ayudar?')
        return
    
    if message.text == '/Asesoria':
        bot.reply_to(message, 'Estoy aqui para orientarte escoge una opcion o dime en que te puedo ayudar: \n \n * Consulta de horarios \n * Consulta de paquetes \n * Destinos de envio')
        return
    else:
        select_consult(message)
    
    if message.text == '/Envio':
        bot.reply_to(message, 'Escoge un plan de envio: \n \n * Envio gratis \n * Envio rapido \n * Envio express')
        return
    else:
        select_shipping_plan(message)

    if message.text == '/Cotizacion':
        bot.reply_to(message, 'Escoge una opcion: \n \n * Cotizacion de envio \n * Cotizacion de producto')
        return
    else:
        price(message)
    

    #detener el bot
    if message.text == '/stop':
        bot.reply_to(message, 'Rutinas detenidas')
        return

    if message.text == '/help':
        #muestra la lista de comandos
        bot.reply_to(message, 'Lista de comandos: \n /start \n /help \n /Comprar \n /Contacto')
        return

    #reiiciar el bot
    if message.text == '/restart':
        bot.reply_to(message, 'Rutinas reiniciadas')
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
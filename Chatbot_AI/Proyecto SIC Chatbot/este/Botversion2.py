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
        bot.send_message(message, 'El plan de envio gratis tiene un costo de $0.00 y un tiempo de entrega de 3 a 5 dias habiles')
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')
        return
    elif message.text == 'Envio rapido' or message.text == 'envio rapido' or message.text == 'Envio rápido' or message.text == 'envio rápido':
        bot.reply_to(message, 'Escogiste el plan de envio rapido')
        bot.send_message(message, 'El plan de envio rapido tiene un costo de $5.00 y un tiempo de entrega de 1 a 2 dias habiles')
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')

        return
    elif message.text == 'Envio express' or message.text == 'envio express' or message.text == 'Envio expres' or message.text == 'envio expres':
        bot.reply_to(message, 'Escogiste el plan de envio express')
        bot.send_message(message, 'El plan de envio express tiene un costo de $10.00 y un tiempo de entrega de 1 dia habil')
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')

        return

def select_consult(message):
    if message.text == 'Consulta de horarios' or message.text == 'consulta de horarios' or message.text == 'Consulta de horario' or message.text == 'consulta de horario':
        bot.reply_to(message, 'Escogiste la opcion de consultar horarios')
        bot.send_message(message.chat.id, 'Estos son nuestros horarios de atencion:')
        bot.send_photo(message.chat.id, open('imagen1.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')
        return

    elif message.text == 'Consulta de productos' or message.text == 'consulta de productos' or message.text == 'Consulta de producto' or message.text == 'consulta de producto':
        bot.reply_to(message, 'Escogiste la opcion de consultar productos')
        bot.send_message(message.chat.id, 'Enviame una imagen del producto que deseas consultar')
        # aqui entra el modelo de reconocimiento de imagenes



        return
    elif message.text == 'Destinos de envio' or message.text == 'destinos de envio':
        bot.reply_to(message, 'Escogiste la opcion de consultar destinos de envio')
        bot.send_message(message.chat.id, 'Estos son los destinos de envio:')
        bot.send_photo(message.chat.id, open('imagen2.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')
        return

def price(message):
    if message.text == 'Cotizacion de envio' or message.text == 'cotizacion de envio' or message.text == 'Cotizacion de envío' or message.text == 'cotizacion de envío' or message.text == 'Cotización de envio' or message.text == 'cotización de envio' or message.text == 'Cotización de envío' or message.text == 'cotización de envío':
        bot.reply_to(message, 'Escogiste la opcion de cotizar envio')
        bot.reply_to(message, 'Para continuar necesito que me proporciones el peso del producto en lbs')
        bot.register_next_step_handler(message, process_peso)
    elif message.text == 'Cotizacion de producto' or message.text == 'cotizacion de producto' or message.text == 'Cotización de producto' or message.text == 'cotización de producto':
        bot.reply_to(message, 'Escogiste la opcion de cotizar producto')
        bot.reply_to(message, 'Por favor, envía el ID del producto o una foto del producto')
        bot.register_next_step_handler(message, process_producto)

import os

class Producto:
    def __init__(self, file_id, precio):
        self.file_id = file_id
        self.precio = precio

def buscar_producto(file_id):
    path_img = os.path.join('bdproductos', file_id + '.jpg')
    path_txt = os.path.join('bdproductos', file_id + '.txt')
    if os.path.exists(path_img) and os.path.exists(path_txt):
        with open(path_txt, 'rb') as f:
            precio = f.read()
        return Producto(file_id, precio)
    return None

def process_producto(message):
    if message.photo:
        file_id = message.photo[-1].file_id
        producto = buscar_producto(file_id)
        if producto:
            bot.send_message(message.chat.id, f'El precio del producto es {producto.precio}')
        else:
            bot.send_message(message.chat.id, 'Producto no encontrado')
    elif message.text:
        producto = buscar_producto(message.text)
        if producto:
            bot.send_message(message.chat.id, f'El precio del producto es {producto.precio}')
        else:
            bot.send_message(message.chat.id, 'Producto no encontrado')



def process_peso(message):
    try:
        peso = float(message.text)
        if peso >= 0 and peso <= 2:
            bot.send_message(message.chat.id, 'El precio de envío para ese peso es $5')
        elif peso > 2 and peso <= 5:
            bot.send_message(message.chat.id, 'El precio de envío para ese peso es $10')
        elif peso > 5:
            bot.send_message(message.chat.id, 'El precio de envío para ese peso es $15')
        else:
            bot.send_message(message.chat.id, 'Peso invalido')
        bot.reply_to(message, "¿Desea seguir cotizando?")
        bot.register_next_step_handler(message, process_continue)
    except ValueError:
        bot.send_message(message.chat.id, 'Peso invalido')

def process_continue(message):
    if message.text.lower() == "si":
        bot.reply_to(message, "¡Genial! Por favor proporciona el peso del producto en lbs")
        bot.register_next_step_handler(message, process_peso)
    elif message.text.lower() == "no":
        bot.reply_to(message, "¡De acuerdo, gracias por usar nuestro servicio de cotización!")
        bot.send_message(message.chat.id, 'Presiona aqui para volver al menu principal: \n \n /start')

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
    
    if message.text == '/asesoria':
        bot.reply_to(message, 'Estoy aqui para orientarte escoge una opcion o dime en que te puedo ayudar: \n \n * Consulta de horarios \n * Consulta de productos \n * Destinos de envio')
        return
    else:
        select_consult(message)
    
    if message.text == '/envio':
        bot.reply_to(message, 'Escoge un plan de envio: \n \n * Envio gratis \n * Envio rapido \n * Envio express')
        return
    else:
        select_shipping_plan(message)

    if message.text == '/cotizacion':
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
        bot.reply_to(message, 'Lista de comandos: \n \n /start \n /Asesoria \n /Envio \n /Cotizacion \n /stop \n /restart \n /help')
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
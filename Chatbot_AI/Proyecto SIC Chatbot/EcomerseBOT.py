#pip3 install telethon
#execute this in terminal to install telethon


from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

import apiData

client = TelegramClient('session', apiData.api_id, apiData.api_hash)

@client.on(events.NewMessage(chats=apiData.chatName))
async def my_event_handler(event):
    respuesta = 'Hola'
    print(event.text)
    await client.send_message(apiData.chatName, respuesta)

client.start()
client.run_until_disconnected()


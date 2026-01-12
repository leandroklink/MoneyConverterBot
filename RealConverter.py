import telebot
import requests
<<<<<<< HEAD
import os

CHAVE_API = os.getenv("TELEGRAM_BOT_TOKEN")
usuarios = {}

bot = telebot.TeleBot(CHAVE_API)
siglas = ["BRL", "USD", "EUR", "JPY", "GBP", "CAD", "CHF", "AUD", "CNY"]


def calc_cotacao(origem, moeda):
    try:
        link =  f"https://economia.awesomeapi.com.br/json/last/{origem}-{moeda}"
        resposta = requests.get(link, timeout=5).json()
        return float(resposta[f"{origem}{moeda}"]["ask"])
    except Exception:
        return None


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    usuarios[chat_id] = {
        "etapa": 1,
        "moeda_origem": None,
        "moeda_destino": None,
        "cotacao": None
    }

    texto = """
Olá, eu sou o MoneyConverter! 🚀
um bot que realiza conversão de moedas com base no valor que você me informar e as moedas que deseja converter.

Escolha a moeda de origem 📍

/BRL Real Brasileiro (R$) 
/USD Dólar Americano (US$)
/EUR Euro
/JPY Iene Japonês
/GBP Libra Esterlina (£)
/CAD Dólar Canadense (C$)
/CHF Franco Suíço (Fr)
/AUD Dólar Australiano (A$)
/CNY Yuan Chinês

(Digitar qualquer outra coisa não vai funcionar)"""

    bot.send_message(chat_id, texto)


@bot.message_handler(func=lambda message: True)
def conversation(message):
    chat_id = message.chat.id

    if chat_id not in usuarios:
        bot.send_message(chat_id, "Digite /start para iniciar! 😀")
        return
    
    etapa = usuarios[chat_id]["etapa"]
    if etapa ==1:
        moeda = message.text.replace("/", "").upper()[:3]

        if moeda not in siglas:
            bot.send_message(chat_id, "Mensagem inválida, pressione /start para tentar novamente.")
            return
        
        usuarios[chat_id]["moeda_origem"] = moeda
        usuarios[chat_id]["etapa"] = 2

        texto = """
Escolha a moeda de Destino 📌

/BRL Real Brasileiro (R$)
/USD Dólar Americano (US$)
/EUR Euro
/JPY Iene Japonês
/GBP Libra Esterlina (£)
/CAD Dólar Canadense (C$)
/CHF Franco Suíço (Fr)
/AUD Dólar Australiano (A$)
/CNY Yuan Chinês
(Digitar qualquer outra coisa não vai funcionar)"""

        bot.send_message(chat_id, texto)

    elif etapa == 2: 
        moeda = message.text.replace("/", "").upper()[:3]


        if moeda not in siglas:
            bot.send_message(chat_id, f"Mensagem inválida, pressione /start para tentar novamente.")
            return
        
        origem = usuarios[chat_id]["moeda_origem"]
        usuarios[chat_id]["moeda_destino"] = moeda
        
        cotacao = calc_cotacao(origem, moeda)

        if cotacao is None:
            bot.send_message(chat_id, "Erro ao obter cotação. Tente novamente mais tarde.")
            del usuarios[chat_id]
            return
        usuarios[chat_id]["cotacao"] = cotacao
        

        texto = f"Digite o valor que deseja converter de {origem} para {moeda}."
        bot.send_message(message.chat.id, texto)
        usuarios[chat_id]["etapa"] = 3
=======


CHAVE_API = "insira a chave aqui"

bot = telebot.TeleBot(CHAVE_API)
siglas = ["BRL", "USD", "EUR", "JPY", "GBP", "CAD", "CHF", "AUD", "CNY"]
etapa = 0
valor = 0.0
calculo = 0.0
def cotacao(moedaOrigem, moedaDestino):
    link =  f"https://economia.awesomeapi.com.br/json/last/{moedaOrigem}-{moedaDestino}"
    requisicao = requests.get(link)
    resposta = requisicao.json()
    cotacao = resposta[f"{moedaOrigem}{moedaDestino}"]["ask"]
    return cotacao


@bot.message_handler(commands=['start'])
def moeda1(message):
    global etapa
    texto = """
    Escolha a moeda de origem 📍
    /BRL Real Brasileiro (R$) 
    /USD Dólar Americano (US$)
    /EUR Euro
    /JPY Iene Japonês
    /GBP Libra Esterlina (£)
    /CAD Dólar Canadense (C$)
    /CHF Franco Suíço (Fr)
    /AUD Dólar Australiano (A$)
    /CNY Yuan Chinês
    (Digitar qualquer outra coisa não vai funcionar)"""
    etapa = 1
    bot.send_message(message.chat.id, texto)


@bot.message_handler(func=lambda message: True)
def getMoeda1(message):
    global etapa, moedaOrigem, moedaDestino, valorCotacao, valor
    if etapa == 1:
        moedaOrigem = message.text[1:4]
        if moedaOrigem not in siglas:
            bot.send_message(message.chat.id, "Mensagem inválida, pressione /start para tentar novamente")
            return
        texto = """
        Escolha a moeda de Destino 📌
        /BRL Real Brasileiro (R$)
        /USD Dólar Americano (US$)
        /EUR Euro
        /JPY Iene Japonês
        /GBP Libra Esterlina (£)
        /CAD Dólar Canadense (C$)
        /CHF Franco Suíço (Fr)
        /AUD Dólar Australiano (A$)
        /CNY Yuan Chinês
        (Digitar qualquer outra coisa não vai funcionar)"""
        etapa = 2
        bot.send_message(message.chat.id, texto)
    elif etapa == 2: 
        moedaDestino = message.text[1:4]
        etapa = 3
        if moedaDestino not in siglas:
            bot.send_message(message.chat.id, f"Mensagem inválida, pressione /start para tentar novamente")
            return
        valorCotacao = float(cotacao(moedaOrigem, moedaDestino))
        texto = f"Digite o valor que deseja converter de {moedaOrigem} para {moedaDestino}"
        bot.send_message(message.chat.id, texto)
>>>>>>> 6065e96bc80a1e14ef66cb40af259ea9e90fd1d5

    elif etapa == 3:
        try:
            valor = float(message.text)
<<<<<<< HEAD
            cotacao = usuarios[chat_id]["cotacao"]
            resultado = valor * cotacao
            texto = f"O valor convertido é {resultado:.2f}, pressione /start para realizar uma nova conversão."
            bot.send_message(chat_id, texto)
            del usuarios[chat_id]

        except ValueError:
            bot.send_message(chat_id, "Digite um valor inteiro ou decimal! tente novamente com /start.")


bot.polling(none_stop=True)
=======
            bot.send_message(message.chat.id, calcularcotacao(valor))
        except ValueError:
            bot.send_message(message.chat.id, "Digite um valor inteiro ou decimal! tente novamente com /start")

def calcularcotacao(valor):

    calculo = valor * valorCotacao
    texto = f"O valor convertido é {calculo:.2f}, pressione /start para retornar"
    return texto

bot.polling()
>>>>>>> 6065e96bc80a1e14ef66cb40af259ea9e90fd1d5

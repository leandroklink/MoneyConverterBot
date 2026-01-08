import telebot
import requests


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

    elif etapa == 3:
        try:
            valor = float(message.text)
            bot.send_message(message.chat.id, calcularcotacao(valor))
        except ValueError:
            bot.send_message(message.chat.id, "Digite um valor inteiro ou decimal! tente novamente com /start")

def calcularcotacao(valor):

    calculo = valor * valorCotacao
    texto = f"O valor convertido é {calculo:.2f}, pressione /start para retornar"
    return texto

bot.polling()
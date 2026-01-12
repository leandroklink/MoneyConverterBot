import telebot
import requests
import os

CHAVE_API = os.getenv("TELEGRAM_BOT_TOKEN")
usuarios = {}

bot = telebot.TeleBot(CHAVE_API)
siglas = ["BRL", "USD", "EUR", "JPY", "GBP", "CAD", "CHF", "AUD", "CNY"]


def calc_cotacao(origem, moeda):
    try:
        link = f"https://economia.awesomeapi.com.br/json/last/{origem}-{moeda}"
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
Escolha a moeda de origem 📍

/BRL Real Brasileiro
/USD Dólar Americano
/EUR Euro
/JPY Iene Japonês
/GBP Libra Esterlina
/CAD Dólar Canadense
/CHF Franco Suíço
/AUD Dólar Australiano
/CNY Yuan Chinês
"""
    bot.send_message(chat_id, texto)


@bot.message_handler(func=lambda message: True)
def conversation(message):
    chat_id = message.chat.id

    if chat_id not in usuarios:
        bot.send_message(chat_id, "Digite /start para iniciar 😀")
        return

    etapa = usuarios[chat_id]["etapa"]

    if etapa == 1:
        moeda = message.text.replace("/", "").upper()[:3]

        if moeda not in siglas:
            bot.send_message(chat_id, "Moeda inválida. Use /start.")
            return

        usuarios[chat_id]["moeda_origem"] = moeda
        usuarios[chat_id]["etapa"] = 2

        bot.send_message(chat_id, "Agora escolha a moeda de destino.")

    elif etapa == 2:
        moeda = message.text.replace("/", "").upper()[:3]

        if moeda not in siglas:
            bot.send_message(chat_id, "Moeda inválida. Use /start.")
            return

        origem = usuarios[chat_id]["moeda_origem"]
        cotacao = calc_cotacao(origem, moeda)

        if cotacao is None:
            bot.send_message(chat_id, "Erro ao obter cotação.")
            del usuarios[chat_id]
            return

        usuarios[chat_id]["moeda_destino"] = moeda
        usuarios[chat_id]["cotacao"] = cotacao
        usuarios[chat_id]["etapa"] = 3

        bot.send_message(chat_id, f"Digite o valor em {origem}.")

    elif etapa == 3:
        try:
            valor = float(message.text)
            resultado = valor * usuarios[chat_id]["cotacao"]

            bot.send_message(
                chat_id,
                f"Valor convertido: {resultado:.2f}\nDigite /start para nova conversão."
            )

            del usuarios[chat_id]

        except ValueError:
            bot.send_message(chat_id, "Digite um número válido.")


bot.polling(none_stop=True)

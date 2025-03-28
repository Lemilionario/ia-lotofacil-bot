
import telebot
import requests
import os

TOKEN_BOT = os.getenv("TOKEN_BOT")
TOKEN_API = os.getenv("TOKEN_API", "lotofacil_mestre_2025")
URL_API = os.getenv("URL_API", "https://ia-lotofacil-api.onrender.com")

bot = telebot.TeleBot(TOKEN_BOT)

def formatar_apostas(apostas):
    msg = "🔮 *Apostas geradas pela IA Central da Lotofácil:*\n\n"
    for i, aposta in enumerate(apostas, 1):
        numeros = " ".join(f"{dez:02d}" for dez in sorted(aposta))
        msg += f"• Aposta {i}: `{numeros}`\n"
    return msg

@bot.message_handler(commands=['start', 'ajuda'])
def boas_vindas(message):
    comandos = "/gerar - Gerar apostas oficiais da IA\n"
    comandos += "/bonus - Aposta bônus fidedigna\n"
    comandos += "/status - Ver status da IA\n"
    comandos += "/estrutura - Ver estrutura ativa da IA\n"
    comandos += "/analisar 01 02 ... - Analisar dezenas\n"
    comandos += "/validar 01 02 ... - Validar aposta\n"
    comandos += "/ultimos - Ver últimos resultados\n"
    comandos += "/resumo - Ver análise atual da IA\n"
    bot.send_message(message.chat.id, f"👋 Bem-vindo, Mestre. Comandos disponíveis:\n\n{comandos}", parse_mode="Markdown")

@bot.message_handler(commands=['gerar'])
def gerar_apostas(message):
    try:
        r = requests.get(f"{URL_API}/gerar?token={TOKEN_API}")
        if r.status_code == 200:
            apostas = r.json().get("apostas", [])
            msg = formatar_apostas(apostas)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ Erro ao consultar a IA Central.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro interno: {e}")

@bot.message_handler(commands=['bonus'])
def gerar_bonus(message):
    try:
        r = requests.get(f"{URL_API}/bonus?token={TOKEN_API}")
        if r.status_code == 200:
            aposta = r.json().get("aposta", [])
            numeros = " ".join(f"{dez:02d}" for dez in sorted(aposta))
            bot.send_message(message.chat.id, f"🎯 *Aposta Bônus:* `{numeros}`", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ Erro ao gerar a aposta bônus.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro interno: {e}")

@bot.message_handler(commands=['status'])
def status(message):
    bot.send_message(message.chat.id, "📡 IA Central está *ativa* e conectada ao núcleo estatístico da Lotofácil.", parse_mode="Markdown")

@bot.message_handler(commands=['estrutura'])
def estrutura(message):
    bot.send_message(message.chat.id, "🧠 Estrutura Ativa:\n- Algoritmo Genético\n- Cadeia de Markov 2ª Ordem\n- Clusters Ocultos\n- Score ≥ 6\n- Zonas Quentes\n- Autoaprendizado dinâmico", parse_mode="Markdown")

@bot.message_handler(commands=['ultimos', 'resumo'])
def consultar_info(message):
    endpoint = message.text.strip("/").lower()
    try:
        r = requests.get(f"{URL_API}/{endpoint}?token={TOKEN_API}")
        if r.status_code == 200:
            bot.send_message(message.chat.id, r.text)
        else:
            bot.send_message(message.chat.id, f"⚠️ Erro ao consultar /{endpoint}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro interno: {e}")

@bot.message_handler(commands=['analisar', 'validar'])
def analisar_aposta(message):
    dezenas = message.text.split()[1:]
    if len(dezenas) != 15:
        bot.send_message(message.chat.id, "❗ Envie exatamente 15 dezenas. Exemplo:\n/analisar 01 02 ...", parse_mode="Markdown")
        return
    try:
        endpoint = message.text.split()[0].strip("/").lower()
        r = requests.post(f"{URL_API}/{endpoint}?token={TOKEN_API}", json={"dezenas": [int(d) for d in dezenas]})
        if r.status_code == 200:
            bot.send_message(message.chat.id, str(r.json()))
        else:
            bot.send_message(message.chat.id, f"⚠️ Erro ao consultar /{endpoint}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro interno: {e}")

bot.polling()

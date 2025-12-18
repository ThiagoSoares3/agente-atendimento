from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)  # <<< ISSO RESOLVE O ERRO DO NAVEGADOR

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Agente multiempresas rodando"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    empresa = data.get("empresa", "geral")
    mensagem = data.get("mensagem", "")

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Você é um agente de atendimento educado e claro da empresa {empresa}."
            },
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )

    return jsonify({
        "resposta": resposta.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




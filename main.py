from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensagem = data.get("mensagem", "")

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um agente de atendimento educado."},
            {"role": "user", "content": mensagem}
        ]
    )

    return jsonify({
        "resposta": resposta.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




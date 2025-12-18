from flask import Flask, request, jsonify
from openai import OpenAI
from empresas import EMPRESAS

app = Flask(__name__)

@app.route("/")
def home():
    return "Agente multiempresas rodando"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    empresa_id = data.get("empresa")
    mensagem = data.get("mensagem", "")

    if empresa_id not in EMPRESAS:
        return jsonify({"erro": "Empresa não encontrada"}), 404

    empresa = EMPRESAS[empresa_id]

    client = OpenAI(api_key=empresa["api_key"])

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": empresa["prompt"]},
            {"role": "user", "content": mensagem}
        ]
    )

    return jsonify({
        "empresa": empresa["nome"],
        "resposta": resposta.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



from flask import Flask, request, jsonify
import os
from openai import OpenAI

# Inicializa o app Flask
app = Flask(__name__)

# Inicializa o cliente OpenAI usando variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== DADOS DAS EMPRESAS (SIMULA MULTIEMPRESAS) =====
EMPRESAS = {
    "clinica": {
        "nome": "Clínica Saúde Total",
        "prompt": "Você é um atendente educado e profissional de uma clínica médica."
    },
    "pizzaria": {
        "nome": "Pizzaria do Bairro",
        "prompt": "Você é um atendente simpático e direto de uma pizzaria."
    }
}

# ===== ENDPOINT PRINCIPAL =====
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    empresa_id = data.get("empresa", "clinica")
    mensagem = data.get("mensagem", "")

    empresa = EMPRESAS.get(empresa_id)

    if not empresa:
        return jsonify({"erro": "Empresa não encontrada"}), 404

    # Chamada correta usando o SDK NOVO da OpenAI
    resposta = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": empresa["prompt"]},
            {"role": "user", "content": mensagem}
        ]
    )

    return jsonify({
        "empresa": empresa["nome"],
        "resposta": resposta.output_text
    })

# ===== START LOCAL (Render ignora isso, mas é correto manter) =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.models.list()
    print("CHAVE ATIVA ✅")
    print("Modelos disponíveis:", [m.id for m in response.data][:5])
except Exception as e:
    print("ERRO ❌")
    print(e)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(
    title="Casa de Sucos API",
    description="API para consultar frutas e cadastrar sucos.",
    version="1.0.0"
)

URL_FRUITYVICE = "https://www.fruityvice.com/api/fruit/"

# Banco de dados temporário em memória
sucos = []
proximo_id = 1


# Estrutura dos dados recebidos no cadastro
class SucoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    frutas: list[str] = Field(min_length=1)
    tem_gosto_de: str = Field(min_length=1)


# Consulta uma fruta na API Fruityvice
def consultar_fruta(nome: str):
    nome = nome.strip()

    if not nome:
        raise HTTPException(
            status_code=400,
            detail="Informe o nome de uma fruta."
        )

    try:
        resposta = requests.get(
            f"{URL_FRUITYVICE}{nome}",
            timeout=10
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar à API de frutas."
        )

    if resposta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"A fruta '{nome}' não foi encontrada."
        )

    if resposta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar a API Fruityvice."
        )

    try:
        dados = resposta.json()

        return {
            "nome": dados["name"],
            "calorias": float(dados["nutritions"]["calories"]),
            "acucar": float(dados["nutritions"]["sugar"])
        }

    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="A API Fruityvice retornou dados inválidos."
        )


# Calcula os nutrientes considerando 100 g de cada fruta
def calcular_nutrientes(frutas: list[str]):
    total_calorias = 0
    total_acucar = 0
    nomes_frutas = []

    for nome in frutas:
        fruta = consultar_fruta(nome)

        nomes_frutas.append(fruta["nome"])
        total_calorias += fruta["calorias"]
        total_acucar += fruta["acucar"]

    return {
        "frutas": nomes_frutas,
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }


# 1. GET /frutas/{nome}
@app.get("/frutas/{nome}", tags=["Frutas"])
def obter_fruta(nome: str):
    fruta = consultar_fruta(nome)

    return {
        "nome": fruta["nome"],
        "calorias": fruta["calorias"],
        "acucar": fruta["acucar"]
    }


# 2. POST /sucos
@app.post("/sucos", status_code=201, tags=["Sucos"])
def cadastrar_suco(suco: SucoEntrada):
    global proximo_id

    nutrientes = calcular_nutrientes(suco.frutas)

    novo_suco = {
        "id": proximo_id,
        "nome": suco.nome.strip(),
        "frutas": nutrientes["frutas"],
        "tem_gosto_de": suco.tem_gosto_de.strip(),
        "total_calorias": nutrientes["total_calorias"],
        "total_acucar": nutrientes["total_acucar"]
    }

    sucos.append(novo_suco)
    proximo_id += 1

    return novo_suco


# 3. GET /sucos
@app.get("/sucos", tags=["Sucos"])
def listar_sucos():
    return sucos


# 4. PUT /sucos/{id} - desafio bônus
@app.put("/sucos/{id}", tags=["Sucos"])
def atualizar_suco(id: int, suco: SucoEntrada):
    for item in sucos:
        if item["id"] == id:
            # Calcula antes de alterar o cadastro
            nutrientes = calcular_nutrientes(suco.frutas)

            item["nome"] = suco.nome.strip()
            item["frutas"] = nutrientes["frutas"]
            item["tem_gosto_de"] = suco.tem_gosto_de.strip()
            item["total_calorias"] = nutrientes["total_calorias"]
            item["total_acucar"] = nutrientes["total_acucar"]

            return item

    raise HTTPException(
        status_code=404,
        detail=f"Suco com ID {id} não encontrado."
    )

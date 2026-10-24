# Casa de Sucos API

API desenvolvida em Python com FastAPI para consultar informações nutricionais de frutas e cadastrar sucos utilizando a API pública [Fruityvice](https://www.fruityvice.com/api/fruit/).

## Funcionalidades

- `GET /frutas/{nome}` — consulta nome, calorias e açúcar de uma fruta.
- `POST /sucos` — cadastra sucos e calcula os valores nutricionais.
- `GET /sucos` — lista os sucos cadastrados.
- `PUT /sucos/{id}` — atualiza um suco e recalcula seus valores nutricionais.

Os cálculos consideram 100 g de cada fruta informada. Os valores são obtidos da API Fruityvice.

## Tecnologias utilizadas

- Python
- FastAPI
- Requests
- Uvicorn
- Fruityvice API

## Como executar

1. Clone ou baixe este repositório.
2. Crie e ative um ambiente virtual.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a aplicação:

   ```bash
   python -m uvicorn main:app --reload
   ```

5. Acesse a documentação interativa:

   http://127.0.0.1:8000/docs

## Armazenamento

Os sucos são armazenados temporariamente em memória. Os registros são perdidos quando a aplicação é reiniciada.

## Testes

As evidências dos testes realizados no Swagger serão disponibilizadas na pasta `evidencias/`.

## Objetivo acadêmico

Atividade prática para aplicar conceitos de criação e consumo de APIs, endpoints, métodos HTTP, JSON, integração com serviços externos e tratamento de erros.

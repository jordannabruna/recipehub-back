import uvicorn
from fastapi import FastAPI

# 1. Cria a instância principal da nossa aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

# 2. Criando o primeiro endpoint
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do nosso projeto!"}

# 3. Endpoint com Parâmetro de Rota (Path Parameter)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# 4. Código para rodar o servidor
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
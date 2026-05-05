from fastapi import FastAPI

app = FastAPI(title="Serviço de Membros")

members = [
    {"id": 101, "nome": "João Pedro", "tipo": "professor"},
    {"id": 102, "nome": "Maria Eduarda", "tipo": "estudante"},
    {"id": 103, "nome": "Mateus Filipe", "tipo": "estudante"},
    {"id": 104, "nome": "Bruna Geovana", "tipo": "estudante"}
]

@app.get("/")
def home():
    return {"status": "Serviço de Membros Online", "endpoint": "/members"}

@app.get("/members")
def get_members():
    return members
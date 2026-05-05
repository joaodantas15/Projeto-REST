from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(
    title="LibLink API Gateway",
    description="Orquestrador Central com HATEOAS e Microserviços",
    version="1.0.0"
)

# Habilita CORS para permitir que o Cliente Web acesse o Gateway - deu bo no meu pc, mas usei extensão do chrome
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs internas - Apontando para os terminais dos microserviços
BOOKS_SERVICE = "http://127.0.0.1:8001"
MEMBERS_SERVICE = "http://127.0.0.1:8002"

@app.get("/", tags=["Diagnóstico"])
def root():
    """Endpoint raiz para validação rápida do Gateway."""
    return {
        "status": "API Gateway Operacional",
        "links": [
            {"rel": "dashboard", "href": "/gateway/dashboard", "method": "GET"},
            {"rel": "cliente_web", "href": "/client", "method": "GET"}
        ]
    }

@app.get("/gateway/dashboard", tags=["Orquestração"])
def get_dashboard():
    """Orquestra dados de múltiplos serviços para compor uma visão unificada."""
    try:
        # Chamadas síncronas para os microserviços internos
        res_books = requests.get(f"{BOOKS_SERVICE}/books", timeout=2)
        res_members = requests.get(f"{MEMBERS_SERVICE}/members", timeout=2)
        
        # Validação de disponibilidade dos serviços
        if res_books.status_code != 200 or res_members.status_code != 200:
            raise Exception("Erro na comunicação com serviços internos")

        return {
            "estatisticas": {
                "total_livros": len(res_books.json()),
                "total_membros": len(res_members.json())
            },
            "links": [
                {"rel": "self", "href": "/gateway/dashboard", "method": "GET"},
                {"rel": "listar_livros", "href": "/gateway/livros", "method": "GET"}
            ]
        }
    except Exception as e:
        return {"erro": "Arquitetura interna indisponível", "detalhes": str(e)}

@app.get("/gateway/livros", tags=["HATEOAS"])
def list_books_gateway():
    """Lista livros injetando links dinâmicos baseados no estado atual (Nível 3 REST)[cite: 1]."""
    try:
        response = requests.get(f"{BOOKS_SERVICE}/books")
        books = response.json()
        
        for book in books:
            # Cada recurso recebe seu próprio conjunto de links de navegação
            book["links"] = [
                {"rel": "self", "href": f"/gateway/livros/{book['id']}", "method": "GET"}
            ]
            
            # Lógica HATEOAS: O estado dita a ação permitida
            if book["status"] == "disponivel":
                book["links"].append({
                    "rel": "alugar", 
                    "href": f"/gateway/alugar/{book['id']}", 
                    "method": "POST"
                })
            else:
                book["links"].append({
                    "rel": "devolver", 
                    "href": f"/gateway/devolver/{book['id']}", 
                    "method": "POST"
                })
                
        return {"livros": books}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao acessar serviço de livros: {str(e)}")

@app.post("/gateway/alugar/{book_id}", tags=["Ações"])
def alugar_livro(book_id: int):
    """Orquestra a mudança de estado para 'emprestado' no serviço remoto[cite: 1]."""
    url = f"{BOOKS_SERVICE}/books/{book_id}/status?status=emprestado"
    response = requests.patch(url)
    return {"status": "sucesso", "dados": response.json()}

@app.post("/gateway/devolver/{book_id}", tags=["Ações"])
def devolver_livro(book_id: int):
    """Orquestra a mudança de estado para 'disponivel' no serviço remoto[cite: 1]."""
    url = f"{BOOKS_SERVICE}/books/{book_id}/status?status=disponivel"
    response = requests.patch(url)
    return {"status": "sucesso", "dados": response.json()}

@app.get("/client", response_class=HTMLResponse, tags=["Interface"])
def get_client():
    """Serve a interface administrativa do Cliente Web."""
    try:
        with open("web_client/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h3>Erro: Arquivo web_client/index.html não encontrado.</h3>"

@app.get("/gateway/membros", tags=["Orquestração"])
def list_members_gateway():
    """Busca a lista de membros no microserviço de membros e retorna ao cliente."""
    try:
        response = requests.get(f"{MEMBERS_SERVICE}/members", timeout=2)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail="Serviço de membros indisponível")
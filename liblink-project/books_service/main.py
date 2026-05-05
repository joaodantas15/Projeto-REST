from fastapi import FastAPI, HTTPException

app = FastAPI(title="Serviço de Livros")

books = [
    {"id": 1, "titulo": "Sistemas Distribuídos", "autor": "Tanenbaum", "status": "disponivel"},
    {"id": 2, "titulo": "Clean Code", "autor": "Robert Martin", "status": "emprestado"},
    {"id": 3, "titulo": "O Senhor dos Anéis - A Sociedade do Anel", "autor": "J.R.R Tolkien", "status": "disponivel"},
    {"id": 4, "titulo": "O Senhor dos Anéis - As Duas Torres", "autor": "J.R.R Tolkien", "status": "disponivel"},
    {"id": 5, "titulo": "O Senhor dos Anéis - O Retorno do Rei", "autor": "J.R.R Tolkien", "status": "emprestado"},
    {"id": 6, "titulo": "O Hobbit", "autor": "J.R.R Tolkien", "status": "disponivel"},
    {"id": 7, "titulo": "Diário de um banana", "autor": "Jeff Kinney", "status": "disponivel"},
    {"id": 8, "titulo": "Cartas de um diabo a seu aprendiz", "autor": "CS Lewis", "status": "disponivel"}
]

@app.get("/")
def home():
    return {"status": "Serviço de Livros Online"}

@app.get("/books")
def get_books():
    return books

@app.patch("/books/{book_id}/status")
def update_book_status(book_id: int, status: str):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    book["status"] = status
    return book
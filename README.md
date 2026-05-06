# LibLink API - Sistema de Biblioteca Distribuído

Projeto desenvolvido para a disciplina de Sistemas Distribuídos, demonstrando uma arquitetura de microserviços com API Gateway, Orquestração e HATEOAS.

## 🚀 Arquitetura do Sistema
O sistema é composto por 3 serviços independentes:
1. **API Gateway (Porta 8000):** Orquestrador central que implementa HATEOAS e serve o cliente web.
2. **Books Service (Porta 8001):** Gerenciamento do acervo e persistência de status dos livros.
3. **Members Service (Porta 8002):** Gerenciamento de membros ativos.

## 🛠️ Tecnologias Utilizadas
* Python 3.12 + FastAPI
* Uvicorn (Servidor ASGI)
* Requests (Comunicação inter-serviços)
* Tailwind CSS (Interface Visual)

## 📖 Como Rodar
1. Ative o ambiente virtual: `source venv/bin/activate`
2. Inicie os três terminais com os comandos de `uvicorn` detalhados no projeto.
3. Acesse `/client` na porta 8000 para a interface visual.
4. Acesse `/docs` na porta 8000 para a documentação Swagger.

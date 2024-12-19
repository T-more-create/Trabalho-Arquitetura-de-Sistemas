from typing import List

from fastapi import FastAPI, Form, HTTPException, Query

app = FastAPI()

# Armazenamento em memória para tarefas
tarefas = []

@app.get("/")
async def default():
    print("hello, world")
    return {"message": "Hello, World!"}

@app.get("/tarefas")
async def listar_tarefas():
    """
    Recuperar a lista de tarefas.
    """
    return {
        "status": "sucesso",
        "mensagem": "Tarefas recuperadas com sucesso.",
        "dados": tarefas
    }

@app.get("/tarefas/{tarefa_id}")
async def obter_tarefa_por_id(tarefa_id: int):
    """
    Recuperar uma tarefa pelo ID.
    """
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return {
                "status": "sucesso",
                "mensagem": "Tarefa recuperada com sucesso.",
                "dados": tarefa
            }
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.get("/tarefas_pesquisa")
async def pesquisar_tarefas_por_titulo(titulo: str = Query(...)):
    """
    Pesquisar tarefas pelo título.
    """
    tarefas_correspondentes = [tarefa for tarefa in tarefas if titulo.lower() in tarefa["titulo"].lower()]
    if tarefas_correspondentes:
        return {
            "status": "sucesso",
            "mensagem": "Tarefas recuperadas com sucesso.",
            "dados": tarefas_correspondentes
        }
    raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada com o título fornecido.")

@app.post("/tarefas")
async def criar_tarefa(
    titulo: str = Form(...),
    descricao: str = Form(...),
    status: str = Form(...)
):
    """
    Adicionar uma nova tarefa à lista.
    """
    tarefa = {
        "id": len(tarefas) + 1,  # Gerar um ID simples
        "titulo": titulo,
        "descricao": descricao,
        "status": status
    }
    tarefas.append(tarefa)
    return {
        "status": "sucesso",
        "mensagem": "Tarefa adicionada com sucesso.",
        "dados": tarefa
    }

@app.put("/tarefas/{tarefa_id}")
async def atualizar_tarefa(
    tarefa_id: int,
    titulo: str = Form(...),
    descricao: str = Form(...),
    status: str = Form(...)
):
    """
    Atualizar os detalhes de uma tarefa pelo ID.
    """
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa.update({"titulo": titulo, "descricao": descricao, "status": status})
            return {
                "status": "sucesso",
                "mensagem": "Tarefa atualizada com sucesso.",
                "dados": tarefa
            }
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete("/tarefas/{tarefa_id}")
async def deletar_tarefa(tarefa_id: int):
    """
    Deletar uma tarefa pelo ID.
    """
    for index, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            tarefa_deletada = tarefas.pop(index)
            return {
                "status": "sucesso",
                "mensagem": "Tarefa deletada com sucesso.",
                "dados": tarefa_deletada
            }
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

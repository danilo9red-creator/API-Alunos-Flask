from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, 'alunos.json')

def ler_dados():

    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
  
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


@app.route('/alunos', methods=['GET'])
def listar_alunos():
  
    dados = ler_dados()
    return jsonify(dados)


@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def buscar_aluno(aluno_id):

    dados = ler_dados()
    for aluno in dados:
        if aluno['id'] == aluno_id:
            return jsonify(aluno)
    return jsonify({'erro': 'Aluno não encontrado'}), 404

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
  
    dados = ler_dados()
    novo_aluno = request.json
    
    for aluno in dados:
        if aluno['id'] == novo_aluno['id']:
            return jsonify({'erro': 'ID já existe'}), 400
    
    dados.append(novo_aluno)
    salvar_dados(dados)
    return jsonify(novo_aluno), 201


@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):

    dados = ler_dados()
    for aluno in dados:
        if aluno['id'] == aluno_id:
            aluno.update(request.json)
            salvar_dados(dados)
            return jsonify(aluno)
    return jsonify({'erro': 'Aluno não encontrado'}), 404

@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def deletar_aluno(aluno_id):

    dados = ler_dados()
    for i, aluno in enumerate(dados):
        if aluno['id'] == aluno_id:
            dados.pop(i)
            salvar_dados(dados)
            return jsonify({'mensagem': 'Aluno removido com sucesso'})
    return jsonify({'erro': 'Aluno não encontrado'}), 404


@app.route('/alunos/curso/<string:nome_curso>', methods=['GET'])
def buscar_por_curso(nome_curso):

    dados = ler_dados()
    alunos_curso = [aluno for aluno in dados if aluno['curso'].lower() == nome_curso.lower()]
    if alunos_curso:
        return jsonify(alunos_curso)
    return jsonify({'mensagem': f'Nenhum aluno encontrado no curso {nome_curso}'}), 404


@app.route('/alunos/idade/<int:idade_minima>', methods=['GET'])
def buscar_por_idade(idade_minima):

    dados = ler_dados()
    alunos_filtrados = [aluno for aluno in dados if aluno['idade'] >= idade_minima]
    if alunos_filtrados:
        return jsonify(alunos_filtrados)
    return jsonify({'mensagem': f'Nenhum aluno com {idade_minima} anos ou mais'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
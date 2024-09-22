import json
import uuid

import redis
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = "your_secret_key"
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

@app.route("/")
def index():
    return render_template("list_sessions.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/list_sessions_page")
def list_sessions_page():
    return render_template("list_sessions.html")

@app.route("/session_details/<session_id>", methods=["GET"])
def session_details(session_id):
    # Recupera a sessão e verifica se ela existe
    session_data = redis_client.get(session_id)
    if not session_data:
        return jsonify({"message": "Sessão não encontrada."}), 404

    session_data = json.loads(session_data)
    title = session_data.get("title")
    quests = session_data.get("quests", [])

    # Formata as questões para o frontend
    formatted_quests = []
    for quest in quests:
        formatted_quests.append({
            "id": quest["id"],
            "pergunta": quest["pergunta"],
            "opcoes": quest["opcoes"]
        })

    return render_template("session_details.html", title=title, quests=formatted_quests, session_id=session_id)


# Função de verificação de tipo de usuário
def generate_session_id():
    return uuid.uuid4().hex

# Rota para iniciar uma sessão de votação (somente Admin)
@app.route("/start_voting", methods=["POST"])
def start_voting():
    data = request.json
    session_id = generate_session_id()
    title = data.get("title")
    quests = data.get("quests")

    # Iniciar a sessão de votação
    session_data = {
        "title": title,
        "quests": quests,
        "count": 0,  # Total de votos
        "responses": {}  # Inicializa os votos para cada questão
    }

    # Inicializa votos para cada questão e suas opções
    for quest in quests:
        quest_id = quest["id"]
        session_data["responses"][quest_id] = {opcao: 0 for opcao in quest["opcoes"]}

    # Status da sessão
    session_data["status"] = "ativa"
    redis_client.set(session_id, json.dumps(session_data))
    
    return jsonify({"message": "Sessão de votação iniciada com sucesso.", "session_id": session_id})

# Rota para os usuários votarem nas quests
@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    session_id = data.get("session_id")
    votes = data.get("votes")  # Lista de votos, cada item correspondente a uma quest

    # Verifica se a sessão existe e está ativa
    session_data = redis_client.get(session_id)
    if not session_data:
        return jsonify({"message": "Sessão não encontrada."}), 404

    session_data = json.loads(session_data)
    if session_data["status"] != "ativa":
        return jsonify({"message": "A votação para esta sessão está encerrada."}), 400

    # Registra os votos
    for quest_id, vote_list in votes.items():
        if quest_id not in session_data['responses']:
            session_data['responses'][quest_id] = {}
        
        for vote in vote_list:  # Vote pode ser uma lista
            if vote not in session_data['responses'][quest_id]:
                session_data['responses'][quest_id][vote] = 0
            session_data['responses'][quest_id][vote] += 1

    session_data['count'] += 1
    redis_client.set(session_id, json.dumps(session_data))

    return jsonify({"message": "Votos registrados com sucesso."})

# Rota para encerrar a sessão de votação (somente Admin)
@app.route("/end_voting/<session_id>", methods=["POST"])
def end_voting(session_id):

    session_data = redis_client.get(session_id)
    if not session_data:
        return jsonify({"message": "Sessão não encontrada."}), 404

    # Encerrar a sessão de votação
    session_data = json.loads(session_data)
    session_data["status"] = "encerrada"
    redis_client.set(session_id, json.dumps(session_data))

    return jsonify({"message": "Sessão de votação encerrada com sucesso."})

# Rota para listar todas as sessões (Admin)
@app.route('/list_sessions', methods=['GET'])
def list_sessions():
    
    # Busca todas as chaves que representam sessões
    session_keys = redis_client.keys('*')
    
    # Filtra apenas sessões ativas, ignorando outras chaves
    session_keys = [key for key in session_keys if json.loads(redis_client.get(key)).get('status') == 'ativa']

    return jsonify(session_keys)


@app.route('/list_all_sessions', methods=['GET'])
def list_all_sessions():
    # Busca todas as chaves que representam sessões
    session_keys = redis_client.keys('*')
    
    # Cria uma lista para armazenar os detalhes de cada sessão
    sessions_details = []

    for key in session_keys:
        session_data = redis_client.get(key)
        if session_data:
            session_data = json.loads(session_data)
            # Verifica se a sessão está ativa
            # Calcula o total de votos
            total_votes = session_data.get('count', 0)
            
            # Formata os votos das questões
            formatted_quests = {}
            for quest_id, votes in session_data.get('responses', {}).items():
                formatted_quests[quest_id] = votes

            sessions_details.append({
                'session_id': key,
                'title': session_data.get('title'),
                'total_votes': total_votes,
                'quests_votes': formatted_quests
            })

    return jsonify(sessions_details)



if __name__ == "__main__":
    app.run(debug=True)

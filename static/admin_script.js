// Função para adicionar uma nova questão
document.getElementById('add-quest-btn').addEventListener('click', () => {
    const questsContainer = document.getElementById('quests-container');
    const questNumber = questsContainer.children.length + 1;

    const questDiv = document.createElement('div');
    questDiv.classList.add('quest');
    questDiv.innerHTML = `
        <label for="pergunta">Pergunta ${questNumber}:</label>
        <input type="text" name="pergunta" required>
        <label for="opcoes">Opções (separadas por vírgula):</label>
        <input type="text" name="opcoes" required>
    `;
    questsContainer.appendChild(questDiv);
});

// Função para criar uma nova sessão de votação
document.getElementById('create-voting-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const questElements = document.querySelectorAll('#quests-container .quest');
    const quests = Array.from(questElements).map((quest, index) => {
        return {
            id: index + 1,
            pergunta: quest.querySelector('input[name="pergunta"]').value,
            opcoes: quest.querySelector('input[name="opcoes"]').value.split(',')
        };
    });

    const response = await fetch('/start_voting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, quests })
    });

    const result = await response.json();
    document.getElementById('create-session-result').innerText = result.message;
    listAllSessions();

});

// Função para encerrar uma sessão de votaçã

async function listAllSessions() {
    const response = await fetch('/list_sessions', { method: 'GET' });

    const result = await response.json();
    const sessionsListDiv = document.getElementById('sessions-list');
    sessionsListDiv.innerHTML = '<h3>Sessões Ativas:</h3>';

    if (result.length === 0) {
        sessionsListDiv.innerHTML += '<p>Nenhuma sessão encontrada.</p>';
    } else {
        const ul = document.createElement('ul');
        result.forEach(sessionId => {
            const li = document.createElement('li');
            const buttonEndSession = document.createElement('button');
            buttonEndSession.innerText = 'Encerrar Sessão';
            buttonEndSession.addEventListener('click', async () => {
                const response = await fetch(`/end_voting/${sessionId}`, { method: 'POST' });
                const result = await response.json();
                listAllSessions();
            });
            const text = document.createElement('div');
            text.innerText = `Sessão ID: ${sessionId}`;
            li.appendChild(text);
            li.appendChild(buttonEndSession);

            ul.appendChild(li);

        });
        sessionsListDiv.appendChild(ul);
    }
}
// Função para listar todas as sessões
document.getElementById('list-sessions-btn').addEventListener('click', async () => {
    listAllSessions();
});

document.onload = listAllSessions();
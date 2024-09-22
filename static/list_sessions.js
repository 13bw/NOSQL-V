window.addEventListener('DOMContentLoaded', async () => {
    // Busca sessões ativas para permitir votação
    const activeSessionsResponse = await fetch('/list_sessions', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    const activeSessions = await activeSessionsResponse.json();
    const activeSessionsListDiv = document.getElementById('active-sessions-list');
    activeSessionsListDiv.innerHTML = '';

    if (Array.isArray(activeSessions)) {
        activeSessions.forEach(sessionId => {
            const sessionDiv = document.createElement('div');
            sessionDiv.classList.add('session-item');
            sessionDiv.innerHTML = `
                <p>ID da Sessão: ${sessionId}</p>
                <a href="/session_details/${sessionId}">Ver Detalhes e Votar</a>
            `;
            activeSessionsListDiv.appendChild(sessionDiv);
        });
    } else {
        activeSessionsListDiv.innerText = 'Nenhuma sessão ativa encontrada.';
    }

    // Busca todos os resultados das sessões
    const allSessionsResponse = await fetch('/list_all_sessions', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    const allSessions = await allSessionsResponse.json();
    const resultsListDiv = document.getElementById('results-list');
    resultsListDiv.innerHTML = '';

    if (Array.isArray(allSessions)) {
        allSessions.forEach(session => {
            const sessionDiv = document.createElement('div');
            sessionDiv.classList.add('session-item');

            let questsVotesHtml = '';
            for (const [questId, votes] of Object.entries(session.quests_votes)) {
                for (const [option, count] of Object.entries(votes)) {
                    questsVotesHtml += `<li>${questId} - ${option}, Votos: ${count}</li>`;
                }
                questsVotesHtml += '</ul>';
            }

            sessionDiv.innerHTML = `
                <p>ID da Sessão: ${session.session_id}</p>
                <p>Título: ${session.title}</p>
                <p>Total de Votos: ${session.total_votes}</p>
                <div>${questsVotesHtml}</div>
            `;
            resultsListDiv.appendChild(sessionDiv);
        });
    } else {
        resultsListDiv.innerText = 'Nenhum resultado de sessão encontrado.';
    }
});

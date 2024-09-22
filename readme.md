## Integrantes do Grupo
- Lennon Machado da Silva
- Willian Neves de Araujo
- Gustavo Pereira

---

Esse script é uma aplicação web de votações. Ele usa o Redis, que é um banco de dados bem rápido, para salvar as votações temporariamente. Cada votação é chamada de "sessão" e tem um título, várias perguntas (quests) e opções de respostas. O admin cria a sessão, as perguntas e opções, e cada vez que alguém vota, o Redis guarda esses votos e atualiza a contagem de quantas pessoas escolheram cada resposta. Cada sessão tem um ID único, como um código especial, para diferenciar as votações. Quando a votação acaba, o admin pode fechar a sessão e ninguém mais pode votar.

As rotas da aplicação fazem tudo funcionar: tem uma rota para o admin iniciar uma votação, outra para os usuários votarem, e uma para o admin encerrar. Também tem como listar as sessões ativas (as que estão abertas para votar) e ver o resumo de todas as sessões, incluindo as encerradas, com a contagem de votos. A escolha de usar Redis e JSON facilita muito, porque é simples de salvar e buscar os dados rapidamente, sem complicar o código.
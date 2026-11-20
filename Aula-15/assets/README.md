## 💡 O problema que essa automação resolveu

Eu queria acompanhar as novidades e lançamentos do **Fragrantica Brasil** sem precisar lembrar de abrir o site todos os dias, navegar por menus ou lidar com o excesso de informação da página inicial — e, principalmente, sem depender de configurações complexas, chaves de API ou criação de contas extras.

Com esse fluxo simples de 5 etapas no **n8n**, eu transformei uma checagem manual diária em um resumo direto na minha caixa de entrada:

1. **O despertador (`Schedule Trigger`):** Em vez de eu ter que lembrar de visitar o site, o próprio fluxo acorda sozinho todos os dias no horário que eu defini.
2. **A visita ao site (`HTTP Request`):** Como o portal não tinha um feed RSS aberto funcionando, esse nó faz o papel de abrir a aba de notícias do Fragrantica por baixo dos panos e trazer o conteúdo da página.
3. **A peneira (`HTML`):** Para não receber uma bagunça cheia de menus e botões, esse passo filtra o código da página e pesca apenas o que interessa: os títulos das matérias em destaque e seus respectivos links.
4. **O filtro de foco (`Limit`):** Para o e-mail não virar um textão cansativo, ele corta a lista e segura apenas os 5 artigos mais recentes.
5. **A entrega (`Gmail`):** Por fim, ele monta uma mensagem limpa com os títulos e links e dispara direto para o meu e-mail, pronto para eu ler quando quiser.

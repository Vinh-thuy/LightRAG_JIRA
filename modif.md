Modifications dans les fichiers modifiés
Voici un résumé en Markdown des modifications apportées à chaque fichier par rapport au repo d'origine. Chaque section décrit les changements clés pour faciliter l'upload (par exemple, dans un PR).

examples/lightrag_openai_demo.py
Suppression des anciens fichiers de données : Le code pour supprimer les fichiers de données existants (comme graph_chunk_entity_relation.graphml, etc.) a été commenté, empêchant la suppression automatique.
Changement de fichier d'entrée : Le fichier lu a été modifié de "./book.txt" à "/Users/vinh/Documents/LightRAG-6 2/jira_tickets_insightsbooster.json" pour traiter des données Jira au lieu d'un livre.
Commentaire des modes de recherche : Les recherches en mode "naive", "local" et "global" ont été commentées, probablement pour se concentrer sur le mode hybride.
Modification de la requête hybride : La requête a été changée en français : "Donne-moi une analyse globale d'avancement de tous les projets", avec des paramètres ajustés (top_k=60, chunk_top_k=10).
lightrag/constants.py
Ajout de types d'entités spécifiques à Jira : Nouveaux types ajoutés à DEFAULT_ENTITY_TYPES : "Ticket", "Project", "User", "Status", "Priority", et "Other". Cela étend le système d'entités pour mieux gérer les données Jira.
lightrag/llm/openai.py
Désactivation de pipmaster : L'import et l'installation dynamique de pipmaster pour openai ont été commentés, avec une note pour les environnements "air-gapped" (sans accès internet).
Changement de modèle : Dans gpt_4o_complete, le modèle utilisé a été changé de "gpt-4o" à "gpt-4o-mini" pour une version plus légère.
Nouvelle fonction ajoutée : Ajout de gpt_5_mini_complete, une fonction similaire à gpt_4o_mini_complete mais utilisant le modèle "gpt-5-mini" (possiblement une faute de frappe ou un modèle personnalisé).
lightrag/operate.py
Ajout de données d'exemple Jira : Dans la fonction 
extract_entities
, un paramètre example_jira_data=PROMPTS["example_jira_data"] a été ajouté au formatage des prompts, intégrant des exemples spécifiques à Jira pour l'extraction d'entités.
lightrag/prompt.py
Modification des exemples de prompts : Les exemples existants (sur les finances et l'athlétisme) ont été supprimés.
Ajout d'un exemple Jira : Un long exemple a été ajouté avec des données de tickets Jira (TCAAS3883-xxx), incluant entités comme tickets, statuts, priorités, et relations (e.g., has_status, has_priority). Le format a été changé de {tuple_delimiter} à <|#|> pour les délimiteurs, et {completion_delimiter} à <|COMPLETE|>.
Focus sur les données Jira : Les exemples sont maintenant orientés vers l'analyse de tickets Jira, avec des entités et relations adaptées (e.g., projets, utilisateurs, statuts opérationnels).

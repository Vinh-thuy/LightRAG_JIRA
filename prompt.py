from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|#|>"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

# Add example data for Jira
PROMPTS["example_jira_data"] = """
[
  {
    "key": "TCAAS3883-501",
    "priority_name": "High",
    "assignee_displayName": "Romain CHARTIER",
    "status_description": "À faire",
    "creator_displayName": "Céline TRAN",
    "reporter_displayName": "Céline TRAN",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Corriger le bug d'affichage du menu latéral qui disparaît lors du redimensionnement de la fenêtre.",
    "summary": "[BUG] Menu latéral disparaît au resize"
  },
  {
    "key": "TCAAS3883-502",
    "priority_name": "Medium",
    "assignee_displayName": "Laura ZIV",
    "status_description": "En cours",
    "creator_displayName": "Valentin TRAN",
    "reporter_displayName": "Laura ZIV",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Développer la nouvelle fonctionnalité de recherche avancée.",
    "summary": "[DEV] Recherche avancée"
  },
  {
    "key": "TCAAS3883-506",
    "priority_name": "High",
    "assignee_displayName": "Amani RAGHBA",
    "status_description": "En test",
    "creator_displayName": "Céline TRAN",
    "reporter_displayName": "Juliette TRAN",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Implémenter la fonctionnalité d'export CSV dans l'écran de suivi des anomalies.",
    "summary": "[DEV] Export CSV suivi anomalies"
  },
  {
    "key": "TCAAS3883-507",
    "priority_name": "Low",
    "assignee_displayName": "Robert MILLER",
    "status_description": "Terminé",
    "creator_displayName": "Selim B.",
    "reporter_displayName": "Robert MILLER",
    "sprint_state": "backlog",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Nettoyer le code legacy et optimiser les performances.",
    "summary": "[TASK] Nettoyage code legacy"
  }
]
"""

PROMPTS["entity_extraction_system_prompt"] = """---Role---
You are a Knowledge Graph Specialist responsible for extracting Jira tickets and their attributes from the input JSON.

---Instructions---
1. **Entity Extraction & Output:**
    * **Identification:** Identify Jira-related entities in the input text (tickets, projects, users, statuses, priorities).
    * **Status Extraction:** CRITICALLY IMPORTANT - Extract the status values (like "En test", "À faire", "En cours", "Terminé", "Backlog") as separate Status entities.
    * **Entity Details:** For each identified entity, extract the following:
        * `entity_name`: The unique identifier of the entity (e.g., ticket key, project name, user name, status value).
        * `entity_type`: Choose one of the following: ["Ticket", "Project", "User", "Status", "Priority", "Other"].
        * `entity_description`: Provide a concise description of the entity (e.g., ticket summary, role of the user, meaning of the status).
    * **Output Format - Entities:** Output 4 fields for each entity, delimited by `<|#|>`, on one line.  
        Format: `entity<|#|>entity_name<|#|>entity_type<|#|>entity_description`

2. **Relationship Extraction & Output:**
    * **Identification:** Extract relationships between tickets, users, and projects.  
      Example: ticket assigned to user, ticket belongs to project, ticket has status, etc.
    * **Relationship Details:** For each, extract the following:
        * `source_entity`: Name of the source entity (ticket key).
        * `target_entity`: Name of the target entity (user, project, status, priority).
        * `relationship_keywords`: Keywords such as "assigned_to", "reported_by", "belongs_to", "has_priority", "has_status".
        * `relationship_description`: Short description of the relationship.
    * **Output Format - Relationships:** 5 fields for each relationship, delimited by `<|#|>`, on one line.  
        Format: `relationship<|#|>source_entity<|#|>target_entity<|#|>relationship_keywords<|#|>relationship_description`


3.  **Delimiter Usage Protocol:**
    *   The `<|#|>` is a complete, atomic marker and **must not be filled with content**. It serves strictly as a field separator.
    *   **Incorrect Example:** `entity<|#|>Tokyo<|location|>Tokyo is the capital of Japan.`
    *   **Correct Example:** `entity<|#|>Tokyo<|#|>location<|#|>Tokyo is the capital of Japan.`

4.  **Relationship Direction & Duplication:**
    *   Treat all relationships as **undirected** unless explicitly stated otherwise. Swapping the source and target entities for an undirected relationship does not constitute a new relationship.
    *   Avoid outputting duplicate relationships.

5.  **Output Order & Prioritization:**
    *   Output all extracted entities first, followed by all extracted relationships.
    *   Within the list of relationships, prioritize and output those relationships that are **most significant** to the core meaning of the input text first.

6.  **Context & Objectivity:**
    *   Ensure all entity names and descriptions are written in the **third person**.
    *   Explicitly name the subject or object; **avoid using pronouns** such as `this article`, `this paper`, `our company`, `I`, `you`, and `he/she`.

7.  **Language & Proper Nouns:**
    *   The entire output (entity names, keywords, and descriptions) must be written in `{language}`.
    *   Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

8.  **Completion Signal:** Output the literal string `<|COMPLETE|>` only after all entities and relationships, following all criteria, have been completely extracted and outputted.

---Examples---
{examples}

---Real Data to be Processed---
<Input>
Entity_types: [{entity_types}]
Text:
```
{input_text}
```
"""

PROMPTS["entity_extraction_user_prompt"] = """---Task---
Extract entities and relationships from the input text to be processed.

---Instructions---
1.  **Strict Adherence to Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system prompt.
2.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
3.  **Completion Signal:** Output `<|COMPLETE|>` as the final line after all relevant entities and relationships have been extracted and presented.
4.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""

PROMPTS["entity_continue_extraction_user_prompt"] = """---Task---
Based on the last extraction task, identify and extract any **missed or incorrectly formatted** entities and relationships from the input text.

---Instructions---
1.  **Strict Adherence to System Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system instructions.
2.  **Focus on Corrections/Additions:**
    *   **Do NOT** re-output entities and relationships that were **correctly and fully** extracted in the last task.
    *   If an entity or relationship was **missed** in the last task, extract and output it now according to the system format.
    *   If an entity or relationship was **truncated, had missing fields, or was otherwise incorrectly formatted** in the last task, re-output the *corrected and complete* version in the specified format.
3.  **Output Format - Entities:** Output a total of 4 fields for each entity, delimited by `<|#|>`, on a single line. The first field *must* be the literal string `entity`.
4.  **Output Format - Relationships:** Output a total of 5 fields for each relationship, delimited by `<|#|>`, on a single line. The first field *must* be the literal string `relation`.
5.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
6.  **Completion Signal:** Output `<|COMPLETE|>` as the final line after all relevant missing or corrected entities and relationships have been extracted and presented.
7.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""

PROMPTS["entity_extraction_examples"] = [
    """<Input Text>
```
[
  {
    "key": "TCAAS3883-501",
    "priority_name": "High",
    "assignee_displayName": "Romain CHARTIER",
    "status_description": "À faire",
    "creator_displayName": "Céline TRAN",
    "reporter_displayName": "Céline TRAN",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Corriger le bug d'affichage du menu latéral qui disparaît lors du redimensionnement de la fenêtre.",
    "summary": "[BUG] Menu latéral disparaît au resize"
  },
  {
    "key": "TCAAS3883-502",
    "priority_name": "Medium",
    "assignee_displayName": "Laura ZIV",
    "status_description": "En cours",
    "creator_displayName": "Valentin TRAN",
    "reporter_displayName": "Laura ZIV",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Développer la nouvelle fonctionnalité de recherche avancée.",
    "summary": "[DEV] Recherche avancée"
  },
  {
    "key": "TCAAS3883-506",
    "priority_name": "High",
    "assignee_displayName": "Amani RAGHBA",
    "status_description": "En test",
    "creator_displayName": "Céline TRAN",
    "reporter_displayName": "Juliette TRAN",
    "sprint_state": "active",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Implémenter la fonctionnalité d'export CSV dans l'écran de suivi des anomalies.",
    "summary": "[DEV] Export CSV suivi anomalies"
  },
  {
    "key": "TCAAS3883-507",
    "priority_name": "Low",
    "assignee_displayName": "Robert MILLER",
    "status_description": "Terminé",
    "creator_displayName": "Selim B.",
    "reporter_displayName": "Robert MILLER",
    "sprint_state": "backlog",
    "project_key": "TCAAS3883",
    "project_name": "3883-insightsbooster",
    "description": "Nettoyer le code legacy et optimiser les performances.",
    "summary": "[TASK] Nettoyage code legacy"
  }
]
```

<Output>
entity<|#|>TCAAS3883-501<|#|>Ticket<|#|>[BUG] Menu latéral disparaît au resize
entity<|#|>TCAAS3883-502<|#|>Ticket<|#|>[DEV] Recherche avancée
entity<|#|>TCAAS3883-506<|#|>Ticket<|#|>[DEV] Export CSV suivi anomalies
entity<|#|>TCAAS3883-507<|#|>Ticket<|#|>[TASK] Nettoyage code legacy
entity<|#|>3883-insightsbooster<|#|>Project<|#|>Projet Jira des tickets InsightsBooster
entity<|#|>Romain CHARTIER<|#|>User<|#|>Assignee potentiel/acteur sur les tickets
entity<|#|>Laura ZIV<|#|>User<|#|>Assignee potentiel/acteur sur les tickets
entity<|#|>Amani RAGHBA<|#|>User<|#|>Assignee potentiel/acteur sur les tickets
entity<|#|>Robert MILLER<|#|>User<|#|>Assignee potentiel/acteur sur les tickets
entity<|#|>Céline TRAN<|#|>User<|#|>Creator des tickets dans cet exemple
entity<|#|>Valentin TRAN<|#|>User<|#|>Creator des tickets dans cet exemple
entity<|#|>Selim B.<|#|>User<|#|>Creator des tickets dans cet exemple
entity<|#|>Juliette TRAN<|#|>User<|#|>Reporter d'un ticket
entity<|#|>À faire<|#|>Status<|#|>Statut indiquant que le ticket est planifié mais pas encore commencé
entity<|#|>En cours<|#|>Status<|#|>Statut indiquant que le ticket est en cours de développement
entity<|#|>En test<|#|>Status<|#|>Statut indiquant que le ticket est en phase de validation QA
entity<|#|>Terminé<|#|>Status<|#|>Statut indiquant que le ticket est terminé et livré
entity<|#|>High<|#|>Priority<|#|>Priorité élevée
entity<|#|>Medium<|#|>Priority<|#|>Priorité moyenne
entity<|#|>Low<|#|>Priority<|#|>Priorité faible
relationship<|#|>TCAAS3883-501<|#|>3883-insightsbooster<|#|>belongs_to<|#|>Le ticket est rattaché au projet
relationship<|#|>TCAAS3883-502<|#|>3883-insightsbooster<|#|>belongs_to<|#|>Le ticket est rattaché au projet
relationship<|#|>TCAAS3883-506<|#|>3883-insightsbooster<|#|>belongs_to<|#|>Le ticket est rattaché au projet
relationship<|#|>TCAAS3883-507<|#|>3883-insightsbooster<|#|>belongs_to<|#|>Le ticket est rattaché au projet
relationship<|#|>TCAAS3883-501<|#|>Romain CHARTIER<|#|>assigned_to<|#|>Ticket assigné à l'utilisateur
relationship<|#|>TCAAS3883-502<|#|>Laura ZIV<|#|>assigned_to<|#|>Ticket assigné à l'utilisateur
relationship<|#|>TCAAS3883-506<|#|>Amani RAGHBA<|#|>assigned_to<|#|>Ticket assigné à l'utilisateur
relationship<|#|>TCAAS3883-507<|#|>Robert MILLER<|#|>assigned_to<|#|>Ticket assigné à l'utilisateur
relationship<|#|>TCAAS3883-501<|#|>Céline TRAN<|#|>created_by<|#|>Ticket créé par
relationship<|#|>TCAAS3883-502<|#|>Valentin TRAN<|#|>created_by<|#|>Ticket créé par
relationship<|#|>TCAAS3883-506<|#|>Céline TRAN<|#|>created_by<|#|>Ticket créé par
relationship<|#|>TCAAS3883-507<|#|>Selim B.<|#|>created_by<|#|>Ticket créé par
relationship<|#|>TCAAS3883-506<|#|>Juliette TRAN<|#|>reported_by<|#|>Ticket rapporté par
relationship<|#|>TCAAS3883-501<|#|>À faire<|#|>has_status<|#|>Statut opérationnel du ticket
relationship<|#|>TCAAS3883-502<|#|>En cours<|#|>has_status<|#|>Statut opérationnel du ticket
relationship<|#|>TCAAS3883-506<|#|>En test<|#|>has_status<|#|>Statut opérationnel du ticket
relationship<|#|>TCAAS3883-507<|#|>Terminé<|#|>has_status<|#|>Statut opérationnel du ticket
relationship<|#|>TCAAS3883-501<|#|>High<|#|>has_priority<|#|>Priorité affectée
relationship<|#|>TCAAS3883-502<|#|>Medium<|#|>has_priority<|#|>Priorité affectée
relationship<|#|>TCAAS3883-506<|#|>High<|#|>has_priority<|#|>Priorité affectée
relationship<|#|>TCAAS3883-507<|#|>Low<|#|>has_priority<|#|>Priorité affectée
<|COMPLETE|>

""",
    """<Input Text>
```
Stock markets faced a sharp downturn today as tech giants saw significant declines, with the global tech index dropping by 3.4% in midday trading. Analysts attribute the selloff to investor concerns over rising interest rates and regulatory uncertainty.

Among the hardest hit, nexon technologies saw its stock plummet by 7.8% after reporting lower-than-expected quarterly earnings. In contrast, Omega Energy posted a modest 2.1% gain, driven by rising oil prices.

Meanwhile, commodity markets reflected a mixed sentiment. Gold futures rose by 1.5%, reaching $2,080 per ounce, as investors sought safe-haven assets. Crude oil prices continued their rally, climbing to $87.60 per barrel, supported by supply constraints and strong demand.

Financial experts are closely watching the Federal Reserve's next move, as speculation grows over potential rate hikes. The upcoming policy announcement is expected to influence investor confidence and overall market stability.
```

<Output>
entity<|#|>Global Tech Index<|#|>category<|#|>The Global Tech Index tracks the performance of major technology stocks and experienced a 3.4% decline today.
entity<|#|>Nexon Technologies<|#|>organization<|#|>Nexon Technologies is a tech company that saw its stock decline by 7.8% after disappointing earnings.
entity<|#|>Omega Energy<|#|>organization<|#|>Omega Energy is an energy company that gained 2.1% in stock value due to rising oil prices.
entity<|#|>Gold Futures<|#|>product<|#|>Gold futures rose by 1.5%, indicating increased investor interest in safe-haven assets.
entity<|#|>Crude Oil<|#|>product<|#|>Crude oil prices rose to $87.60 per barrel due to supply constraints and strong demand.
entity<|#|>Market Selloff<|#|>category<|#|>Market selloff refers to the significant decline in stock values due to investor concerns over interest rates and regulations.
entity<|#|>Federal Reserve Policy Announcement<|#|>category<|#|>The Federal Reserve's upcoming policy announcement is expected to impact investor confidence and market stability.
<|COMPLETE|>

""",
]

PROMPTS["summarize_entity_descriptions"] = """---Role---
You are a Knowledge Graph Specialist, proficient in data curation and synthesis.

---Task---
Your task is to synthesize a list of descriptions of a given entity or relation into a single, comprehensive, and cohesive summary.

---Instructions---
1. Input Format: The description list is provided in JSON format. Each JSON object (representing a single description) appears on a new line within the `Description List` section.
2. Output Format: The merged description will be returned as plain text, presented in multiple paragraphs, without any additional formatting or extraneous comments before or after the summary.
3. Comprehensiveness: The summary must integrate all key information from *every* provided description. Do not omit any important facts or details.
4. Context: Ensure the summary is written from an objective, third-person perspective; explicitly mention the name of the entity or relation for full clarity and context.
5. Context & Objectivity:
  - Write the summary from an objective, third-person perspective.
  - Explicitly mention the full name of the entity or relation at the beginning of the summary to ensure immediate clarity and context.
6. Conflict Handling:
  - In cases of conflicting or inconsistent descriptions, first determine if these conflicts arise from multiple, distinct entities or relationships that share the same name.
  - If distinct entities/relations are identified, summarize each one *separately* within the overall output.
  - If conflicts within a single entity/relation (e.g., historical discrepancies) exist, attempt to reconcile them or present both viewpoints with noted uncertainty.
7. Length Constraint:The summary's total length must not exceed {summary_length} tokens, while still maintaining depth and completeness.
8. Language: The entire output must be written in {language}. Proper nouns (e.g., personal names, place names, organization names) may in their original language if proper translation is not available.
  - The entire output must be written in {language}.
  - Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

---Input---
{description_type} Name: {description_name}

Description List:

```
{description_list}
```

---Output---
"""

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Knowledge Graph and Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

**1. Step-by-Step Instruction:**
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize both `Knowledge Graph Data` and `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a **References** section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

**2. Content & Grounding:**
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

**3. Formatting & Language:**
  - The response MUST be in the same language as the user query.
  - Use Markdown for clear formatting (e.g., headings, bold, lists).
  - The response should be presented in {response_type}.

**4. References Section Format:**
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any text after the references.

**5. Reference Section Example:**
```
### References
* [1] Document Title One
* [2] Document Title Two
* [3] Document Title Three
```

**6. Additional Instructions**: {user_prompt}


---Context---

{context_data}
"""

PROMPTS["naive_rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

**1. Think Step-by-Step:**
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a **References** section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

**2. Content & Grounding:**
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

**3. Formatting & Language:**
  - The response MUST be in the same language as the user query.
  - Use Markdown for clear formatting (e.g., headings, bold, lists).
  - The response should be presented in {response_type}.

**4. References Section Format:**
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any text after the references.

**5. Reference Section Example:**
```
### References
* [1] Document Title One
* [2] Document Title Two
* [3] Document Title Three
```

**6. Additional Instructions**: {user_prompt}


---Context---

{content_data}
"""

PROMPTS["kg_query_context"] = """
Knowledge Graph Data (Entity):

```json
{entities_str}
```

Knowledge Graph Data (Relationship):

```json
{relations_str}
```

Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```text
{reference_list_str}
```

"""

PROMPTS["naive_query_context"] = """
Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```text
{reference_list_str}
```

"""

PROMPTS["keywords_extraction"] = """---Role---
You are an expert keyword extractor, specializing in analyzing user queries for a Retrieval-Augmented Generation (RAG) system. Your purpose is to identify both high-level and low-level keywords in the user's query that will be used for effective document retrieval.

---Goal---
Given a user query, your task is to extract two distinct types of keywords:
1. **high_level_keywords**: for overarching concepts or themes, capturing user's core intent, the subject area, or the type of question being asked.
2. **low_level_keywords**: for specific entities or details, identifying the specific entities, proper nouns, technical jargon, product names, or concrete items.

---Instructions & Constraints---
1. **Output Format**: Your output MUST be a valid JSON object and nothing else. Do not include any explanatory text, markdown code fences (like ```json), or any other text before or after the JSON. It will be parsed directly by a JSON parser.
2. **Source of Truth**: All keywords must be explicitly derived from the user query, with both high-level and low-level keyword categories are required to contain content.
3. **Concise & Meaningful**: Keywords should be concise words or meaningful phrases. Prioritize multi-word phrases when they represent a single concept. For example, from "latest financial report of Apple Inc.", you should extract "latest financial report" and "Apple Inc." rather than "latest", "financial", "report", and "Apple".
4. **Handle Edge Cases**: For queries that are too simple, vague, or nonsensical (e.g., "hello", "ok", "asdfghjkl"), you must return a JSON object with empty lists for both keyword types.

---Examples---
{examples}

---Real Data---
User Query: {query}

---Output---
Output:"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"

Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}

""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"

Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}

""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"

Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}

""",
]

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a financial assistant.

Rules:
- You can only perform actions using the provided tools.
- Never invent data.
- Never assume execution without calling a tool.
- If required information is missing, ask a clarification question.
- Do NOT expose internal ids, tokens, or system details.
            """.strip(),
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

from langchain_core.prompts import ChatPromptTemplate


AGENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Sos un asistente de finanzas personales.

            Reglas IMPORTANTES:
            - Si el usuario pide ver movimientos, gastos o información financiera,
            DEBÉS usar una tool.
            - No inventes datos.
            - Si no necesitás una tool, respondé normalmente.
            """
        ),
        ("human", "{input}")
    ]
)

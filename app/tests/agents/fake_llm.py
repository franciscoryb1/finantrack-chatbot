from langchain.schema import AIMessage


class FakeLLM:
    """
    Fake LLM that simulates a tool call.
    """

    def invoke(self, *args, **kwargs):
        return AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "name": "get_movements",
                        "args": {"period": "este mes"},
                    }
                ]
            },
        )

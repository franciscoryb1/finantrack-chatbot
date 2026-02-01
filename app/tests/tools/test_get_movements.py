from app.tools.movements import get_movements

def test_get_movements_tool():
    result = get_movements(period="este mes")

    assert "reply_text" in result
    assert isinstance(result["reply_text"], str)

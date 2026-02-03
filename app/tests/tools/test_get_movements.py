import pytest
from app.tools.movements import get_movements


@pytest.mark.asyncio
async def test_get_movements_calls_client_and_returns_data(mocker):
    phone = "+5493411111111"

    fake_client_result = {
        "items": [
            {
                "id": 1,
                "date": "2026-01-01",
                "description": "Supermercado",
                "amount": -12000,
                "type": "expense",
            }
        ],
        "pagination": {
            "page": 1,
            "pageSize": 20,
            "totalItems": 1,
            "totalPages": 1,
        },
    }

    async def fake_list_movements(*args, **kwargs):
        assert kwargs["user_phone"] == phone
        return type(
            "FakeResult",
            (),
            {"model_dump": lambda self: fake_client_result},
        )()

    mocker.patch(
        "app.tools.movements.MovementsClient.list_movements",
        side_effect=fake_list_movements,
    )

    result = await get_movements.ainvoke(
        {
            "phone_number": phone,
            "page": 1,
            "page_size": 20,
        }
    )

    assert result == fake_client_result

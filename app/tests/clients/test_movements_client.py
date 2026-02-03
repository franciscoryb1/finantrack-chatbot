import pytest
import httpx
from app.clients.movements.client import MovementsClient
from app.clients.movements.schemas import PaginatedMovements
from app.core.config import settings


@pytest.mark.asyncio
async def test_list_movements_ok(mocker):
    """
    El client debe:
    - llamar al endpoint correcto
    - enviar API Key
    - enviar X-User-Phone
    - parsear la respuesta correctamente
    """

    # ------------------
    # Arrange
    # ------------------
    base_url = "http://fake-backend"
    api_key = "test-chatbot-api-key"
    phone = "+5493411111111"

    fake_response = {
        "items": [
            {
                "id": 1,
                "date": "2026-01-01",
                "description": "Supermercado",
                "amount": -12000,
                "type": "expense",
                "category_id": 2,
                "category_name": "Alimentos",
                "account_id": 1,
                "account_name": "Cuenta Corriente",
            }
        ],
        "pagination": {
            "page": 1,
            "pageSize": 20,
            "totalItems": 1,
            "totalPages": 1,
        },
    }


    async def fake_get(*args, **kwargs):
        headers = kwargs["headers"]
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["X-User-Phone"] == phone

        request = httpx.Request(
            method="GET",
            url=f"{base_url}/movements",
        )

        return httpx.Response(
            status_code=200,
            json=fake_response,
            request=request,
        )

    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    client = MovementsClient(
        base_url=base_url,
        api_key=api_key,
    )

    # ------------------
    # Act
    # ------------------
    result = await client.list_movements(
        user_phone=phone,
        page=1,
        page_size=20,
    )

    # ------------------
    # Assert
    # ------------------
    assert isinstance(result, PaginatedMovements)
    assert len(result.items) == 1
    assert result.items[0].description == "Supermercado"
    assert result.pagination.total_items == 1


@pytest.mark.asyncio
async def test_list_movements_http_error(mocker):
    """
    Si el backend responde error HTTP,
    el client debe propagar la excepción.
    """

    base_url = "http://fake-backend"
    api_key = "test-chatbot-api-key"
    phone = "+5493411111111"

    async def fake_get(*args, **kwargs):
        request = httpx.Request(
            method="GET",
            url=f"{base_url}/movements",
        )

        return httpx.Response(
            status_code=401,
            json={"message": "Unauthorized"},
            request=request,
        )


    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    client = MovementsClient(
        base_url=base_url,
        api_key=api_key,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await client.list_movements(user_phone=phone)

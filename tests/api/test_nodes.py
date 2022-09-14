from http import HTTPStatus

from store.api.handlers import NodesView


async def test_nodes(seeded_data, api_client):
    response = await api_client.get(
        NodesView.URL_PATH
    )
    assert response.status == HTTPStatus.OK
    data = await response.json()
    assert data == {
        'items': [
            '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            '863e1a7a-1304-42ae-943b-179184c077e3',
            'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
            '98883e8f-0507-482f-bce2-2fb306cf6483'
        ]
    }

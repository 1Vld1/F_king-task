from http import HTTPStatus

from store.api.handlers import NodeView
from store.api.middleware import VALIDATION_FAILED, ITEM_NOT_FOUND


async def test_nodes(seeded_data, api_client, url_for):
    correct_uuid = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=correct_uuid))
    )
    assert response.status == HTTPStatus.OK
    data = await response.json()
    assert data == {
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'date': '2022-03-01T12:00:00.000Z',
        'parentId': None,
        'type': 'CATEGORY',
        'price': 57665,
        'children': [
            {
                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                'name': "Samson 70' LED UHD Smart",
                'date': '2022-03-01T12:00:00.000Z',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'type': 'OFFER',
                'price': 32999,
                'children': None
            },
            {
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'name': 'Смартфоны',
                'date': '2022-02-04T12:00:00.000Z',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'type': 'CATEGORY',
                'price': 69999,
                'children': [
                    {
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'name': 'jPhone 13',
                        'date': '2022-02-01T12:00:00.000Z',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'type': 'OFFER',
                        'price': 79999,
                        'children': None
                    },
                    {
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'name': 'Xomiа Readme 10',
                        'date': '2022-02-04T12:00:00.000Z',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'type': 'OFFER',
                        'price': 59999,
                        'children': None
                    }
                ]
            }
        ]
    }

    invalid_uuid = '069'
    response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=invalid_uuid))
    )
    assert response.status == HTTPStatus.BAD_REQUEST
    data = await response.json()
    assert data['message'] == VALIDATION_FAILED
    assert data['code'] == 400

    nonexistent_uuid = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df2'
    response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=nonexistent_uuid))
    )
    assert response.status == HTTPStatus.NOT_FOUND
    data = await response.json()
    assert data['message'] == ITEM_NOT_FOUND
    assert data['code'] == 404

from http import HTTPStatus

from store.api.handlers import ImportsView, NodeView
from store.api.middleware import VALIDATION_FAILED


async def test_imports(pg, api_client, url_for):
    offers = {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'parentId': None
            }
        ],
        'updateDate': '2022-02-01T12:00:00.000Z'
    }
    smartphones = {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
            },
            {
                'type': 'OFFER',
                'name': 'jPhone 13',
                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'price': 79999
            },
            {
                'type': 'OFFER',
                'name': 'Xomiа Readme 10',
                'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'price': 59999
            }
        ],
        'updateDate': '2022-02-02T12:00:00.000Z'
    }
    tv_sets = {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
            },
            {
                'type': 'OFFER',
                'name': 'Samson 70\" LED UHD Smart',
                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 32999
            },
            {
                'type': 'OFFER',
                'name': 'Phyllis 50\" LED UHD Smarter',
                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 49999
            }
        ],
        'updateDate': '2022-02-03T12:00:00.000Z'
    }
    goldstar = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Goldstar 65\" LED UHD LOL Very Smart',
                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 69999
            }
        ],
        'updateDate': '2022-02-03T15:00:00.000Z'
    }
    changing_parent_uuid = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Phyllis 50\" LED UHD Smarter',
                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'price': 49999
            }
        ],
        'updateDate': '2022-04-03T12:00:00.000Z'
    }

    root_uuid = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=smartphones  # data with nonexistent parentId
    )
    assert response.status == HTTPStatus.BAD_REQUEST
    data = await response.json()
    assert data['message'] == VALIDATION_FAILED
    assert data['code'] == 400

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=offers
    )
    assert response.status == HTTPStatus.OK

    tree_response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=root_uuid))
    )
    data = await tree_response.json()
    assert data == {
        'children': [],
        'date': '2022-02-01T12:00:00.000Z',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'parentId': None,
        'price': None,
        'type': 'CATEGORY'
    }

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=smartphones
    )
    assert response.status == HTTPStatus.OK

    tree_response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=root_uuid))
    )
    data = await tree_response.json()
    assert data == {
        'children': [
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'name': 'jPhone 13',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'name': 'Xomiа Readme 10',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-02-02T12:00:00.000Z',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'name': 'Смартфоны',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'type': 'CATEGORY'
            }
        ],
        'date': '2022-02-02T12:00:00.000Z',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'parentId': None,
        'price': 69999,
        'type': 'CATEGORY'
    }

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=tv_sets
    )
    assert response.status == HTTPStatus.OK

    tree_response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=root_uuid))
    )
    data = await tree_response.json()
    assert data == {
        'children': [
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'name': 'jPhone 13',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'name': 'Xomiа Readme 10',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-02-02T12:00:00.000Z',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'name': 'Смартфоны',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'type': 'CATEGORY'
            },
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-03T12:00:00.000Z',
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'name': 'Samson 70" LED UHD Smart',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-03T12:00:00.000Z',
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'name': 'Phyllis 50" LED UHD Smarter',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 49999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-02-03T12:00:00.000Z',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'name': 'Телевизоры',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 41499,
                'type': 'CATEGORY'
            }
        ],
        'date': '2022-02-03T12:00:00.000Z',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'parentId': None,
        'price': 55749,
        'type': 'CATEGORY'
    }

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=goldstar
    )
    assert response.status == HTTPStatus.OK

    tree_response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=root_uuid))
    )
    data = await tree_response.json()
    assert data == {
        'children': [
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'name': 'jPhone 13',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'name': 'Xomiа Readme 10',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-02-02T12:00:00.000Z',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'name': 'Смартфоны',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 69999,
                'type': 'CATEGORY'
            },
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-03T12:00:00.000Z',
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'name': 'Samson 70" LED UHD Smart',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-03T12:00:00.000Z',
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'name': 'Phyllis 50" LED UHD Smarter',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 49999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-03T15:00:00.000Z',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'name': 'Goldstar 65" LED UHD LOL Very Smart',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 69999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-02-03T15:00:00.000Z',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'name': 'Телевизоры',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 50999,
                'type': 'CATEGORY'
            }
        ],
        'date': '2022-02-03T15:00:00.000Z',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'parentId': None,
        'price': 58599,
        'type': 'CATEGORY'
    }

    response = await api_client.post(
        ImportsView.URL_PATH,
        data=changing_parent_uuid
    )
    assert response.status == HTTPStatus.OK

    tree_response = await api_client.get(
        url_for(NodeView.URL_PATH.format(id=root_uuid))
    )
    data = await tree_response.json()
    assert data == {
        'children': [
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'name': 'jPhone 13',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-02T12:00:00.000Z',
                        'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                        'name': 'Xomiа Readme 10',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 59999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-04-03T12:00:00.000Z',
                        'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                        'name': 'Phyllis 50" LED UHD Smarter',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 49999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-04-03T12:00:00.000Z',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'name': 'Смартфоны',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 63332,
                'type': 'CATEGORY'},
            {
                'children': [
                    {
                        'children': None,
                        'date': '2022-02-03T12:00:00.000Z',
                        'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                        'name': 'Samson 70" LED UHD Smart',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 32999,
                        'type': 'OFFER'
                    },
                    {
                        'children': None,
                        'date': '2022-02-03T15:00:00.000Z',
                        'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                        'name': 'Goldstar 65" LED UHD LOL Very Smart',
                        'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                        'price': 69999,
                        'type': 'OFFER'
                    }
                ],
                'date': '2022-04-03T12:00:00.000Z',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'name': 'Телевизоры',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'price': 51499,
                'type': 'CATEGORY'
            }
        ],
        'date': '2022-04-03T12:00:00.000Z',
        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
        'name': 'Товары',
        'parentId': None,
        'price': 58599,
        'type': 'CATEGORY'
    }

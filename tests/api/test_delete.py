from http import HTTPStatus

import pytest

from store.api.handlers import DeleteView, NodesView
from store.api.middleware import VALIDATION_FAILED, ITEM_NOT_FOUND


@pytest.mark.parametrize(
    'uuid, expected_nodes',
    [
        (
            '98883e8f-0507-482f-bce2-2fb306cf6483',
            [
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                '863e1a7a-1304-42ae-943b-179184c077e3',
                'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'
            ]
        ),
        (
            'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            [
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                '98883e8f-0507-482f-bce2-2fb306cf6483'
            ]
        ),
        (
            '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            []
        )
    ]
)
async def test_delete(seeded_data, api_client, uuid, expected_nodes, url_for):
    response = await api_client.delete(
        url_for(DeleteView.URL_PATH.format(id=uuid))
    )
    assert response.status == HTTPStatus.OK
    nodes_response = await api_client.get(NodesView.URL_PATH)
    nodes = await nodes_response.json()
    assert nodes['items'] == expected_nodes


async def test_delete_invalid_uuid(seeded_data, api_client, url_for):
    invalid_uuid = '123'
    response = await api_client.delete(
        url_for(DeleteView.URL_PATH.format(id=invalid_uuid))
    )
    assert response.status == HTTPStatus.BAD_REQUEST
    data = await response.json()
    assert data['code'] == 400
    assert data['message'] == VALIDATION_FAILED


async def test_delete_nonexistent_uuid(seeded_data, api_client, url_for):
    nonexistent_uuid = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df4'
    response = await api_client.delete(
        url_for(DeleteView.URL_PATH.format(id=nonexistent_uuid))
    )
    assert response.status == HTTPStatus.NOT_FOUND
    data = await response.json()
    assert data['code'] == 404
    assert data['message'] == ITEM_NOT_FOUND

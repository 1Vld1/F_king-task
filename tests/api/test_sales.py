from http import HTTPStatus

from yarl import URL

from store.api.handlers import SalesView
from store.api.middleware import VALIDATION_FAILED


async def test_sales(seeded_data, api_client):
    date = '2022-03-01T14:00:00.000Z'
    response = await api_client.get(
        URL(SalesView.URL_PATH).update_query(date=date)
    )
    assert response.status == HTTPStatus.OK
    data = await response.json()
    assert data == {
        'items': [
            {
                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                'name': "Samson 70' LED UHD Smart",
                'date': '2022-03-01T12:00:00.000Z',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'type': 'OFFER',
                'price': 32999
            }
        ]
    }

    empty_date = '2022-03-03T14:00:00.000Z'
    response = await api_client.get(
        URL(SalesView.URL_PATH).update_query(date=empty_date)
    )
    assert response.status == HTTPStatus.OK
    data = await response.json()
    assert data == {'items': []}

    invalid_date = '2022-03-03T14:00:00.000'
    response = await api_client.get(
        URL(SalesView.URL_PATH).update_query(date=invalid_date)
    )
    assert response.status == HTTPStatus.BAD_REQUEST
    data = await response.json()
    assert data['message'] == VALIDATION_FAILED
    assert data['code'] == 400

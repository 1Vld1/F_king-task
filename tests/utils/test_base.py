from datetime import datetime
from uuid import UUID

import pytest

from store.db.schema import nodes_table
from store.utils.base import (
    CategoryStat,
    format_node,
    get_all_children,
    get_all_parent_uuids,
    get_category_price,
    get_category_stats,
    get_child_category_stat
)


@pytest.mark.parametrize(
    'uuids_set, expected_parent_uuids',
    [
        (
            {'98883e8f-0507-482f-bce2-2fb306cf6483'},
            {
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
            }
        ),
        (
            {'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'},
            {
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'd515e43f-f3f6-4471-bb77-6b455017a2d2'
            }
        ),
        (
            {
                'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                '863e1a7a-1304-42ae-943b-179184c077e3'
            },
            {
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            }
        ),
        (
            {'069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'},
            set()
        )
    ]
)
async def test_get_all_parent_uuids(
    pg,
    seeded_data,
    uuids_set,
    expected_parent_uuids
):
    async with pg.transaction() as conn:
        parent_uuids = await get_all_parent_uuids(conn, uuids_set)

    assert parent_uuids == expected_parent_uuids


testdata = [
    (
        CategoryStat(
            children=[
                {
                    'id': UUID('863e1a7a-1304-42ae-943b-179184c077e3'),
                    'name': 'jPhone 13',
                    'date': datetime(2022, 6, 20, 18, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 79999,
                    'children': None
                },
                {
                    'id': UUID('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'),
                    'name': 'Xomiа Readme 10',
                    'date': datetime(2022, 6, 20, 18, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 59999,
                    'children': None
                }
            ],
            offer_price_sum=139998,
            offer_count=2
        ),
        False,
        {
            'children': [
                {
                    'children': None,
                    'date': datetime(2022, 6, 20, 18, 0),
                    'id': UUID('863e1a7a-1304-42ae-943b-179184c077e3'),
                    'name': 'jPhone 13',
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'price': 79999,
                    'type': 'OFFER'
                },
                {
                    'children': None,
                    'date': datetime(2022, 6, 20, 18, 0),
                    'id': UUID('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'),
                    'name': 'Xomiа Readme 10',
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'price': 59999,
                    'type': 'OFFER'
                }
            ],
            'date': datetime(2022, 2, 1, 12, 0),
            'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            'name': 'Смартфоны',
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'price': 69999,
            'type': 'CATEGORY'
        }
    ),
    (
        CategoryStat(
            children=[
                {
                    'id': UUID('863e1a7a-1304-42ae-943b-179184c077e3'),
                    'name': 'jPhone 13',
                    'date': datetime(2022, 6, 20, 18, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 79999,
                    'children': None
                },
                {
                    'id': UUID('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'),
                    'name': 'Xomiа Readme 10',
                    'date': datetime(2022, 6, 20, 18, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 59999,
                    'children': None
                }
            ],
            offer_price_sum=139998,
            offer_count=2
        ),
        True,
        {
            'date': datetime(2022, 2, 1, 12, 0),
            'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            'name': 'Смартфоны',
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'price': 69999,
            'type': 'CATEGORY'
        }
    ),
    (
        None,
        False,
        {
            'children': None,
            'date': datetime(2022, 2, 1, 12, 0),
            'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            'name': 'Смартфоны',
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'price': None,
            'type': 'CATEGORY'
        }
    ),
    (
        None,
        True,
        {
            'date': datetime(2022, 2, 1, 12, 0),
            'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            'name': 'Смартфоны',
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'price': None,
            'type': 'CATEGORY'
        }
    )
]


@pytest.mark.parametrize(
    'category_stat, without_children, expected_format',
    testdata
)
def test_format_node(category_stat, expected_format, without_children):
    node = {
        'uuid': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
        'node_type': 'CATEGORY',
        'parent_uuid': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
        'name': 'Смартфоны',
        'price': None,
        'updated_at': datetime(2022, 2, 1, 12, 0)
    }

    formatted_node = format_node(node, category_stat, without_children)

    assert formatted_node == expected_format


async def test_get_child_category_stat(pg, seeded_data):
    uuid = UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2')
    select_query = nodes_table.select().where(
        nodes_table.c.uuid == uuid
    )

    async with pg.transaction() as conn:
        raw_child = await conn.fetch(select_query)
        category_stats = await get_category_stats(conn, [uuid])
    category_stat = get_child_category_stat(raw_child, category_stats)

    expected_category_stat = CategoryStat(
        children=[
            {
                'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                'name': 'Смартфоны',
                'date': datetime(2022, 2, 4, 12, 0),
                'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
                'type': 'CATEGORY',
                'price': 69999,
                'children': [
                    {
                        'id': UUID('863e1a7a-1304-42ae-943b-179184c077e3'),
                        'name': 'jPhone 13',
                        'date': datetime(2022, 2, 1, 12, 0),
                        'parentId': UUID(
                            'd515e43f-f3f6-4471-bb77-6b455017a2d2'
                        ),
                        'type': 'OFFER',
                        'price': 79999,
                        'children': None
                    },
                    {
                        'id': UUID('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'),
                        'name': 'Xomiа Readme 10',
                        'date': datetime(2022, 2, 4, 12, 0),
                        'parentId': UUID(
                            'd515e43f-f3f6-4471-bb77-6b455017a2d2'
                        ),
                        'type': 'OFFER',
                        'price': 59999,
                        'children': None
                    }
                ]
            }
        ],
        offer_price_sum=139998,
        offer_count=2)

    assert category_stat == expected_category_stat


@pytest.mark.parametrize(
    'parent_uuid, expected_children_uuids',
    [
        (
            UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            {
                '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                '98883e8f-0507-482f-bce2-2fb306cf6483',
                '863e1a7a-1304-42ae-943b-179184c077e3',
                'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'
            }
        ),
        (
            UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            {
                'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                '863e1a7a-1304-42ae-943b-179184c077e3',
                'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'
            }
        )
    ]
)
async def test_get_all_children(
    pg,
    seeded_data,
    parent_uuid,
    expected_children_uuids
):
    async with pg.transaction() as conn:
        children = {
            str(child['uuid']) for child in await get_all_children(
                conn,
                parent_uuid
            )
        }

    assert children == expected_children_uuids


@pytest.mark.parametrize(
    'price_sum, count, price',
    [(10, 3, 3), (10, 2, 5), (0, 0, None)]
)
def test_get_category_price(price_sum, count, price):
    category_stat = CategoryStat(
        children=[],
        offer_price_sum=price_sum,
        offer_count=count
    )
    category_price = get_category_price(category_stat)

    assert category_price == price


async def test_get_category_stats(pg, seeded_data):
    parent_uuid = UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    expected_children = [
        {
            'id': UUID('98883e8f-0507-482f-bce2-2fb306cf6483'),
            'name': "Samson 70' LED UHD Smart",
            'date': datetime(2022, 3, 1, 12, 0),
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'type': 'OFFER',
            'price': 32999,
            'children': None
        },
        {
            'id': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
            'name': 'Смартфоны',
            'date': datetime(2022, 2, 4, 12, 0),
            'parentId': UUID('069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'),
            'type': 'CATEGORY',
            'price': 69999,
            'children': [
                {
                    'id': UUID('863e1a7a-1304-42ae-943b-179184c077e3'),
                    'name': 'jPhone 13',
                    'date': datetime(2022, 2, 1, 12, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 79999,
                    'children': None
                },
                {
                    'id': UUID('b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4'),
                    'name': 'Xomiа Readme 10',
                    'date': datetime(2022, 2, 4, 12, 0),
                    'parentId': UUID('d515e43f-f3f6-4471-bb77-6b455017a2d2'),
                    'type': 'OFFER',
                    'price': 59999,
                    'children': None
                }
            ]
        }
    ]

    async with pg.transaction() as conn:
        category_stats = await get_category_stats(conn, [parent_uuid])

    assert category_stats == {
        parent_uuid: CategoryStat(
            children=expected_children,
            offer_price_sum=172997,
            offer_count=3
        )
    }

import os
import uuid
from datetime import datetime
from types import SimpleNamespace

import pytest
from alembic.command import upgrade
from asyncpgsa import PG
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from store.db.schema import nodes_table
from store.utils.pg import DEFAULT_PG_URL, make_alembic_config

PG_URL = os.getenv('CI_STORE_PG_URL', DEFAULT_PG_URL)


@pytest.fixture
def tmp_url():
    tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    tmp_url = str(URL(PG_URL).with_path(tmp_name))
    return tmp_url


@pytest.fixture
def postgres(tmp_url):
    """
    Создает временную БД для запуска теста.
    """
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(tmp_url):
    """
    Создает объект с конфигурацией для alembic, настроенный на временную БД.
    """
    cmd_options = SimpleNamespace(config='alembic.ini', name='alembic',
                                  pg_url=tmp_url, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    """
    Возвращает URL к БД с примененными миграциями.
    """
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
async def pg(migrated_postgres):
    pg = PG()
    await pg.init(migrated_postgres)

    return pg


@pytest.fixture(scope='session')
def seeds():
    return [
        {
            'node_type': 'CATEGORY',
            'name': 'Товары',
            'uuid': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'parent_uuid': None,
            'updated_at': datetime(2022, 3, 1, 12, 0),
            'price': None
        },
        {
            'node_type': 'CATEGORY',
            'name': 'Смартфоны',
            'uuid': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'parent_uuid': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': None,
            'updated_at': datetime(2022, 2, 4, 12, 0),
        },
        {
            'node_type': 'OFFER',
            'name': 'jPhone 13',
            'uuid': '863e1a7a-1304-42ae-943b-179184c077e3',
            'parent_uuid': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'price': 79999,
            'updated_at': datetime(2022, 2, 1, 12, 0),
        },
        {
            'node_type': 'OFFER',
            'name': 'Xomiа Readme 10',
            'uuid': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
            'parent_uuid': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'price': 59999,
            'updated_at': datetime(2022, 2, 4, 12, 0),
        },
        {
            'node_type': 'OFFER',
            'name': 'Samson 70\' LED UHD Smart',
            'uuid': '98883e8f-0507-482f-bce2-2fb306cf6483',
            'parent_uuid': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 32999,
            'updated_at': datetime(2022, 3, 1, 12, 0),
        },
    ]


@pytest.fixture
async def seeded_data(seeds, pg):
    async with pg.transaction() as conn:
        query = nodes_table.insert().values(seeds)
        await conn.execute(query)

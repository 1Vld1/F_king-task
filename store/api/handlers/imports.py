from http import HTTPStatus
from typing import Mapping, Any, Set

from aiohttp.web_response import Response
from aiohttp_apispec import request_schema
from asyncpg import Connection
from marshmallow.exceptions import ValidationError
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from store.api.handlers.base import BaseView
from store.api.schema import ImportSchema
from store.db.schema import nodes_table
from store.utils.base import get_all_parent_uuids


class ImportsView(BaseView):
    URL_PATH = '/imports'

    @request_schema(ImportSchema())
    async def post(self):
        """
        Функция делает следующее:
        1. Валидирует запрос
        2. Пишет в БД новые товары или категории
        3. Если товар или категория есть в БД - обновляет их
        4. Обновляет даты обновления всех родителей внесенных записей

        5. ОЧЕНЬ ТОНКИЙ МОМЕНТ, ИНФОРМАЦИЯ ПОЛУЧЕНА ИЗ ПЕРЕПИСКИ С
        ОРГАНИЗАТОРАМИ!!! Если с помощью ручки imports изменяем родителя товара
        или категории - нужно менять дату обновления не только у новых
        родителей, но и у старых.
        IMHO: Такое поведение ручки сомнительно, поскольку при удалении товара
        из категории мы дату обновления не изменяем.
        Применяя удаление и последующую вставку в другую категорию, мы получаем
        такое же состояние БД, что и при изменении родителя при помощи imports,
        но при этом старые родители будут иметь другие даты обновления.
        Тут противоречие.
        """
        items = self.data['items']
        update_date = self.data['updateDate']
        nodes = [
            {
                'uuid': item['id'],
                'name': item['name'],
                'parent_uuid': item.get('parentId'),
                'node_type': item['type'],
                'price': item.get('price'),
                'updated_at': update_date
            } for item in items
        ]

        node_uuids = {node['uuid'] for node in nodes}

        async with self.pg.transaction() as conn:
            all_old_parents = await get_all_parent_uuids(conn, node_uuids)

            ins = insert(nodes_table)
            column_dict = {
                column.name: getattr(ins.excluded, column.name)
                for column in nodes_table.c
            }
            upsert_query = ins.on_conflict_do_update(
                constraint=nodes_table.primary_key,
                set_=column_dict
            ).values(nodes)
            await conn.execute(upsert_query)

            parent_uuids = {
                node['parent_uuid']
                for node in nodes if node['parent_uuid'] is not None
            }

            await self.validate_parent_uuids(conn, parent_uuids)

            # update updated_at for all parents
            all_parent_uuids = await get_all_parent_uuids(conn, node_uuids)
            all_parent_uuids.update(all_old_parents)
            update_query = nodes_table.update().values(
                updated_at=update_date
            ).where(nodes_table.c.uuid.in_(all_parent_uuids))
            await conn.execute(update_query)

        return Response(status=HTTPStatus.OK)

    @staticmethod
    async def validate_parent_uuids(
        conn: Connection,
        parent_uuids: Set[str]
    ):
        select_query = select(
            [func.count(nodes_table.c.uuid)]
        ).where(nodes_table.c.uuid.in_(parent_uuids))
        if len(parent_uuids) != await conn.fetchval(select_query):
            raise ValidationError('Parent UUID is not exist.')

    @property
    def data(self) -> Mapping[str, Any]:
        return self.request['data']

from http import HTTPStatus

from aiohttp.web_response import Response
from sqlalchemy import select

from store.api.handlers.base import BaseView
from store.db.schema import nodes_table


class NodesView(BaseView):
    URL_PATH = '/nodes'

    async def get(self):
        async with self.pg.transaction() as conn:
            select_query = select([nodes_table.c.uuid])
            items = [node['uuid'] for node in await conn.fetch(select_query)]

        return Response(body={'items': items}, status=HTTPStatus.OK)

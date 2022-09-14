from http import HTTPStatus
from uuid import UUID

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response

from store.api.handlers.base import BaseView
from store.api.middleware import ITEM_NOT_FOUND
from store.api.schema import IdSchema
from store.db.schema import nodes_table, NodeType
from store.utils.base import format_node, get_category_stats


class NodeView(BaseView):
    URL_PATH = '/nodes/{id}'

    async def get(self):
        uuid = self.validate_id()
        async with self.pg.transaction() as conn:
            select_query = nodes_table.select().where(
                nodes_table.c.uuid == uuid
            )
            node = await conn.fetch(select_query)
            if not node:
                raise HTTPNotFound(text=ITEM_NOT_FOUND)

            node,  = node
            if node['node_type'] == NodeType.OFFER:
                response_body = format_node(node)
            elif node['node_type'] == NodeType.CATEGORY:
                category_stats = await get_category_stats(conn, [uuid])
                response_body = format_node(node, category_stats[uuid])

        return Response(body=response_body, status=HTTPStatus.OK)

    def validate_id(self) -> UUID:
        return IdSchema().load({'id': self.id})['id']

    @property
    def id(self) -> str:
        return self.request.match_info.get('id')

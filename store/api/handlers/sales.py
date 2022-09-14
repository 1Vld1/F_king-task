import datetime
from http import HTTPStatus

from aiohttp.web_response import Response
from sqlalchemy import and_

from store.api.handlers.base import BaseView
from store.api.schema import DateSchema
from store.db.schema import nodes_table, NodeType
from store.utils.base import format_node


class SalesView(BaseView):
    URL_PATH = '/sales'

    async def get(self):
        end_time = self.validate_date()
        start_time = end_time - datetime.timedelta(hours=24)
        async with self.pg.transaction() as conn:
            select_query = nodes_table.select().where(
                and_(
                    nodes_table.c.node_type == NodeType.OFFER,
                    nodes_table.c.updated_at <= end_time,
                    nodes_table.c.updated_at >= start_time
                )
            )

            items = [
                format_node(node, without_children=True)
                for node in await conn.fetch(select_query)
            ]

        return Response(body={'items': items}, status=HTTPStatus.OK)

    def validate_date(self) -> datetime:
        return DateSchema().load({'date': self.date})['date']

    @property
    def date(self) -> str:
        return self.request.url.query.get('date')

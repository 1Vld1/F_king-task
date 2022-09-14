from http import HTTPStatus
from uuid import UUID

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response

from store.api.handlers.base import BaseView
from store.api.middleware import ITEM_NOT_FOUND
from store.api.schema import IdSchema
from store.db.schema import nodes_table
from store.utils.base import get_all_children


class DeleteView(BaseView):
    URL_PATH = '/delete/{id}'

    async def delete(self):
        uuid = self.validate_id()
        async with self.pg.transaction() as conn:
            children = await get_all_children(conn, uuid)

            if not children:
                raise HTTPNotFound(text=ITEM_NOT_FOUND)
            delete_query = nodes_table.delete().where(
                nodes_table.c.uuid.in_([child['uuid'] for child in children])
            )
            await conn.execute(delete_query)

        return Response(status=HTTPStatus.OK)

    def validate_id(self) -> UUID:
        return IdSchema().load({'id': self.id})['id']

    @property
    def id(self) -> str:
        return self.request.match_info.get('id')

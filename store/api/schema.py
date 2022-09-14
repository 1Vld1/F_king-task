"""
Модуль содержит схемы для валидации данных в запросах и ответах.

Схемы валидации запросов используются в бою для валидации данных отправленных
клиентами.

Схемы валидации ответов *ResponseSchema используются только при тестировании,
чтобы убедиться что обработчики возвращают данные в корректном формате.
"""

from marshmallow import Schema, ValidationError, validates_schema
from marshmallow.fields import Int, Nested, Str, DateTime, UUID
from marshmallow.validate import Length, OneOf, Range

from store.db.schema import NodeType

FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class NodesSchema(Schema):
    id = UUID(required=True)
    name = Str(validate=Length(min=1), required=True)
    type = Str(
        validate=OneOf([node_type.value for node_type in NodeType]),
        required=True
    )
    parentId = UUID(allow_none=True)
    price = Int(validate=Range(min=0), allow_none=True)

    @validates_schema
    def validate_price(self, data, **_):
        if (
            (data['type'] == NodeType.OFFER and data.get('price') is None) or
            (
                data['type'] == NodeType.CATEGORY and
                data.get('price') is not None
            )
        ):
            raise ValidationError('')


class ImportSchema(Schema):
    items = Nested(NodesSchema(many=True), required=True)
    updateDate = DateTime(format=FORMAT, required=True)


class IdSchema(Schema):
    id = UUID(required=True)


class DateSchema(Schema):
    date = DateTime(format=FORMAT)

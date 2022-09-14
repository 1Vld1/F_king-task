from enum import Enum, unique

from sqlalchemy import (
    Column, Enum as PgEnum, Integer,
    MetaData, String, Table, DateTime
)
from sqlalchemy.dialects.postgresql import UUID

# SQLAlchemy рекомендует использовать единый формат для генерации названий для
# индексов и внешних ключей.
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@unique
class NodeType(str, Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


nodes_table = Table(
    'nodes',
    metadata,
    Column('uuid', UUID, primary_key=True),
    Column('node_type', PgEnum(NodeType, name='node_type'), nullable=False),
    Column('parent_uuid', UUID),
    Column('name', String, nullable=False),
    Column('price', Integer),
    Column('updated_at', DateTime, nullable=False)
)

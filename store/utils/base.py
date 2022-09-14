from collections import defaultdict
from dataclasses import dataclass
from typing import List, Mapping, Dict, Any, Optional, Set
from uuid import UUID

from asyncpg import Connection

from store.db.schema import nodes_table, NodeType


async def get_all_parent_uuids(conn: Connection, uuids: Set[str]) -> set:
    result = set()
    while True:
        select_query = nodes_table.select().where(
            nodes_table.c.uuid.in_(uuids)
        )
        nodes = await conn.fetch(select_query)
        if not nodes:
            break
        else:
            uuids = [
                str(node['parent_uuid']) for node in nodes
                if node['parent_uuid'] is not None
            ]
            result.update(uuids)

    return result


async def get_all_children(conn: Connection, uuid: UUID) -> list:
    select_parent_query = nodes_table.select().where(
        nodes_table.c.uuid == uuid
    )
    children = await conn.fetch(select_parent_query)

    parent_uuids = [uuid]
    while True:
        select_query = nodes_table.select().where(
            nodes_table.c.parent_uuid.in_(parent_uuids)
        )
        nodes = await conn.fetch(select_query)
        if not nodes:
            break
        else:
            parent_uuids = [node['uuid'] for node in nodes]
            children.extend(nodes)

    return children


@dataclass
class CategoryStat:
    children: list
    offer_price_sum: int = 0
    offer_count: int = 0


def get_category_price(category_stat: CategoryStat) -> Optional[int]:
    if category_stat.offer_count == 0:
        return None
    return category_stat.offer_price_sum // category_stat.offer_count


def format_node(
    node: Mapping[str, Any],
    category_stat: CategoryStat = None,
    without_children: bool = False
) -> Dict[str, Any]:
    price = node['price']
    children = None

    if category_stat is not None:
        price = get_category_price(category_stat)
        children = category_stat.children

    result = {
        'id': node['uuid'],
        'name': node['name'],
        'date': node['updated_at'],
        'parentId': node['parent_uuid'],
        'type': node['node_type'],
        'price': price,
    }

    if without_children:
        return result
    return {**result, 'children': children}


def get_child_category_stat(
    raw_children: Mapping[str, Any],
    category_stats: Dict[UUID, CategoryStat]
) -> CategoryStat:
    children = []
    offer_price_sum = 0
    offer_count = 0
    for child in raw_children:
        category_stat = category_stats[child['uuid']]
        children.append(format_node(child, category_stat))
        offer_price_sum += category_stat.offer_price_sum
        offer_count += category_stat.offer_count
    return CategoryStat(children, offer_price_sum, offer_count)


async def get_category_stats(
    conn: Connection,
    parent_uuids: List[UUID]
) -> Dict[UUID, CategoryStat]:
    result = {uuid: CategoryStat(children=[]) for uuid in parent_uuids}
    category_children = defaultdict(list)

    select_query = nodes_table.select().where(
        nodes_table.c.parent_uuid.in_(parent_uuids)
    )
    for child in await conn.fetch(select_query):
        uuid = child['parent_uuid']
        if child['node_type'] == NodeType.OFFER:
            category_stat = result[uuid]
            category_stat.children.append(format_node(child))
            category_stat.offer_price_sum += child['price']
            category_stat.offer_count += 1
        elif child['node_type'] == NodeType.CATEGORY:
            category_children[uuid].append(child)

    if category_children:
        parent_uuids = [
            node['uuid'] for value in category_children.values()
            for node in value
        ]
        category_stats = await get_category_stats(conn, parent_uuids)
        for uuid, raw_children in category_children.items():
            child_category_stat = get_child_category_stat(
                raw_children, category_stats
            )
            category_stat = result[uuid]
            category_stat.children.extend(child_category_stat.children)
            category_stat.offer_price_sum += (
                child_category_stat.offer_price_sum
            )
            category_stat.offer_count += child_category_stat.offer_count

    return result

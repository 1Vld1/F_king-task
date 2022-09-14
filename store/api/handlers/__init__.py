from store.api.handlers.delete import DeleteView
from store.api.handlers.imports import ImportsView
from store.api.handlers.node import NodeView
from store.api.handlers.nodes import NodesView
from store.api.handlers.sales import SalesView

HANDLERS = (
    DeleteView, ImportsView, NodesView, NodeView, SalesView
)

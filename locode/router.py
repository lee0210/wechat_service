import importlib
import logging

_alias = {}
_routing_tree = {}

class alias:
    def __init__(self, alias, handler):
        self._alias = alias
        module, function = handler.rsplit('.', 1)
        self._handler = getattr(importlib.import_module(module), function)
    def register(self):
        global _alias
        _alias[self._alias] = self._handler

class routing_node:
    def __init__(self, node_id):
        self._node_id, self._sub_node_id = (node_id.rsplit('.', 1) + [None])[0:2]
        self._handler = None
        self._before = [] 
        self._after = []

    def handler(self, handler):
        module, function = handler.rsplit('.', 1)
        self._handler = getattr(importlib.import_module(module), function)
        return self

    def register(self):
        node = _get_routing_node(self._node_id)
        node['type'] = 'node'
        if self._sub_node_id is not None:
            node['child_nodes'][self._sub_node_id] = {}
            node = node.get('child_nodes').get(self._sub_node_id)
        node['type'] = 'leaf'
        node['after'] = self._after
        node['before'] = self._before
        node['handler'] = self._handler
        node['child_nodes'] = {}

    def before_process(self, *argv):
        self._before = [_alias.get(k) for k in argv]
        return self

    def after_process(self, *argv):
        self._after = [_alias.get(k) for k in argv]
        return self

def _get_routing_node(node_id):
    global _routing_tree
    node = _routing_tree
    for nid in node_id.split('.')[1:]:
        node = node.get('child_nodes').get(nid)
    return node
    

def handle(e):
    if e.get('LOCODE_ROUTING_NODE') is None:
        e['LOCODE_ROUTING_NODE'] = '$'
    node = _get_routing_node(e['LOCODE_ROUTING_NODE'])
    print(node['handler'], node['before'], node['after'], node['type'])
    for process in node.get('before'):
        if not process(e):
            return
    node.get('handler')(e)
    if node.get('type') == 'node':
        handle(e)
    for process in node.get('after'):
        if not process(e):
            return
def next_node(e, sub_node_id):
    e['LOCODE_ROUTING_NODE'] += '.' + sub_node_id
    

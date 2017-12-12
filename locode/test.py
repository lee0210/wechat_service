from router import routing_node
from router import alias 
from router import handle

alias('auth', 't.auth').register()
routing_node('$').set_handler('t.root').before_process('auth').register()
routing_node('$.event').set_handler('t.event').register()
routing_node('$.event.text').set_handler('t.text').register()
routing_node('$.event.text.register').set_handler('t.register').register()


handle({'LOCODE_ROUTING_NODE': '$'})


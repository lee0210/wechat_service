from locode.router import alias
from locode.router import routing_node 

alias('validation', 'middleware.validation').register()
alias('decrypt_xml', 'middleware.decrypt_xml').register()
alias('encrypt_xml', 'middleware.encrypt_xml').register()

routing_node('$').handler('handler.root.route').before_process('validation').register()
routing_node('$.init').handler('handler.root.init').register()
routing_node('$.event').handler('handler.event.route').before_process('decrypt_xml').after_process('encrypt_xml').register()

routing_node('$.event.text').handler('handler.text.route').register()
routing_node('$.event.text.captcha').handler('handler.text.captcha').register()
routing_node('$.event.text.register').handler('handler.text.register').register()
routing_node('$.event.text.default').handler('handler.text.default').register()

routing_node('$.event.subscribe').handler('handler.event.subscribe').register()


from router import next_node
def root(e):
    next_node(e, 'event')
    print(e)
def event(e):
    next_node(e, 'text')
    print(e)
def text(e):
    next_node(e, 'register')
    print(e)
def auth(e):
    print('auth')
    return True
def register(e):
    print('register')

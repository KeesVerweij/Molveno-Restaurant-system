class OrderList:
    def __init__(self, item=None, menu=None):
        '''
        if object created it should get either a menu item or menu (either one of them must be
        ordered first)
        '''
        self._items = list(item) if item else list()
        self._menus = list(menu) if menu else list()

    def add_item(self, item):
        self._items.append(item)

    def add_menu(self, menu):
        self._menus.append(menu)

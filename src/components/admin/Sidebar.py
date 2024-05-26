from src.components.Sidebar import Sidebar, AdminLayout


class AdminSidebar(Sidebar):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = AdminLayout(self)
        self.setLayout(self.layout)

        self.setFixedWidth(self.layout.collapsedWidth)
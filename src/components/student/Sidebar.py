from src.components.Sidebar import Sidebar, StudentLayout


class StudentSidebar(Sidebar):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = StudentLayout(self)
        self.setLayout(self.layout)

        self.setFixedWidth(self.layout.collapsedWidth)
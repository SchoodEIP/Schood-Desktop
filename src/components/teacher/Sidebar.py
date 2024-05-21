from src.components.Sidebar import Sidebar, TeacherLayout


class TeacherSidebar(Sidebar):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = TeacherLayout(self)
        self.setLayout(self.layout)

        self.setFixedWidth(self.layout.collapsedWidth)

from src.components.Sidebar import Sidebar, AdmLayout


class AdmSidebar(Sidebar):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = AdmLayout(self)
        self.setLayout(self.layout)

        self.setFixedWidth(self.layout.collapsedWidth)
from src.stores import stores


class SurveyStore:
    def __init__(self):
        self.selected = None
        self.id = ""
        self.questions = []

    def get_questions(self):
        return self.questions
    

    def fetch_questions(self):
        if self.questions == "":
            return []
        self.questions = stores.request.get("/shared/questionnaire/:id").json()
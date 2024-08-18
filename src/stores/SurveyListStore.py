from src.stores import stores


class SurveyListStore:
    def __init__(self):
        self.selected = None
        self.surveyList = []

    def get_surveyList(self):
        return self.surveyList

    def fetch_surveyList(self):
        if self.surveyList == "":
            return []
        self.surveyList = stores.request.get("/shared/questionnaire/").json()
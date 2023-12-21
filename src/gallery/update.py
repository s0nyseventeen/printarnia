from src.lib.abstractview import AbstractView


class AbstractUpdate(AbstractView):
    def __init__(self, model, template):
        self.model = model
        self.template = template

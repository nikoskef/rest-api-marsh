from uuid import uuid4

from admin.modelview import MyModelView


class ConfirmationView(MyModelView):
    def _on_model_change(self, form, model, is_created):
        model.id = uuid4().hex

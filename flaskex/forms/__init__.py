from wtforms.fields import TextField
from wtforms import Form


class TrimTextField(TextField):
    def process_formdata(self, *args, **kwargs):
        super(TrimTextField, self).process_formdata(*args, **kwargs)
        if self.data:
            self.data = self.data.strip()


class AjaxForm(Form):
    def errors_to_json(self):
        errors = {}
        for field in self:
            if field.errors:
                errors[field.name] = field.errors
        return errors

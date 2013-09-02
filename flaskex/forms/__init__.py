from flask.ext.wtf import TextField


class TrimTextField(TextField):
    def process_formdata(self, *args, **kwargs):
        super(TrimTextField, self).process_formdata(*args, **kwargs)
        if self.data:
            self.data = self.data.strip()

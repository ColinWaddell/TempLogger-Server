from multiselectfield import MultiSelectField

class MultiSelectCustomField(MultiSelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_val_from_obj(self, model):
        days = model.get_day_list()
        return days
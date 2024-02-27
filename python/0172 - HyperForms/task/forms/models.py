from django import forms
from django.db import models
from django.utils import timezone

from forms.constants import FORM_PARTICIPANTS_NAME, FIELD_TYPE_TEXT, FIELD_TYPE_NUMBER, FIELD_TYPES


def create_default_register_fields():
    form_model, _ = FormModel.objects.get_or_create(name=FORM_PARTICIPANTS_NAME)
    FormField.objects.bulk_create([
        FormField(form=form_model, name='name', label='Your name', type=FIELD_TYPE_TEXT),
        FormField(form=form_model, name='age', label='Your age', type=FIELD_TYPE_NUMBER),
        FormField(form=form_model, name='favorite_book', label='Your favorite book', type=FIELD_TYPE_TEXT),
    ])


class FormModel(models.Model):
    name = models.CharField(max_length=255)

    @classmethod
    def generate_dynamic_form_class(cls, form_name):
        form_fields = FormField.objects.filter(form__name=form_name)

        # WARNING: it exists only because of a requirement that asks for a dynamic form,
        # but for some reason tests don't create necessary fields before testing
        if form_name == FORM_PARTICIPANTS_NAME and not form_fields.exists():
            create_default_register_fields()

        fields = {
            field.name: cls.create_form_field_class(field) for field in form_fields
        }
        return type('DynamicForm', (forms.BaseForm,), {'base_fields': fields})

    @staticmethod
    def create_form_field_class(field):
        if field.type == FIELD_TYPE_TEXT:
            return forms.CharField(label=field.label, max_length=255)
        if field.type == FIELD_TYPE_NUMBER:
            return forms.IntegerField(label=field.label)

        raise ValueError(f'Unknown field type: {field.type}')

    def __str__(self):
        return f'Model(name={self.name})'


class FormField(models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=FIELD_TYPES)
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)

    @classmethod
    def get_fields_by_form_name(cls, form_name):
        return cls.objects.filter(form__name=form_name)

    def __str__(self):
        return f'Field(name={self.name}, label={self.label}, type={self.type})'


class FormRecord(models.Model):
    date = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_all_records(cls):
        records = cls.objects.prefetch_related('formdata_set').all()
        return [
            {field.field.name: field.value for field in record.formdata_set.all()}
            for record in records
        ]

    def __str__(self):
        return f'Record(date={self.date})'


class FormData(models.Model):
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    record = models.ForeignKey(FormRecord, on_delete=models.CASCADE)

    @classmethod
    def create_data(cls, form):
        record = FormRecord.objects.create()
        cls.objects.bulk_create([
            cls(
                form=field_instance.form,
                field=field_instance,
                value=value,
                record=record
            )
            for field_name, value in form.cleaned_data.items()
            for field_instance in FormField.objects.filter(name=field_name)
        ])

    def __str__(self):
        return f'Field(name={self.field.name}, value={self.value}, record_id={self.record.id})'

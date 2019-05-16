def get_form(form_obj):
    from django import forms

    class save_form(object):
        def save(self):
            pass

    fields = {}

    for form_field in form_obj.fields.filter(active=True):
        if form_field.field_type == 'text':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'radio':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'checkbox':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'date':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'number':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'money':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'textarea':
            fields[form_field.name] = forms.CharField()
        if form_field.field_type == 'select':
            fields[form_field.name] = forms.CharField()

    # Create form with previously created set of fields
    form = type('WorkflowForm', (forms.Form, save_form), fields)

    # Return a copy of the derived form class
    return form

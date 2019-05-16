def get_form(form_obj):
    try:
        from django.urls import reverse
    except ImportError:
        from django.core.urlresolvers import reverse
    from django import forms
    from django.http import HttpResponseRedirect

    class save_form(object):
        def save(self, request, odl=None):
            return HttpResponseRedirect(request.POST.get('next_url', reverse('dashboard')))

    fields = {}
    field_types = {
        'text': forms.CharField,
        'radio': forms.CharField,
        'checkbox': forms.CharField,
        'date': forms.CharField,
        'number': forms.CharField,
        'money': forms.CharField,
        'textarea': forms.CharField,
        'select': forms.CharField,
        'signature': forms.CharField,
        'file': forms.CharField,
    }

    for form_field in form_obj.fields.filter(active=True):
        field_kwargs = {'required': form_field.required}
        fields[form_field.name] = field_types.get(form_field.field_type)
        if fields[form_field.name] is not None:
            fields[form_field.name] = fields[form_field.name](**field_kwargs)

    # Create form with previously created set of fields
    form = type('WorkflowForm', (forms.Form, save_form), fields)

    # Return a copy of the derived form class
    return form

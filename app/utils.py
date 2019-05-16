def get_form(form_obj):
    try:
        from django.urls import reverse
    except ImportError:
        from django.core.urlresolvers import reverse
    from django import forms
    from django.http import HttpResponseRedirect

    from jsignature.forms import JSignatureField
    from jsignature.widgets import JSignatureWidget

    class save_form(object):
        def save(self, request, odl=None):
            request.session['flash_alerts'].append({'msg': 'Saved successfully', 'type': 'success'})
            return HttpResponseRedirect(request.POST.get('next_url', reverse('dashboard')))

    fields = {}
    field_types = {
        'text': forms.CharField,
        'radio': forms.ChoiceField,
        'checkbox': forms.MultipleChoiceField,
        'date': forms.DateField,
        'number': forms.DecimalField,
        'textarea': forms.CharField,
        'select': forms.ChoiceField,
        'signature': JSignatureField,
        'file': forms.FileField,
    }

    for form_field in form_obj.fields.filter(active=True):
        field_kwargs = {'required': form_field.required}
        if form_field.field_type == 'select':
            field_kwargs['choices'] = [('no', 'No'), ('yes', 'yes')]

        elif form_field.field_type == 'radio':
            field_kwargs['widget'] = forms.widgets.RadioSelect
            field_kwargs['choices'] = [('no', 'No'), ('yes', 'yes')]

        elif form_field.field_type == 'checkbox':
            field_kwargs['widget'] = forms.widgets.CheckboxSelectMultiple
            field_kwargs['choices'] = [('no', 'No'), ('yes', 'yes')]

        elif form_field.field_type == 'textarea':
            field_kwargs['widget'] = forms.widgets.Textarea

        elif form_field.field_type == 'signature':
            field_kwargs['widget'] = JSignatureWidget(jsignature_attrs={'decor-color': '#000'})

        fields[form_field.name] = field_types.get(form_field.field_type)
        if fields[form_field.name] is not None:
            fields[form_field.name] = fields[form_field.name](**field_kwargs)

    # Create form with previously created set of fields
    form = type('WorkflowForm', (forms.Form, save_form), fields)

    # Return a copy of the derived form class
    return form

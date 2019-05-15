try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class LegalAgreementCheckInput(forms.CheckboxInput):
    def __init__(self, attrs=None, check_test=None):
        super(LegalAgreementCheckInput, self).__init__(attrs, check_test)

    def instance_check(self):
        self.has_instance = False
        if hasattr(self, 'instance'):
            self.has_instance = True
        return self.has_instance

    def render(self, name, value, attrs=None):
        if self.instance_check() and self.instance.sign:
            attrs.update({
                'class': 'require-signing',
                'data-legal-id': self.instance.id,
                'data-user-id': self.instance.id
            })

        html = '<div class="checkboxRow">' + super(LegalAgreementCheckInput, self).render(name, value, attrs)
        pdf = ''
        extra_attrs = '' if self.extra_attrs is None else 'data-load_data="%s"' % self.extra_attrs
        if self.instance.pdf:
            pdf = ' data-pdf="' + self.instance.pdf.url + '"'

        if self.instance_check():
            signed = ' signed' if value else ''
            extra_html = ' <span>I have read and agree to the terms in the '
            extra_html += '<a href="%s" target="_blank" class="legal-link%s"%s%s>%s</a></span>'
            html += extra_html % (self.instance.get_slug, signed, pdf, extra_attrs, self.instance.label)

        else:
            html += str(name).title()
        html += '<div class="clear"></div></div>'
        return mark_safe(html)

    class Media:
        js = ('js/form-widgets/legalagreement.js', 'js/jsignature/jSignature.js')
        css = {
            'all': ('styles/form-widgets/legalagreement.css',),
        }


class LegalAgreementCheckField(forms.BooleanField):
    widget = LegalAgreementCheckInput

    def __init__(self, agreement, required=True, widget=None, label=None, initial=None, help_text='', *args, **kwargs):
        widget_attrs = kwargs.pop('widget_attrs', None)
        super(LegalAgreementCheckField, self).__init__(
            required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)

        # Set Field / Widget variables
        self.instance = self.widget.instance = agreement
        self.widget.extra_attrs = widget_attrs


# Setup Wizard Legal Agreement form
class LegalAgreementForm(forms.Form):
    def __init__(self, agreements=[], *args, **kwargs):
        super(LegalAgreementForm, self).__init__(*args, **kwargs)
        for agreement in agreements:
            widget_attrs = None
            if isinstance(agreement, (tuple, list)) and len(agreement) == 2:
                # split list/tuple into multiple values
                agreement, widget_attrs = agreement

            field_kwargs = {'agreement': agreement, 'label': agreement.label, 'required': True}
            if hasattr(agreement, 'initial'):
                field_kwargs['initial'] = agreement.initial

            if widget_attrs is not None:
                field_kwargs['widget_attrs'] = widget_attrs

            self.fields[agreement.slug] = LegalAgreementCheckField(**field_kwargs)

    form_label = "Agreements"
    step_required = True


class CheckCompletionForm(forms.Form):
    valid_code = forms.CharField(label=_("Please enter the code to continue:"), required=True)

    @staticmethod
    def get_initial(request, **kwargs):
        initial_data = {}
        return initial_data

    def __init__(self, step, *args, **kwargs):
        self.step = step
        super(CheckCompletionForm, self).__init__(*args, **kwargs)

    def clean_valid_code(self):
        value = self.cleaned_data.get("valid_code")
        if value != self.step.completion_code:
            raise forms.ValidationError('Invalid Code')

    def save(self, request=None, commit=True):
        msg = 'Saved successfully'
        request.session['flash_alerts'].append({'msg': msg, 'type': 'success'})
        return HttpResponseRedirect(request.POST.get('next_url', reverse('dashboard')))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import os

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from app.encrypt import EncryptionService, ValidationError
from app.files import secure_storage


# Create your models here.
class BaseModel(models.Model):
    '''
        This is going to be the new base model
        The django auto_now and auto_now_add do not operate as expected.
        They tend to give inaccurate results for date this abstract model addresses that issue.
    '''
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)


@python_2_unicode_compatible
class LegalAgreement(BaseModel):
    # company = models.ForeignKey(Company, null=True, default=None, blank=True, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default='')
    slug = models.CharField(max_length=100, default='')
    content = models.TextField(default='', blank=True)
    pdf = models.FileField(upload_to="legal", default='', blank=True)
    sign = models.BooleanField(default=False)
    is_linked = models.BooleanField(default=False)
    publicly_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    @property
    def get_slug(self):
        return '/legal/' + str(self.slug) + '/'

    def get_content(self):
        if self.pdf:
            self.pdf.open('rb')
            return self.pdf.read()

        else:
            return self.content

    def get_content_hash(self):
        hash = hashlib.sha1()
        if self.pdf:
            try:
                self.pdf.open('rb')
            except IOError:
                return hash.hexdigest()

            if self.pdf.multiple_chunks():
                for chunk in self.pdf.chunks():
                    hash.update(chunk)

            else:
                hash.update(self.pdf.read())

        else:
            hash.update(self.content)

        return hash.hexdigest()


def secure_upload_path(instance, filename):
    return os.path.join('', 'user-docs', 'user-' + str(instance.user.id), filename)


@receiver(pre_save, sender=LegalAgreement)
def onLegalAgreementSave(sender, instance, **kwargs):
    # force existance of slug
    if instance.slug.strip() == '':
        instance.slug = instance.label.lower().replace(' ', '-')

    slug = instance.slug.strip()
    if slug == '' or LegalAgreement.objects.filter(slug=instance.slug).exclude(id=instance.id).exists():
        raise Exception('Duplicate slug')


@python_2_unicode_compatible
class SecureUpload(BaseModel):
    name = models.CharField(max_length=200, default='')
    upload = models.FileField(upload_to=secure_upload_path, storage=secure_storage, default=None, null=True)

    def __str__(self):
        return self.name

    @property
    def has_thumbnail(self):
        if self.upload != '':
            return True if secure_storage.exists(self.upload.path + '-thumb.png') else False

        else:
            return False

    @property
    def get_thumbnail(self):
        if self.upload != '':
            return reverse('secure_upload_download', kwargs={'res_id': self.id})

        else:
            return False

    def save(self, *args, **kwargs):
        if self.pk:
            changed_fields = kwargs.get('update_fields', [])
        else:
            changed_fields = kwargs.pop('update_fields', [])

        super(SecureUpload, self).save(*args, **kwargs)
        if 'upload' in changed_fields:
            try:
                service = EncryptionService()
                enc_file = service.encrypt_file(self.upload, settings.SECURE_PASS)
            except ValidationError:
                raise
            else:
                dir_name, file_name = os.path.split(enc_file.name)
                new_name = os.path.join(dir_name, 'tmp_' + file_name)
                os.rename(enc_file.name, new_name)
                enc_file.name = new_name

                self.upload.save(os.path.join(dir_name, file_name), enc_file)
                os.unlink(new_name)


@python_2_unicode_compatible
class PdfGeneration(BaseModel):
    PAGESIZES = (
        ('LETTER', "Letter"),
        ('LEGAL', "Legal"),
        ('A4', "A4")
    )

    name = models.CharField(max_length=100, default='')
    pdf_file = models.FileField(upload_to='pdf_generation', storage=secure_storage, default=None, null=True)
    pagesize = models.CharField(max_length=100, default=PAGESIZES[0][0], choices=PAGESIZES, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PdfGenerationField(BaseModel):
    FIELD_TYPES = (
        ('string', "Text Field"),
        ('signature', "Signature"),
        ('checkbox', "Checkbox"),
        ('image', "Image Field")
    )
    pdf = models.ForeignKey(PdfGeneration, models.CASCADE, default=None, null=True)
    page_number = models.PositiveIntegerField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    field_type = models.CharField(max_length=100, default=FIELD_TYPES[0][0], choices=FIELD_TYPES)
    field_model = models.ForeignKey(ContentType, models.CASCADE, default=None, null=True)
    field_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return 'PDF Field for %s' % self.pdf.name


@python_2_unicode_compatible
class WorkflowWizard(BaseModel):
    # company = models.ForeignKey(Company, models.CASCADE, null=True, default=None, blank=True)
    is_template = models.BooleanField(default=False)
    name = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class WorkflowWizardStep(BaseModel):
    name = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    agreement = models.ForeignKey(LegalAgreement, models.CASCADE, null=True, default=None, blank=True)
    completion_code = models.CharField(max_length=100, default='', blank=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=2000)

    workflow_wizard = models.ForeignKey(WorkflowWizard, models.CASCADE, 'steps', null=True, default=None)
    employer = models.BooleanField(default=False, verbose_name="Employer Step")
    pdfgen = models.ManyToManyField(PdfGeneration, blank=True, verbose_name="PDF Forms (Generated)")
    form = models.ForeignKey('WorkflowWizardForm', models.CASCADE, default=None, null=True)
    # upload = models.ManyToManyField(SecureUpload, blank=True)

    def __str__(self):
        return self.name

    def check_completion(self, odl):
        if self.agreement:
            return None

        elif self.form_name:
            return None

        else:
            return None

        return False

    class Meta:
        ordering = ['workflow_wizard__id', 'ordering']


@python_2_unicode_compatible
class WorkflowWizardForm(BaseModel):
    name = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class WorkflowWizardFormField(BaseModel):
    FIELD_TYPES = (
        ('text', 'Text Field'), ('radio', 'Radio'),
        ('checkbox', 'Checkbox'), ('date', 'Date Field'),
        ('number', 'Number Field'), ('money', 'Money Field'),
        ('textarea', 'Text Area'), ('select', 'Select Box'),
    )
    form = models.ForeignKey(WorkflowWizardForm, models.CASCADE, 'fields', default=None, null=True)
    name = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    field_type = models.CharField(max_length=100, default=FIELD_TYPES[0][0], choices=FIELD_TYPES)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return self.name

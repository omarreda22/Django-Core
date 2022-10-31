from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify


from .models import Post


TEXT_SELECTOR = [
    ('First', 'First'),
    ('First', 'First'),
    ('First', 'First'),
]

RANGE_YEAR = [x for x in range(1980, 2022)]

# if you need widget you wanna check out in documention


class TestForm(forms.Form):
    text = forms.CharField()
    text_area = forms.CharField(
        widget=forms.Textarea(attrs={'row': 4, 'cols': 4}))

    text_select = forms.CharField(widget=forms.Select(choices=TEXT_SELECTOR))
    text_select_checkbox = forms.CharField(
        widget=forms.CheckboxSelectMultiple(choices=TEXT_SELECTOR))
    text_select_radio = forms.CharField(
        widget=forms.RadioSelect(choices=TEXT_SELECTOR))
    text_select_mult = forms.CharField(
        widget=forms.SelectMultiple(choices=TEXT_SELECTOR))

    text_date = forms.CharField(widget=forms.SelectDateWidget())
    text_date_range_year = forms.CharField(
        widget=forms.SelectDateWidget(years=RANGE_YEAR))
    text_date_with_initial = forms.CharField(initial="2001-9-26",
                                             widget=forms.SelectDateWidget(years=RANGE_YEAR))

    # image = forms.ImageField()
    time = forms.TimeField(initial=timezone.now())

    number = forms.IntegerField()
    number_choices = forms.IntegerField(widget=forms.Select(
        choices=[tuple([x, x]) for x in range(1, 100)]))
    number_choices_inital = forms.IntegerField(widget=forms.Select(
        choices=[tuple([x, x]) for x in range(1, 100)]), initial=9)

    boolean = forms.BooleanField(required=False)
    email = forms.EmailField(min_length=8)

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        # self.fields['text'].initial = 'From Inital Class'

        for field in self.fields:
            if field == 'text_select_checkbox' or field == 'text_select_radio':
                continue
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'margin-bottom:10px'

        self.fields['text'].widget.attrs['placeholder'] = 'Enter Some Test Text'
        self.fields['number'].widget.attrs['placeholder'] = 'Enter Test Number'
        self.fields['email'].widget.attrs['placeholder'] = '@Emaple.com'

    def clean_number(self, *args, **kwargs):
        num = self.cleaned_data.get('number')
        if num == 9:
            raise ValidationError("Number must not equal '9'")
        return num

    def clean_text(self, *args, **kwargs):
        text = self.cleaned_data.get('text')
        if 'shit' in text:
            raise ValidationError("Can't Us this word")

        if 'fuck' in text:
            raise ValidationError("Can't Us this word2")

        if len(text) <= 5:
            raise ValidationError('Must bigger than 5 char')

        return text


class PostModelForm(forms.ModelForm):
    # widget=forms.Textarea()
    # slug = forms.SlugField(
    #     error_messages={"unique": "This is fields must be unique!!!"},
    #     help_text="This Must",
    #     label='Slugg')
    # height_field = forms.IntegerField(label='Height')
    # width_field = forms.IntegerField(label='Width')
    # publish = forms.DateField(initial=timezone.now())

    class Meta:
        model = Post
        # fields = [
        #     'title',
        #     'height_field',
        #     'width_field',
        #     'content',
        #     'draft',
        # ]
        exclude = ['user', 'publish']
        labels = {
            'title': 'Title',
            'slug': 'Slug',
            'height_field': 'Height'
        }
        # help_text = {
        #     'title': 'O Title',
        #     'slug': 'O Slug',
        # }
        # error_messages = {
        #     'slug': {
        #         'unique': 'Must'
        #     }
        # }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'shit' in title:
            raise ValidationError("Don't use this shit word")
        return title

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)

        #################################
        # for field in self.fields.values():
        #     field.widget.attrs['class'] = 'form-control'
        #################################
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-bottom:15px'
            field.widget.attrs['placeholder'] = f'{field.label}'
            field.label = f'{field.label.upper()}'

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'
        #     self.fields[field].widget.attrs['style'] = 'margin-bottom:15px'

    def save(self, commit=True, *args, **kwargs):
        obj = super(PostModelForm, self).save(commit=False, *args, **kwargs)
        obj.slug = slugify(obj.title)
        obj.publish = timezone.now()
        if commit:
            obj.save()
        return obj

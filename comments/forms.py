from django import forms


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(label='')
    email = forms.EmailField(widget=forms.HiddenInput)
    # parent_id = forms.CharField(widget=forms.HiddenInput)

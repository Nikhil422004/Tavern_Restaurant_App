from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search for menu items...',
        'class': 'searchInput'
    }))

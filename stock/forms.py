from django import forms

class SearchKeywordForm(forms.Form):
    search_keyword = forms.CharField(max_length=100)

    def clean_search_keyword(self):
        data = self.cleaned_data['search_keyword']
        #check data
        return data


class PerInputForm(forms.Form):
    per_value = forms.IntegerField()

    def clean_per_value(self):
        data = self.cleaned_data['per_value']
        if data < 0:
            data *= -1
        elif data == 0:
            data = 10
            
        #check data
        return data

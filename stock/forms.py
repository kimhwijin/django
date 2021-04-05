from django import forms

from stock.django_crawler import NameToCode

class SearchKeywordForm(forms.Form):
    search_keyword = forms.CharField(max_length=100)

    def clean_search_keyword(self):
        print("clean_search_keyword")
        data = self.cleaned_data['search_keyword']
        #종목명 검색
        if not (len(data) == 6 and data.isdigit()):
            data = NameToCode(data)[1:]
        #check data
        print(data)
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

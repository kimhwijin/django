from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from stock.models import StockInfo
from django.http  import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

#template
class StockModelView(TemplateView):
    template_name = 'stock/stockinfo_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_list"] = ['StockInfo',]
        return context

#favor stock list view
from stock import django_crawler
def StockInfo_List_View(request):
    stockinfo_list = StockInfo.objects.all().order_by('id')
    context_list = []

    for stockinfo in stockinfo_list:
        temp_list = django_crawler.get_listinfo(stockinfo.code)
        context_list.append((temp_list))
    context = {
        'object_info_list' : context_list,
    }
    print('list')
    return render(request, 'stock/stockinfo_list.html', context)


#
import json
def StockInfo_Detail_View(request,code_number):

    stockinfo = get_object_or_404(StockInfo,code=code_number)

    
    detailinfo = django_crawler.get_all_detail_info(code_number)
    chartinfo = django_crawler.get_chart_info(code_number)
    chart_close_info = json.dumps(list(chartinfo.to_dict()['Close'].values()))
    chart_date_info = json.dumps(list(chartinfo.to_dict()['Date'].values()))
    print(chart_close_info)
    print(chart_date_info)

    #example plotly graph
    '''
    x = [-2,0,4,6,7]
    y = [q**2-q+3 for q in x]
    trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                        mode="lines",  name='1st Trace')

    data=go.Data([trace1])
    layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div')
    #--
    '''
    context = {
        'stockinfo' : stockinfo,
        'detailinfo' : detailinfo,
        'deltaprice' : django_crawler.get_price_info(code_number),
        'chartcloseinfo': chart_close_info,
        'chartdateinfo': chart_date_info,
        'graph': django_crawler.makeGraph(code_number),
        'dataframe' : django_crawler.todayRatio().values.tolist(),
    }


    print('detail')
    return render(request,'stock/stockinfo_detail.html',context)


from stock.forms import SearchKeywordForm


#
def Search_Info(request):
    search_keyword_form = SearchKeywordForm(request.GET)
    kw_valid = False
    temp_list = []

    if search_keyword_form.is_valid():
        skw = search_keyword_form.cleaned_data['search_keyword']
        if len(skw) == 6 and skw.isdigit():
            kw_valid = True
            detail_info = django_crawler.get_all_detail_info(skw)
            list_info = django_crawler.get_listinfo(skw)
    else:
        skw = 'form_invalid'
    
    context = {
        'search_keyword' : skw,
        'keyword_valid' : kw_valid,
        'listinfo':list_info,
        'detailinfo': detail_info,
    }
    print('search')
    return render(request, 'stock/stockinfo_search_result.html', context)

#
def Save_Favor(request,stock_name,code_number):
    print('save')
    StockInfo.objects.create(name=stock_name, code=code_number)
    return HttpResponseRedirect(reverse('stock:stockinfo_detail', args=[code_number,]))

#
def Delete_Favor(request,pk):
    print('delete')
    StockInfo.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('stock:stockinfo_list'))


#전체 주식관련정보 로딩 함수
def Total_Init(request):
    print('init')
    #세션 확인
    #세션 저장
    request.session['test'] = "hahaha"
    #request.session['df'] = json.loads(django_crawler.todayRatio()),
    request.session['sort'] = "외국인"
    #세션 존재
    return HttpResponseRedirect(reverse('stock:total_stockdata_home'))

import pandas as pd

def Total_Home(request):
    print('home')
    context = {
        'test' : request.session['test'],
        #'df' : df.values.tolist(),
        'dataframe' : django_crawler.todayRatio().values.tolist(),
        'sort' : request.session['sort'],
    }

    return render(request, 'stock/total_home.html', context)

def Total_SessionChange(request):
    #code 상장주식수 당일외국인순매수 당일기관당순매수 외국인순매수비율 기관순매수비율
    print('SessionChanging')
    if request.session['sort'] == "외국인":
        request.session['sort'] = "기관"
        sorted(request.session['df'], key=lambda x: x[5])
    elif request.session['sort'] == "기관":
        request.session['sort'] = "외국인"
        sorted(request.session['df'], key=lambda x: x[4])

    return HttpResponseRedirect(reverse('stock:total_stockdata_home'))
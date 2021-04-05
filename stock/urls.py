from django.urls import path
from stock import views

app_name = 'stock'
urlpatterns = [
    #/stock/
    path('',views.StockModelView.as_view(), name='index'), #home
    #/stock/stockinfo/
    path('stockinfo/',views.StockInfo_List_View, name='stockinfo_list'), #관심목록 리스트
    #/stock/stockinfo/<str:code>
    path('stockinfo/detail/<str:code_number>/',views.StockInfo_Detail_View, name='stockinfo_detail'), #개별종목 디테일뷰
    #path('stockinfo/detail/<int:pk>',views.Delete_Favor, name='delete_favor'), #관심 목록삭제

    #total
    path('stockinfo/total/index',views.Total_Init, name='total_stockdata_index'),
    path('stockinfo/total/home',views.Total_Home, name='total_stockdata_home'),
    
    #PER CHANGE
    path('modify/<str:code_number>',views.Change_Per, name='change_per'),

    #search
    path('search/',views.Search_Info, name='search_info'),
    path('search/<str:stock_name>/<str:code_number>',views.Save_Favor, name='save_favor'),

    path('favor_detail/favor/<int:pk>',views.Delete_Favor, name='delete_favor'),

]
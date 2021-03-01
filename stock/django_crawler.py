import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_listinfo(code_number):
    #종목코드에 따른 현재가, 등락폭(listview에 필요한)을 가져온다.
    #input : (str)종목번호 , output : list [종가/ 전일대비 , 거래량]
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임

    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.select('.corp_group1 > h1') # '.'은 BeautifulSoup에서 태그를 추출할때 사용하는 것임.
    name_2 = str(name) # name이 리스트 형식이여서 문자열로 변경
    name_3 = name_2.split('<') # '<' 기호를 기준으로 나누었음
    name_last = name_3[1] # 나눈 것 중 2번째에 있는 리스트 선택
    name_last = name_last.split('>') # 선택한 것을 다시 '>' 기호를 기준으로 나누었음
    name_last = str(name_last[1]) #종목명만 다시 name_last에 저장


    info_list = []
    info_list.append(name_last)
    info_list.append(code_number)

    #종가, 전일대비, 거래량 내용을 추출/ 시세현황 테이블
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr.rwf > td' )
    for ifrs_data in ifrs:
        info_list.append(ifrs_data.get_text())
    print(info_list)
    return info_list

def get_all_detail_info(code_number):
    #종목코드에 따른 디테일한 정보를 전부 가져옴.
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임

    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    #기본 정보 0 
    detail_info = []
    group_info = []
    ifrs = soup.select('div.corp_group2 > dl > dd')
    for ifrs_data in ifrs:
        group_info.append(ifrs_data.text)
    detail_info.append(group_info)

    #시세현황 1
    group_info = []
    ifrs = soup.select('#svdMainGrid1 > table > tbody > tr')
    for ifrs_data in ifrs:
        ifrs_data = ifrs_data.select('td')
        for ifrs_data_td in ifrs_data:
                group_info.append(ifrs_data_td.text)
    detail_info.append(group_info)
    
    #실적이슈 2
    group_info = []
    ifrs = soup.select('#svdMainGrid2 > table > tbody > tr > td')
    for ifrs_data in ifrs:
        group_info.append(ifrs_data.get_text())
    detail_info.append(group_info)

 
    #운용사별 보유현황 3 
    group_info = []
    ifrs = soup.select('#svdMainGrid3 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = [ifrs_tr.select_one('th').text]
        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)

    #주주현황 4 
    group_info = []
    ifrs = soup.select('#svdMainGrid4 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = []
        temp = ifrs_tr.select_one('th > div')
        if temp.string == None:
            inst_list.append(temp.select_one('a').text)
        else:
            inst_list.append(temp.text)

        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)
    
    #주주구분현황 5
    group_info = []
    ifrs = soup.select('#svdMainGrid5 > table > tbody > tr')
    for ifrs_tr in ifrs:
        inst_list = []
        temp = ifrs_tr.select_one('th > div')
        if temp.string == None:
            inst_list.append(temp.select_one('a').text)
        else:
            inst_list.append(temp.text)
        
        ifrs_tds = ifrs_tr.select('td')
        for ifrs_td in ifrs_tds:
            inst_list.append(ifrs_td.text)
        group_info.append(inst_list)
    detail_info.append(group_info)

    print(detail_info)

    return(detail_info)

#가격변동 정보
def get_price_info(code_number):

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    base_url = 'http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}' #{}안에 종목코드가 들어갈 것임
    
    url = base_url.format(code_number)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')

    ifrs = soup.select_one('#svdMainGrid1 > table > tbody > tr.rwf > td.r > span')
    delta_price = ifrs.text
    print(delta_price)
    if delta_price[0] == '-':
        return False
    elif delta_price[0] == '+':
        return True


#차트정보
import datetime
def get_chart_info(code_number):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Whale/2.7.99.20 Safari/537.36'}
    count = 10
    timeframe = 'day'
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={}&timeframe={}&count={}&requestType=0".format(code_number,timeframe,count)
    get_result = requests.get(url,headers = headers)
    bs_obj = BeautifulSoup(get_result.content, "html.parser")
    inf = bs_obj.select('item')
    columns = ['Date', 'Open' ,'High', 'Low', 'Close', 'Volume']
    df_inf = pd.DataFrame([], columns = columns, index = range(len(inf)))
    for i in range(len(inf)):
        df_inf.iloc[i] = str(inf[i]['data']).split('|')
    
    return df_inf.drop(['Open','High','Low'], axis=1)


import win32com.client
import time
from datetime import datetime
import pandas as pd
from pandas.tseries.offsets import *
import plotly.graph_objs as go
from pywinauto import application
import time
import os
from datetime import datetime

def makeGraph(code_number):

    # 증권사 API 자동 실행
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    time.sleep(5)        

    app = application.Application()
    app.start('C:\CREON\STARTER\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwd} /autostart'.format(
    id='sheee7', pwd='sh5167!!'))
    time.sleep(60)

    # 서버 접속 확인
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect

    if (bConnect == 1): #접속 - 1, 비접속 - 0
        print("서버가 정상적으로 접속되었습니다.")
    else:
        print("서버가 정상적으로 연결되지 않았습니다. ")
        exit(0)
    #testdf = pd.read_excel('21.01.12_stock_data.xlsx')
    #testdf = pd.read_excel('21.01.29_stock_data.xlsx')
    testdf = pd.read_excel(os.getcwd() + '\\stock\\21.02.05_stock_data.xlsx')
    # 종목명 -> 종목코드 변환
    instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
    stock_code = code_number
    stock_name = instCpStockCode.CodeToName(stock_code)
    per = 50
    table_name = stock_name

    now = time.strftime('%Y%m%d')

    stock_pastday = '20150101'
    stock_presentday = now

    # 오브젝트 가져오기
    inStockMst = win32com.client.Dispatch("dscbo1.StockMst") #현재 미사용
    inStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    inStockChart.SetInputValue(0, stock_code) # 종목 코드 - 삼성전자
    inStockChart.SetInputValue(1, ord('1')) # 기간으로 확인
    inStockChart.SetInputValue(2, stock_presentday) # 최신일자
    inStockChart.SetInputValue(3, stock_pastday) # 과거일자
    inStockChart.SetInputValue(5, [0,2,3,4,5,8]) # 날짜,시가,고가,저가,종가,거래량
    inStockChart.SetInputValue(6, ord('D')) # 차트 주가 - 일간 차트 요청
    inStockChart.SetInputValue(9, ord('1')) # 수정주가 사용

    inStockChart.BlockRequest()

    len = inStockChart.GetHeaderValue(3)

    data = []

    for i in range(len):
        line = []  # 안쪽 리스트로 사용할 빈 리스트 생성
        date = inStockChart.GetDataValue(0, i)  # 날짜
        open = inStockChart.GetDataValue(1, i)  # 시가
        high = inStockChart.GetDataValue(2, i)  # 고가
        low = inStockChart.GetDataValue(3, i)  # 저가
        close = inStockChart.GetDataValue(4, i)  # 종가
        vol = inStockChart.GetDataValue(5, i)  # 거래량

        line.append(date)  # 리스트에 내용 추가
        line.append(open)
        line.append(high)
        line.append(low)
        line.append(close)
        line.append(vol)
        data.append(line)  # 전체 리스트에 안쪽 리스트를 추가

    labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    # 리스트 형태를 라벨이 있는 데이터프레임으로 변환하는 내용
    df1 = pd.DataFrame.from_records(data, columns=labels)
    # Date 일자를 문자열로 변환
    df1['Date'] = df1['Date'].astype('str')
    # datetime 를 이용해서 날짜로 변환
    df1['Date'] = pd.to_datetime(df1['Date'])
    #df1.info()

    # 스크랩한 데이터에서 검색하려는 종목명과 일치하는 것을 찾아내기
    sam = (testdf['종목명'] == stock_name)
    ## SettingWithCopyWarning 오류 의심부분
    testdf_sam = testdf[sam].copy()
    # 스크랩한 데이터에서 '2019/12'가 포함되는 것을 찾아내기
    data2019 = (testdf['index'] == '2019/12')

    #testdf_data2019 = testdf[data2019]

    #data2021 = (testdf['발행주식수'] == '2021/12(E)')
    #testdf_data2021 = testdf[data2021]

    # 여러 조건에 부합되는 결과값 (& and // | or)
    # '종목명'과 '2019/12'가 포함된 데이터만 찾기
    testdf_total = testdf[sam & data2019].copy()
    #testdf_total

    #testdf_sam
    # API를 통해서 최신 발행주식수를 가져오는 것이 'Best'이지만... 코드가 많이 추가되니 간단하게 넘어감..ㅋㅋ
    # 스크랩한 데이터 중 발행주식수가 있으니 2019년의 발행주식수를 가져옴
    stock_num = testdf_total['발행주식수'].copy()
    stock_num = stock_num.values
    # 나만의 목표가 계산식
    testdf_sam['적정가격'] = round((testdf_sam['영업이익']*per *100000000 / (stock_num *1000) + (testdf_sam['EPS(원)']*per)) /2,-2)
    #testdf_sam[['index', '적정가격']]
    #testdf_sam['index'] = testdf_sam['index'].astype('str')

    # 적정가격을 차트상에 표시하기 위해 일자로 변경
    # 단순작업으로 바꾸는 코드... 이기 때문에 2024, 2025가 되더라도 작동하도록 수정할 것
    testdf_sam.loc[testdf_sam['index'] == '2020/12(P)','index'] ='2020/12'
    testdf_sam.loc[testdf_sam['index'] == '2020/12(E)','index'] ='2020/12'
    testdf_sam.loc[testdf_sam['index'] == '2021/12(E)','index'] ='2021/12'
    testdf_sam.loc[testdf_sam['index'] == '2022/12(E)','index'] ='2022/12'
    testdf_sam.loc[testdf_sam['index'] == '2023/12(E)','index'] ='2023/12'

    # datetime을 이용해 년/월 형식으로 수정함 (2020/12 -> 2020-12-01)
    testdf_sam['index'] = pd.to_datetime(testdf_sam['index'], format='%Y/%m')

    # 2019-12-01의 경우 일요일(주말)이라 차트상에 표시가 안되는 현상을 방지하고자, 일자를 바꿈
    testdf_sam['index'] = testdf_sam['index'] + Week(weekday=4)

    #testdf_sam[['index', '적정가격']]
    #testdf_sam

    # 현재주가 추출
    nowprice = df1.loc[0, 'Close']
    # 2021년 목표주가 추출(2022년 7)
    tp21 = testdf_sam.iloc[6, 33]
    tp22 = testdf_sam.iloc[7, 33]
    # 2021년 영업이익 추출
    op21 = testdf_sam.iloc[6, 2]
    op22 = testdf_sam.iloc[7, 2]
    # 목표주가 상승여력(퍼센트)
    tpper21 = round(((tp21-nowprice)/nowprice*100),2)
    tpper22 = round(((tp22-nowprice)/nowprice*100),2)

    title = stock_name + ' 목표주가 / PER ' + str(per) +' / '+ str(nowprice) +'원('+ str(tp21) + '원 ' + str(round(tpper21,2)) + '%, '+str(op21)+'억)'

    fig = go.Figure(data=[go.Candlestick(x=df1['Date'],
                    open=df1['Open'],
                    high=df1['High'],
                    low=df1['Low'],
                    close=df1['Close'])])

    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        title_text=title
    )

    fig.add_trace(go.Scatter(
        name="목표주가",
        mode="markers+lines", x=testdf_sam["index"], y=testdf_sam["적정가격"],
        xperiod="M1",
        xperiodalignment="middle"
    ))

    """
    fig.add_hline(y=80000, line_dash="dot",
                annotation_text="8만 전자",
                annotation_position="bottom right",
                annotation_font_size=15)

    fig.add_vrect(x0="2020-12-25", x1="2021-01-10", col=1,
                annotation_text="매수 기회", 
                annotation_position="top left",
                annotation_font_size=15, 
                annotation_font_color="red", 
                fillcolor="green", opacity=0.25, line_width=0)
    """

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends
            dict(values=["2020-12-25", "2021-01-01"])  # hide Christmas and New Year's
        ],
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig

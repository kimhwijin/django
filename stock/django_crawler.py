import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging

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

def get_chart_info(code_number):

    import datetime
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
import plotly.offline as opy
from pywinauto import application
import os

def makeGraph(code_number):
    print('debuging makegraph')
    # 증권사 API 자동 실행
    '''
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    time.sleep(5)        

    app = application.Application()
    #cp : creon plus , id : id, pwd : password
    app.start('C:\CREON\STARTER\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwd} /autostart'.format(
    id='sheee7', pwd='sh5167!!'))
    time.sleep(30)
    '''
    # 서버 접속 확인
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect

    if (bConnect == 1): #접속 - 1, 비접속 - 0
        print("서버가 정상적으로 접속되었습니다.")
    else:
        print("서버가 정상적으로 연결되지 않았습니다. ")
        exit(0)

    testdf = pd.read_excel(os.getcwd() + '\\stock\\21.02.05_stock_data.xlsx')
    #종목번호 -> 종목명
    instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
    if instCpStockCode:
        logging.error("CpUtil.CpStockCode이 실행중이지 않습니다.")
    
    stock_code = code_number
    stock_name = instCpStockCode.CodeToName(stock_code)

    #웹에서 받아옴
    per = 50
    table_name = stock_name

    now = time.strftime('%Y%m%d')

    stock_pastday = '20150101'
    stock_presentday = now

    # 오브젝트 가져오기
    inStockMst = win32com.client.Dispatch("dscbo1.StockMst") #현재 미사용
    inStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    #참고 http://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=StockChart&p=8841&v=8643&m=9505
    inStockChart.SetInputValue(0, 'A' + stock_code) # 0 - 종목 코드
    inStockChart.SetInputValue(1, ord('1')) # 1 - 요청구분 / 1 : 기간 2 : 개수
    inStockChart.SetInputValue(2, stock_presentday) # 2 - 요청종료일 YYYYMMDD형식의 데이터마지막날짜
    inStockChart.SetInputValue(3, stock_pastday) # 3 - 요청시작일 YYYYMMDD형식의 데이터처음날짜
    #4 - 요청 데이터의 개수
    inStockChart.SetInputValue(5, [0,2,3,4,5,8,12]) #5 - 가져올데이터의 종류 [날짜,시가,고가,저가,종가,거래량,상장주식수] url참고
    inStockChart.SetInputValue(6, ord('D')) # 6 - D : 일봉
    inStockChart.SetInputValue(9, ord('1')) # 9 - 1 : 수정주가 사용 , 0 : 무수정주가

    print(inStockChart)

    inStockChart.BlockRequest()

    # 3 - 수신개수
    cnt = inStockChart.GetHeaderValue(3)

    data = []

    for i in range(cnt):
        line = []  # 안쪽 리스트로 사용할 빈 리스트 생성
        #SetInputValue 의 type 5 에 해당하는 데이터
        line.append(inStockChart.GetDataValue(0, i)) # 날짜
        line.append(inStockChart.GetDataValue(1, i))  # 시가
        line.append(inStockChart.GetDataValue(2, i))  # 고가
        line.append(inStockChart.GetDataValue(3, i))  # 저가
        line.append(inStockChart.GetDataValue(4, i))  # 종가
        line.append(inStockChart.GetDataValue(5, i))  # 거래량
        #line.append(inStockChart.GetDataValue(6, i))  # 상장주식수

        data.append(line)  # 전체 리스트에 안쪽 리스트를 추가

    labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

    #data(list) -> df1(dataframe)
    
    df1 = pd.DataFrame.from_records(data, columns=labels)
    # Date 일자를 문자열로 변환
    df1['Date'] = df1['Date'].astype('str')
    # datetime 를 이용해서 날짜로 변환
    df1['Date'] = pd.to_datetime(df1['Date'])
    print('df1:::')
    print(df1)
    # 스크랩한 데이터에서 검색하려는 종목명과 일치하는 것을 찾아내기
    #sam
    is_stock_row = testdf['종목명'] == stock_name
    # 스크랩한 데이터에서 '2019/12'가 포함되는 것을 찾아내기
    is_data2019 = testdf['index'] == '2019/12'

    #testdf_data2019 = testdf[data2019]

    #data2021 = (testdf['발행주식수'] == '2021/12(E)')
    #testdf_data2021 = testdf[data2021]

    # 여러 조건에 부합되는 결과값 (& and // | or)
    # '종목명'과 '2019/12'가 포함된 데이터만 찾기
    testdf_total = testdf[is_stock_row & is_data2019]
    #모든기간의 종목데이터
    testdf_stock_row = testdf[is_stock_row]


    # API를 통해서 최신 발행주식수를 가져오는 것이 'Best'이지만... 코드가 많이 추가되니 간단하게 넘어감..ㅋㅋ
    # 스크랩한 데이터 중 발행주식수가 있으니 2019년의 발행주식수를 가져옴
    stock_num = testdf_total['발행주식수'].copy()
    stock_num = int(stock_num.values)
    # 나만의 목표가 계산식
    testdf_stock_row['적정가격'] = round((testdf_stock_row['영업이익']*per *100000000 / (stock_num * 1000) + (testdf_stock_row['EPS(원)']*per)) /2,-2)
    #testdf_sam[['index', '적정가격']]
    #testdf_sam['index'] = testdf_sam['index'].astype('str')

    # 적정가격을 차트상에 표시하기 위해 일자로 변경
    # 단순작업으로 바꾸는 코드... 이기 때문에 2024, 2025가 되더라도 작동하도록 수정할 것
    testdf_stock_row.loc[testdf_stock_row['index'] == '2020/12(P)','index'] ='2020/12'
    testdf_stock_row.loc[testdf_stock_row['index'] == '2020/12(E)','index'] ='2020/12'
    testdf_stock_row.loc[testdf_stock_row['index'] == '2021/12(E)','index'] ='2021/12'
    testdf_stock_row.loc[testdf_stock_row['index'] == '2022/12(E)','index'] ='2022/12'
    testdf_stock_row.loc[testdf_stock_row['index'] == '2023/12(E)','index'] ='2023/12'

    # datetime을 이용해 년/월 형식으로 수정함 (2020/12 -> 2020-12-01)
    testdf_stock_row['index'] = pd.to_datetime(testdf_stock_row['index'], format='%Y/%m')

    # 2019-12-01의 경우 일요일(주말)이라 차트상에 표시가 안되는 현상을 방지하고자, 일자를 바꿈
    testdf_stock_row['index'] = testdf_stock_row['index'] + Week(weekday=4)
    #testdf_sam[['index', '적정가격']]
    #testdf_sam



    # 현재주가 추출
    nowprice = df1.loc[0, 'Close']
    # 2021년 목표주가 추출(2022년 7)
    tp21 = testdf_stock_row.iloc[6, 33]
    tp22 = testdf_stock_row.iloc[7, 33]
    # 2021년 영업이익 추출
    op21 = testdf_stock_row.iloc[6, 2]
    op22 = testdf_stock_row.iloc[7, 2]
    # 목표주가 상승여력(퍼센트)
    tpper21 = round(((tp21-nowprice)/nowprice*100),2)
    tpper22 = round(((tp22-nowprice)/nowprice*100),2)

    title = stock_name + ' 목표주가 / PER ' + str(per) +' / '+ str(nowprice) +'원('+ str(tp21) + '원 ' + str(round(tpper21,2)) + '%, '+str(op21)+'억)'

    
    fig = go.Figure(data=[go.Candlestick(x=df1['Date'],
                    open=df1['Open'],
                    high=df1['High'],
                    low=df1['Low'],
                    close=df1['Close'])])
    print(fig)                    
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        title_text=title    
    )

    fig.add_trace(go.Scatter(
        name="목표주가",
        mode="markers+lines", x=testdf_stock_row["index"], y=testdf_stock_row["적정가격"],
        xperiod="M1",
        xperiodalignment="middle",
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
    div = opy.plot(fig, auto_open=False, output_type='div')
    return div


def todayRatio():
    # 오브젝트 가져오기
    g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
    g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
    g_objCpTrade = win32com.client.Dispatch('CpTrade.CpTdUtil')

    objRq = win32com.client.Dispatch("CpSysDib.MarketEye")

    codeList = g_objCodeMgr.GetStockListByMarket(1)  # 거래소
    codeList2 = g_objCodeMgr.GetStockListByMarket(2)  # 코스닥
    allcodelist = codeList + codeList2 #전체 코드리스트

    rqField = [0,20,118,120] #요청 필드 종목코드 , 시가 , 상장주식수, 당일외국인순매수, 당일기관순매수
    rqCodeList = [] #인자로 넣어줄 코드리스트

    sumcnt = 0 #가져온 데이터 개수
    df = pd.DataFrame(columns=('code', '상장주식수','당일외국인순매수','당일기관순매수','외국인순매수비율','기관순매수비율')) 


    codeindex = 0 #코드리스트 200개씩 받아오기위한 인덱스
    allcodeindex = len(allcodelist) #전체 코드개수

    while True:

        rqCodeList = []
        for i in range(200): #일단 200개씩 추가
            if allcodeindex <= codeindex + i: #최대 코드개수를 초과하면 멈춤
                break
            rqCodeList.append(allcodelist[codeindex + i])
        codeindex += len(rqCodeList) #다음200개 준비
        
        
        remainCount = g_objCpStatus.GetLimitRemainCount(1)  # 1 시세 제한
        if remainCount <= 0:
            print('시세 연속 조회 제한 회피를 위해 sleep', g_objCpStatus.LimitRequestRemainTime)
            time.sleep(g_objCpStatus.LimitRequestRemainTime / 1000)
    
        objRq.SetInputValue(0, rqField) # 받아올 데이터 지정
        objRq.SetInputValue(1, rqCodeList) #받아올 종목 지정

        objRq.BlockRequest()

        cnt = objRq.GetHeaderValue(2)
        sumcnt += cnt
        for i in range(cnt):
            item = {}
            item['code'] = objRq.GetDataValue(0, i) #종목코드
            item['상장주식수'] = objRq.GetDataValue(1, i) #상장주식수
            item['당일외국인순매수'] = objRq.GetDataValue(2, i) #당일외국인순매수
            item['당일기관순매수'] = objRq.GetDataValue(3, i) #당일외국인순매수
            item['외국인순매수비율'] = round(item['당일외국인순매수']  / (item['상장주식수'] / 100000) , 6)
            item['기관순매수비율'] = round(item['당일기관순매수'] / (item['상장주식수'] / 100000) , 6)
            
            
            df.loc[len(df)] = item

        if sumcnt >= allcodeindex:
            break
    df.sort_values(by=['외국인순매수비율'], axis=0, ascending=False, inplace=True)
    #df.sort_values(by=['기관순매수비율'], axis=0, ascending=False)
    return df
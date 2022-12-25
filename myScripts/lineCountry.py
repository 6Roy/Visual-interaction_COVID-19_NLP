# -*- coding: utf-8 -*-
# By: Eastmount CSDN xiuzhang
import time, json
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode

country_name = 'China'

# countrydata.csv 收集了从 2020-1-19 到 2020-6-17 的各个国家的数据, 用于画每个国家的折线图和日历图.
# dateId: 日期;
# countryName: 国家名字;
# confiredCount: 确诊人数;
# currentConfirmedCount: 当前确诊人数
# deadCount: 死亡人数;
# curedCount: 治愈人数


def render_lines(country_name):
    #-------------------------------------------------------------------------------------
    # 第一步：读取数据
    #-------------------------------------------------------------------------------------
    n = "dataSets/countrydata.csv"
    data = pd.read_csv(n)
    data = data[data['Country'] == country_name]
    date_list = list(data['dateId'])
    date_list = list(map(lambda x:str(x),date_list))
    confirm_list = list(data['confirmedCount'])
    dead_list = list(data['deadCount'])
    # heal_list = list(data['curedCount'])
    print(len(date_list))    
    #print(date_list)                        # 日期
    #print(confirm_list)                     # 确诊数据
    #print(current_list)                     # 疑似数据
    #print(dead_list)                        # 死亡数据
    #print(heal_list)                        # 治愈数据


    #-------------------------------------------------------------------------------------
    # 第二步：绘制折线面积图
    #-------------------------------------------------------------------------------------
    line = (
            Line()
        .add_xaxis(date_list)
        # 平均线 最大值 最小值
        # 下面的 `opts.MarkPointItem` 大概是图中的那个泡泡
        .add_yaxis('确诊数据', confirm_list, is_smooth=True,
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                        opts.MarkPointItem(type_="min")]))
        .add_yaxis('死亡数据', dead_list, is_smooth=True,
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                        opts.MarkPointItem(type_="min")]))
        # .add_yaxis('治愈数据', heal_list, is_smooth=True,
        #         markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
        #                                                 opts.MarkPointItem(type_="min")]))
        # 隐藏数字 设置面积
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5), # 不透明度
            label_opts=opts.LabelOpts(is_show=False))
        # 设置x轴标签旋转角度
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)), 
                        yaxis_opts=opts.AxisOpts(name='人数', min_=3), 
                        title_opts=opts.TitleOpts(title='2019-nCoV'+country_name+'疫情数据曲线图'))          
        )


    return line

import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar

# 日历图
def calendar_base() -> Calendar:
    begin = datetime.date(2022, 9, 1) #设置起始日期
    end = datetime.date(2022, 12, 20) #设置终止日期
    n = "dataSets\\countrydata.csv"
    data = pd.read_csv(n)
    data = data[data['Country'] == country_name]
    date_list = list(data['dateId'])
    date_list = list(map(lambda x:str(x),date_list))
    confirm_list = list(data['confirmedIncr'])
    data =[
    [str(begin + datetime.timedelta(days=i)), confirm_list[i]] #设置日期间隔，步数范围
    for i in range((end - begin).days - 3)
     ]
    print(len(data))

    c = (
    Calendar()
    .add('', data, calendar_opts=opts.CalendarOpts(range_=['2022-9','2022-12'])) #添加到日历图，指定显示2019年数据
    .set_global_opts(          #设置底部显示条，解释数据
        title_opts=opts.TitleOpts(title='全国疫情每日新增确诊病例日历图',subtitle='From Weix'),
        visualmap_opts=opts.VisualMapOpts(
            pieces=[
                                                {'min': 13000, 'color': '#7f1818'},  #不指定 max
                                                {'min': 1000, 'max': 10000},
                                                {'min': 500, 'max': 999},
                                                {'min': 100, 'max': 499},
                                                {'min': 10, 'max': 99},
                                                {'min': 0, 'max': 9} ],   
            orient='vertical',  #设置垂直显示
            pos_top='230px',    
            pos_left='100px',
            is_piecewise=True    #是否连续
         )
     )
    )
    return  c

if __name__ == "__main__":
    calendar_base().render('全国疫情每日新增确诊病例日历图.html')
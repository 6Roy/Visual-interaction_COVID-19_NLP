<script src="https://cdn.bootcss.com/jquery/3.0.0/jquery.min.js"></script>

<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>

<script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/world.js"></script>

<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts-wordcloud.min.js"></script>

<script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/china.js"></script>

<div id="links" style="line-height: 36px; background-color:black;">
    <a href="/" style="display: inline-block; text-align: center;text-decoration: none;color: azure;" >数据分析与可视化</a>
    <a href="/document" style="display: inline-block; text-align: center;text-decoration: none;color: azure;" >技术文档</a>
</div>

# 疫情空间数据与舆情数据分析可视化

新型冠状病毒肺炎（COVID-19，简称“新冠肺炎”）疫情肆虐全球多个国家，2020年3月11日，世界卫生组织 (WHO) 正式宣布将新冠肺炎列为全球性大流行病。在全球抗击新型冠状病毒疫情的过程中，产生了前所未有的大规模疫情数据，本项目希望能利用交互式空间数据分析技术，感知和预测疫情发展趋势与关键节点、分析社交媒体话题与情感的动态演变、对社会舆情进行态势感知。

## 所使用的数据集：

- 疫情统计时空数据，分为国内各省市疫情统计数据及世界各国疫情统计数据，包括从1.19至5.19四个月时间的确诊人数、现存确诊人数、治愈人数、死亡人数等
- 使用爬虫获取的人民网疫情快讯新闻100篇，包含时间、标题、正文内容、作者等
- 依据与“新冠肺炎”相关的230个主题关键词进行数据采集的2020年1月1日—2020年2月20日期间共计100万条微博数据

部分数据经爬虫采集，部分数据采用公开数据集


## 可视化部分采用pyecharts+flask实现动态交互

## part 1：疫情空间数据数据可视化态势感知、趋势分析：

### 疫情数据动态交互可视化地图

共有三种地图类型：现存确诊率地图、累计死亡人数地图、死亡率（累计死亡人数/累计确诊人数）地图，可以通过下拉框进行选择；

可以拖动时间轴上的滑块改变地图显示日期，范围为 1.19-5.19；

<div id="current-maps" >
    <div>
        <label>请选择地图类型:     </label>
        <select name="select-map" id="mapselecter">
            <option value="0" >现存确诊人数</option>
            <option value="1" >累计死亡人数</option>
            <option value="2" >死亡率（死亡/确诊）</option>
        </select>
    </div>
    <div>
        <label>拖动滑块即可切换日期:</label>
        <input id='slider' style="width: 400px;vertical-align: middle;" type='range' min='0' max='121' step='1'/>
    </div>
    <div id="worldMap" class="maps" style="width:800px; height:600px;display: inline-block;"></div>
    <div id="chinaMap" class="maps" style="width:800px; height:600px;display: inline-block;"></div>
</div>

### 世界疫情数据曲线图

通过曲线图可直观地表现出确诊数据、死亡数据、治愈数据等的变化趋势，可以通过下拉框进行选择所显示的国家：

<div>
    <label>请选择国家：    </label>
    <select id="selectCountrys">
    {% for cate in cates %}
        <option value="{{cate}}" >{{cate}}</option>
    {% endfor %}
    </select>
    <div id="lines" style="width:1000px; height:600px;"></div>
</div>

### 全国疫情新增确诊人数日历图

日历图也可以直观的反映出当日疫情新增人数的多少；

<div id="04cd225d9bb642288bef9788ed998f30" class="chart-container" style="width:500px; height:300px;display: inline-block;"></div>
<script type="text/javascript" src="{{ url_for('static',filename='calendar.js') }}"></script>

可以看到，确诊人数的增多从一月底开始，在二月中旬达到高峰后逐步回落；而三月下旬增加人数又有一次较小的上升。

### 疫情趋势预测分析

#### logistic回归算法

（1）模型描述：当一个物种迁入到一个新生态系统中后，其数量会发生变化。假设该物种的起始数量小于环境的最大容纳量，则数量会增长。该物种在此生态系统中有天敌、食物、空间等资源也不足（非理想环境），则增长函数满足逻辑斯谛方程，图像呈S形，此方程是描述在资源有限的条件下种群增长规律的一个最佳数学模型。

（2）一般疾病的传播是S型增长的过程，因为疾病传播的过程中会受到一定的阻力（医治、切断传播途径等措施）。

此处采用最小二乘法，对logistic增长函数进行拟合。以下将检验最小二乘法拟合的逻辑斯蒂模型是否能贴合实际。

`<img src="{{ url_for('static',filename='results/logistic_china.png') }}" style="width:600px; height:500px;">`

本次拟合采用了1月11日到1月27日的累计确诊病例数据作为原始数据，采用最小二乘法拟合逻辑斯蒂曲线，最后经过对逻辑斯蒂模型中R值（增长速率，到达K值的速度）的拟合调整，发现在0.45附近得到的曲线比较贴合我国1月至2月疫情实际情况。从短期来看，2月9日的预测值在4万左右，与实际情况十分贴近，也证明了模型的一定可靠性；但从长期来看，最终值还是相对偏低。

可以将本模型推广，进行全球范围内典型新冠肺炎爆发国家的疫情拟合与未来疫情预测，同时将通过R值的大小反应出该国疫情应对的有效程度：

以下分别是对日本、美国、中国、德国从1.19至5.19的疫情数据进行的拟合和预测：

<div>
<img src="{{ url_for('static',filename='results/logistic_world.png') }}" style="width:400px; height:300px;display: inline-block;">
<img src="{{ url_for('static',filename='results/logistic_american.png') }}" style="width:400px; height:300px;display: inline-block;">
<img src="{{ url_for('static',filename='results/logistic_china1.png') }}" style="width:400px; height:300px;display: inline-block;">
<img src="{{ url_for('static',filename='results/logistic_german.png') }}" style="width:400px; height:300px;display: inline-block;">
</div>

R值：

国家 | 中国 |美国 |英国 |德国 |意大利 |韩国| 日本

- | :-: | :-: | :-: | :-: | :-: | :-: | -:
  R |0.25 | 0.05 |0.08 |0.09 |0.08 |0.11 |0.08

关于R值的补充说明：逻辑斯蒂模型中R值代表的增长速率不是传统意义上理解的种群增长速度，而是接近种群数量达到环境承载力K值的速度。强烈的人为干预可以**大幅度降低K值**，使得种群数量快速达到最大值附近，疫情扩散得以控制。所以本模型在预测各国最终累计感染人数的功能之外，拟合过程中R值的大小可以反映某个国家面对新冠肺炎采取措施的**有效性和效率**。一般来说，R值越大，该国防疫措施越有效。

#### SEITR模型：

（1）模型简介：SEITR模型是基于动力学SEIR模型不断调试模拟的结果，能够比较合理贴合传染病传播的一般规律。

我们先来看看SEIR模型：

1）模型中的4类人群：N为总人数
SUSCEPTIBLES: 用S表示，为易感者, 潜在的可感染人群
EXPOSED：用E表示，为潜伏者, 已经被感染但是没有表现出来的人群
INFECTIVES: 用I表示，为感染者, 表现出感染症状的人
RESISTANCES: 用R表示，为抵抗者, 感染者痊愈后获得抗性的人

2）模型中的3种参数：
αß：易感人群（S) 被感染人员（I) 传染的传染率，相当于单人次易感者接触感染者而被感染的几率（ß）与易感者单位时间内接触的感染者人数（α）的乘积
γ：感染人群（I) 以固定平均速率恢复（R) 或死亡的恢复率
Ω：潜伏人群（E) 变为感染者的平均速率，通常数值取潜伏期的倒数

3）增加修正的参数：
“T”：已被感染且正处于接受治疗时期的人群，主要特征表现为已被感染，已过潜伏期，但不会进行传染，且正在被治疗。
同时也将I人群严格定义为被感染，已过潜伏期但未被医院收治无法接受治疗的人群。
δ，表示I变为T的速率，主要受医院接诊速率及收治能力影响，也受发病后及时就医的时间影响。

以下使用SEITR模型对美国疫情基本得到控制的时间进行预测。

`<img src="{{ url_for('static',filename='results/seir.png') }}" style="width:600px; height:500px;">`

模型拟合评价：

（1）参数的设置：

1）传染率系数与人与人之间的社交距离和社交频率息息相关，美国在疫情早期未及时向民众宣传保持社交距离和戴口罩、减少出行的建议，导致传染率系数会比参数设置的更高；

2）治疗系数与当地医疗水平、卫生设施数量、医疗物资等息息相关，疫情中期各州的医疗设备全面告急，医护人员感染率上升，同时中产阶级及以下家庭因为无法支付高昂医疗费选择在家隔离，错过最佳治疗期，使得治疗系数要低于已经有雷神山火神山的武汉对应时期的治疗系数；

（2）结果分析：
主要的预测在于感染人数逐渐趋于0的时间节点，本次预测得到的结果是今年秋季美国的疫情能够基本得到控制。

（3）拟合分析；
本模型在尝试同时拟合现有病例（正在接受治疗人群）和治愈人数曲线时，发现无法做到相对同时拟合的比较贴合实际的结果。分析可知，（1）中的参数对拟合结果的影响非常大，而模型参数的选择需要结合美国实际疫情情况才能推算，目前使用的计算手段过于粗糙；同时该模型的假设条件是，美国的0号病人出现在今年1月11日，但是目前的报告陆续显示早在2019年美国就有社区性传播，因此本模型的可靠性大大下降。由于具体的时间目前国际上无法追溯，所以进一步的研究很难继续进行。

## part 2: 疫情舆情数据分析与可视化

### 新闻数据分析与可视化

#### 人民网疫情快讯新闻词云可视化：

词云图，也叫文字云，是对文本中出现频率较高的“关键词”予以视觉化的展现，词云图过滤掉大量的低频低质的文本信息，使得浏览者只要一眼扫过文本就可领略文本的主旨。对人民网疫情快讯的100篇新闻使用jieba进行分词、获取主题词（取排名前100位），并渲染词云图：

<div>
    <div id="c61d88ede2df46799724e4ef261fa76f" class="chart-container" style="width:900px; height:500px;"></div>
    <script type="text/javascript" src="{{ url_for('static',filename='wordcloud.js') }}"></script>
</div>

<div>
    <div>
        <label>拖动滑块即可切换日期:</label>
        <input id='sliderWord' style="width: 400px;vertical-align: middle;" type='range' min='0' max='90' step='1'/>
    </div>
    <div id="wordcloud" style="width:1000px; height:600px;"></div>
</div>

### TF-IDF值

TF-IDF（Term Frequency-InversDocument Frequency）是一种常用于信息处理和数据挖掘的加权技术。该技术采用一种统计方法，根据字词的在文本中出现的次数和在整个语料中出现的文档频率来计算一个字词在整个语料中的重要程度。它的优点是能过滤掉一些常见的却无关紧要本的词语，同时保留影响整个文本的重要字词。

`<img src="{{ url_for('static',filename='results/tfidf.png') }}" style="width:600px; height:500px;">`

### 层次聚类分析

对主题词进行层次聚类分析，层次聚类法的基本过程如下：

- 每一个样本点视为一个簇；
- 计算各个簇之间的距离，最近的两个簇聚合成一个新簇；
- 重复以上过程直至最后只有一簇。

层次聚类不指定具体的簇数，而只关注簇之间的远近，最终会形成一个树形图，可以表明相应关键词间的联系：

`<img src="{{ url_for('static',filename='results/tree_word_50.png') }}" style="width:1000px;">`


## part 3:微博舆情分析与数据可视化

#### 微博主题词词云图：

依据与“新冠肺炎”相关的230个主题关键词进行随机数据采集的2020年1月1日—2020年2月20日期间共计100万条微博数据进行主题词计算，可绘制微博主题词词云图：

<script type="text/javascript" src="{{ url_for('static',filename='render.js') }}"></script>

分别对于每日的微博主题词进行分析，可绘制微博每日主题词词云图：

<div>
    <div>
        <label>拖动滑块即可切换日期:</label>
        <input id='sliderWeibo' style="width: 400px;vertical-align: middle;" type='range' min='0' max='49' step='1'/>
    </div>
    <div id="weibocloud" style="width:1000px; height:600px;"></div>
</div>

#### 微博情感分析

对微博数据采用snowNLP进行情感分析得出的情感数值，范围为-0.5 ~ 0.5，大于0为正面情感，小于0为负面情感；

绘制每日平均情感数值曲线图：

<div>
    <div id="9d2779b5eb384c2793ed26055a81879d" class="chart-container" style="width:900px; height:500px;"></div>
    <script type="text/javascript" src="{{ url_for('static',filename='weibolines.js') }}"></script>
</div>

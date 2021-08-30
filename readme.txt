**Important！！**

1. 请在登录淘宝（https://www.taobao.com）, 京东（https://www.jd.com）和1688（https://pjjx.1688.com/之后获取到headers和param填入get_data_1688(), get_Data_taobao(), get_data_jd()中的header字典与param (spider.py)

2. 此框架添加了抓取京东评论数据的函数，需要在抓取数据动态页面函数get_jd_comment()的header，param和cookie变量与字典内容

3. 京东评价内容必须在登录之后才能查看，否则此数据正常浏览的情况下不显示在页面。数据储存在页面返回的jQuery文件中

4.本地查看需要设置虚拟环境运行页面
# -*- coding = utf-8 -*-
# @Time : 2021/5/23 9:26 下午
# @File : spider_1688.py
# @Software : products
"""
1. 请在登录淘宝（https://www.taobao.com）, 京东（https://www.jd.com）和1688（https://pjjx.1688.com/）
之后获取到headers和param填入get_data_1688(), get_Data_taobao(), get_data_jd()中的header字典与param
2. 此框架添加了抓取京东评论数据的函数，需要在抓取数据动态页面函数get_jd_comment()的header，param和cookie变量与字典内容
3. 京东评价内容必须在登录之后才能查看，否则此数据正常浏览的情况下不显示在页面。数据储存在页面返回的jQuery文件中
"""

import time
import requests
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error, urllib.parse  # 定制URL，获取网页数据
import ssl
import urllib
from lxml import etree
from .models import essencial_field
import demjson

ssl._create_default_https_context = ssl._create_unverified_context

items = essencial_field.objects.get(id=1)
jd_header = items.jd_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
jd_comment_cookie = items.jd_comment_cookie.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
jd_comment_header = items.jd_comment_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
pjjx_header = items.pjjx_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
tb_header = items.tb_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')


def get_Data_1688(baseurl, keyword):
    datalist = []
    # print(len(datalist))
    keys = {"keywords": keyword}
    real_key = urllib.parse.urlencode(keys)
    url = baseurl + real_key
    for page in range(10):
        """
        1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
        2. 登陆完账号之后拷贝当前页面的cURL在https://curl.trillworks.com/上转换为headers和param的字典粘贴到下方
        """
        headers = demjson.decode(pjjx_header)
        # headers = {
        #     # headers信息
        #     'authority': 'widget.1688.com',
        #     'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        #     'sec-ch-ua-mobile': '?0',
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        #     'accept': '*/*',
        #     'sec-fetch-site': 'same-site',
        #     'sec-fetch-mode': 'no-cors',
        #     'sec-fetch-dest': 'script',
        #     'referer': 'https://wxb.1688.com/',
        #     'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        #     'cookie': 'SameSite=none; cna=ZYvQGKJpWF4CATzx0Dql5n8G; lid=bennyzhuang00; ali_ab=101.174.144.53.1621415102299.4; UM_distinctid=179ad6f905b2f3-07d9bea215759f-37607201-fa000-179ad6f905c290; taklid=282143df5825440393590fa2e932e9e6; ali_apache_track=c_mid=b2b-282036248|c_lid=bennyzhuang00|c_ms=1; alicnweb=touch_tb_at%3D1622378501187%7Clastlogonid%3Dbennyzhuang00%7Cshow_inter_tips%3Dfalse; hng=CN%7Czh-CN%7CCNY%7C156; xlly_s=1; cookie2=1c40a0e9b15aeabf82c8b597a7f4f84b; t=66ea699be599f5684bbee8dc7e1dbee0; _tb_token_=7788777b08b5e; cookie1=BxeAZlv7ngL%2Bsrsb3TA94oWOY0S5jESMRiiyVxyKkIk%3D; cookie17=UUBaC973gO1j; sg=08a; csg=1411d348; unb=282036248; uc4=nk4=0%40A6yqGglpwGGT7RqCJSkLLAEO0BgaHnxK&id4=0%40U2LIB%2FUuGxYUJHaKSryep3tRklg%3D; __cn_logon__=true; __cn_logon_id__=bennyzhuang00; ali_apache_tracktmp=c_w_signed=Y; _nk_=bennyzhuang00; last_mid=b2b-282036248; _csrf_token=1629602202480; firstRefresh=1629602232257; lastRefresh=1629602232257; _is_show_loginId_change_block_=b2b-282036248_false; _show_force_unbind_div_=b2b-282036248_false; _show_sys_unbind_div_=b2b-282036248_false; _show_user_unbind_div_=b2b-282036248_false; __rn_alert__=false; tfstk=cZEFBgGwt0V1I1n5kDiPAD99OgodwLVuGhk--P3JE9LSevfD4QHgBPDZHjIi-; l=eB_Edcmuj-T9HYcABOfwourza77OSIRAguPzaNbMiOCPO2fp5t0fW6nXDuY9C3MNhsHeR3R4BJt3BeYBcIcidj4KkDh_vkHmn; isg=BJCQTtiaxTKHx5iz7ur8h9eZYdjiWXSjKafya4phXOu-xTBvMmlEM-bznZUlFSx7',
        # }
        params = (
            ('start', str(page * 60)),  #
            ('pageSize', '60'),
            ('keywords', keyword.encode('utf-8')),
            # 保留以上信息添加其他信息
            ('callback', 'jQuery1830530169495744514_1629602281901'),
            ('namespace', 'AllianceSearchOfferFromSw'),
            ('widgetId', 'AllianceSearchOfferFromSw'),
            ('methodName', 'execute'),
            ('_tb_token_', '7788777b08b5e'),
            ('sortType', 'normal'),
            ('descendOrder', 'true'),
            ('_', '1629602282469'),
        )
        html = ''
        try:
            response = requests.get(url, headers=headers, params=params)
            html = response.text  # print(html) # test print
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        for a in range(0, 60):
            data = []
            # match the target by regx
            title = re.findall('"name":"(.*?)"', html)
            if a < len(title):
                if len(title) == 0:
                    data.append('')
                else:
                    data.append(title[a])

                price = re.findall('"price":(.*?),', html)
                if len(price) == 0:
                    data.append('')
                else:
                    data.append(price[a])

                supplier = re.findall('"companyName":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append('')
                else:
                    data.append(supplier[a])

                sales = re.findall('"saleQuantity":(.*?),', html)
                if len(supplier) == 0:
                    data.append('')
                else:
                    data.append(sales[a])

                link = re.findall('"sourceUrl":"(.*?)"', html)
                if len(link) == 0:
                    data.append('')
                else:
                    data.append(link[a])
                datalist.append(data)
            else:
                break
        print('1688_Page %d searching' % (page + 1))
    # print(datalist) # test print
    return datalist


def get_Data_TaoBao(baseurl, keyword):
    datalist = []
    # print(len(datalist))
    keys = {"q": keyword}
    real_key = urllib.parse.urlencode(keys)
    url = baseurl + real_key
    for page in range(10):
        """
        1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
        2. 拷贝cURL在https://curl.trillworks.com/上转换为headers和param的字典粘贴到下方
        3. 淘宝的反爬检测更加敏感，需要频繁更新cookie和header的内容，每页搜索时间间隔2秒
        """
        params = (
            ('q', keyword.encode('utf-8')),
            ('s', str(page * 44)),
            # 此两行保留，添加其他信息
            ('type', 'p'),
            ('tmhkh5', ''),
            ('from', 'sea_1_searchbutton'),
            ('catId', '100'),
            ('spm', 'a2141.241046-cn.searchbar.d_2_searchbox'),
        )
        headers = demjson.decode(tb_header)
        headers = {
            # headers信息
            'authority': 's.taobao.com',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://world.taobao.com/',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
            'cookie': '_fbp=fb.1.1621391722570.1255743606; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; enc=TaYxtUvmziB96HFymV7g7L3vWU6Pe0jOK8NcNQ%2FotfklQ0DtNWszCi9udCaF1sUkdqzX9BaKkdbdHcZ4jFB%2BgQ%3D%3D; _uab_collina=162242619709014642647715; cna=ZYvQGKJpWF4CATzx0Dql5n8G; tracknick=bennyzhuang00; lgc=bennyzhuang00; miid=265413217203878660; mt=ci=-1_0; _samesite_flag_=true; cookie2=1c40a0e9b15aeabf82c8b597a7f4f84b; t=66ea699be599f5684bbee8dc7e1dbee0; _tb_token_=7788777b08b5e; xlly_s=1; sgcookie=E100eDZ4rqWbyiGi1NFjjHxeVOJaLZ4F%2BSvuLa3rQQ2hA0XjZ2fCDS4Vg4ypWOGg4D%2F%2F6B5XwOUSbWV15CL0VlJtvaEU91wlff2NrhNMxYQpCaE%3D; unb=282036248; uc1=cookie21=UtASsssmeJpuuznauA%3D%3D&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=true&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie14=Uoe2xMVETcVyOA%3D%3D&pas=0; uc3=lg2=URm48syIIVrSKA%3D%3D&vt3=F8dCujHtlQmoN%2BCvei8%3D&nk2=AQH9A1xNbcJf%2F600og%3D%3D&id2=UUBaC973gO1j; csg=1411d348; cancelledSubSites=empty; cookie17=UUBaC973gO1j; dnk=bennyzhuang00; skt=335ce88c386bbcbf; existShop=MTYyOTYwMjE5OQ%3D%3D; uc4=nk4=0%40A6yqGglpwGGT7RqCJSkLLAEO0BgaHnxK&id4=0%40U2LIB%2FUuGxYUJHaKSryep3tRklg%3D; publishItemObj=Ng%3D%3D; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=08a; _nk_=bennyzhuang00; cookie1=BxeAZlv7ngL%2Bsrsb3TA94oWOY0S5jESMRiiyVxyKkIk%3D; _ga_YFVFB9JLVB=GS1.1.1629602462.3.0.1629602462.0; _ga=GA1.2.1433280201.1627201365; _gid=GA1.2.1454885366.1629602463; _gat_gtag_UA_202630127_1=1; _m_h5_tk=ba848a9e7b7ab92091e82475f45b21f0_1629612183537; _m_h5_tk_enc=afebd7f2f7beec03320677ebacf30c12; l=eBaAXr_ej-IIxWyDBOfwlurza77ORIRAguPzaNbMiOCPO8165XgOW6nXmDTBCnMNh659R3R4BJt3BeYBcQAonxv9rNWQtWHmn; tfstk=cmNVBuiymfqSrHG1pjGNGj1dihgAZVZgAQutn8H9aUEDk4Hcir-trzeoz2ndZxf..; isg=BL-_RiHy4tffiOdOONt2NZqETpVJpBNGkmIt9lGMem61YN_iWXRglixyoiieOOu-',
        }

        html = ''
        try:
            response = requests.get(url, headers=headers, params=params)
            html = response.text  # print(html) # test print
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        for a in range(0, 44):
            data = []
            # match the target by regx
            title = re.findall('"raw_title":"(.*?)"', html)
            if a < len(title):
                if len(title) == 0:
                    data.append("")
                else:
                    data.append(title[a])

                price = re.findall('"view_price":"(.*?)",', html)
                if len(price) == 0:
                    data.append("")
                else:
                    data.append(price[a])

                supplier = re.findall('"nick":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append("")
                else:
                    data.append(supplier[a])

                location = re.findall('"item_loc":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append("")
                else:
                    data.append(location[a])

                sales = re.findall('"view_sales":"(.*?)人付款"', html)
                sale = str(sales[a])
                if len(sales) == 0:
                    data.append("")
                else:
                    if sale.find('+', 0, len(sale) - 1) and (sale.find('万', 0, len(sale) - 1) == -1):
                        result = sale.strip('+')
                        data.append(int(result))
                    elif sale.find('万+', 0, len(sale) - 1):
                        result = sale.strip('万+')
                        final = int(float(result) * 10000)
                        data.append(int(final))
                    else:
                        data.append(int(result))

                link = re.findall('"comment_url":"(.*?)"', html)
                if len(link) == 0:
                    data.append("")
                else:
                    link = link[a].encode('latin-1').decode('unicode_escape')
                    data.append('https:' + link)

                datalist.append(data)
            else:
                break
        print('TaoBao_Page %d searching' % (page + 1))
        time.sleep(2)
    # print(datalist)  # test print
    return datalist


def get_data_jd(baseurl, keyword):
    datalist = []
    keys = {
        'keyword': keyword,
    }
    real_key = urllib.parse.urlencode(keys)
    # url = baseurl + real_key
    """
    1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
    2. 登陆完账号之后拷贝当前页面的cURL在https: // curl.trillworks.com / 上转换为headers和param的字典粘贴到下方
    """
    headers = demjson.decode(jd_header)
    # headers = {
    #     # headers信息
    #     'authority': 'search.jd.com',
    #     'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    #     'sec-ch-ua-mobile': '?0',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'same-site',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-user': '?1',
    #     'sec-fetch-dest': 'document',
    #     'referer': 'https://www.jd.com/',
    #     'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    #     'cookie': 'shshshfpa=8145111e-7e4a-44e1-b049-3d1dfce63ba8-1621388641; __jdu=16213886404871498490338; shshshfpb=oXH046poVcixILfV8MOr0NQ%3D%3D; qrsc=3; __jdv=76161171|www.google.com|-|referral|-|1628945256926; TrackID=1njGXn3-uN285AEl6KxIOo3CGlnH1lc25DY5zpa5hgXvvHb1TY4hngkqb_dexgziPD_2Ehv-R4UQPQRdSIMmW0kch-oSp3L4a1CB6K8HetFNXZeFESYBaiLelly9EBWkh; pin=bennyzhu00; unick=bennyzhu00; _tp=RBd2AnyI%2FD3rqSJd%2BRPqtA%3D%3D; _pst=bennyzhu00; areaId=1; ipLoc-djd=1-72-2799-0; thor=F20FE97791E6845A729114AAB469C827CB79402490C333E84D043676A4740D6D3AA7CFE851BA467A309FCF321F2FC1D71045DDBCC277EDF7593D3DF0656FB34981F0A070F26CB7EEA452C6833AC3359ED59E882135714C8B3D05D23D5B089444D85D58AD3BC3843AD2B9F5EEF1A609C502F9EF1B99CE3F4F2EE6E281347CD3D068DA44E01E86BAAC781CA4831D4D3AF6; pinId=obkAO9L4QVZ1UBI1KxU0IQ; __jda=76161171.16213886404871498490338.1621388640.1629375706.1629602597.14; __jdb=76161171.4.16213886404871498490338|14.1629602597; __jdc=76161171; PCSYCityID=AU_0_0_0; shshshfp=6a52c9e3e4ef30e835b32bfda3fe9d24; shshshsID=88df3b228ef297e5654dde8686e3877c_1_1629602623702',
    # }
    for i in range(10):
        url = baseurl + str(i) + '&' + real_key
        try:
            # response = urllib.request.urlopen(request)
            # html = response.read()
            # content = etree.HTML(html)
            # print(content)
            request = requests.get(url, headers=headers)
            text = request.text
            selector = etree.HTML(text)
            lis = selector.xpath('//*[@id="J_goodsList"]/ul/li')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

        for li in lis:
            data = []
            title = li.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')
            new_title = ''
            if len(title) == 0:
                data.append("")
            else:
                if title != 0:
                    new_title = keyword.join(title)
                    new_title = new_title.replace("\n", "")
                    new_title = new_title.replace("\t", "")
                data.append(new_title)

            price = li.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
            if len(price) == 0:
                data.append("")
            else:
                data.append(price)

            supplier = li.xpath('.//div[@class="p-shop"]/span/a/text()')
            if len(supplier) == 0:
                data.append("")
            else:
                data.append(supplier[0])

            link = li.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0]
            link = "https:" + str(link)
            if len(link) == 0:
                data.append("")
            else:
                data.append(link)
            # print(data)

            comment_id = li.xpath('.//@data-sku')
            if len(comment_id) == 0:
                data.append('')
            else:
                # comment_id = get_jd_comment(comment_id[0])
                data.append(comment_id[0])

            datalist.append(data)
            # print(len(datalist))

        count = i * 30
        fix_datalist_comment(datalist, count)
        print('JD_Page %d searching' % (i + 1))
    return datalist


def get_jd_comment(comment_id):
    rate_list = []
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='
    base_url = comment_url + comment_id
    cookies = demjson.decode(jd_comment_cookie)
    # cookies = {
    #     'shshshfpa': '8145111e-7e4a-44e1-b049-3d1dfce63ba8-1621388641',
    #     '__jdu': '16213886404871498490338',
    #     'shshshfpb': 'oXH046poVcixILfV8MOr0NQ%3D%3D',
    #     '__jdv': '76161171|www.google.com|-|referral|-|1628945256926',
    #     'TrackID': '1njGXn3-uN285AEl6KxIOo3CGlnH1lc25DY5zpa5hgXvvHb1TY4hngkqb_dexgziPD_2Ehv-R4UQPQRdSIMmW0kch-oSp3L4a1CB6K8HetFNXZeFESYBaiLelly9EBWkh',
    #     'pin': 'bennyzhu00',
    #     'unick': 'bennyzhu00',
    #     '_tp': 'RBd2AnyI%2FD3rqSJd%2BRPqtA%3D%3D',
    #     '_pst': 'bennyzhu00',
    #     'jwotest_product': '99',
    #     'areaId': '1',
    #     'ipLoc-djd': '1-72-2799-0',
    #     'pinId': 'obkAO9L4QVZ1UBI1KxU0IQ',
    #     'PCSYCityID': 'AU_0_0_0',
    #     '__jda': '122270672.16213886404871498490338.1621388640.1629375706.1629602597.14',
    #     '__jdc': '122270672',
    #     'shshshfp': '74fec342a91ab44c5f3dfb173dbc78ab',
    #     'token': 'ff8099bdcbe56e111100abdc2798d9d4,2,905334',
    #     '__tk': 'e370ce87d5d2dc5a7c5ab9b79390d8ca,2,905334',
    #     'thor': 'F20FE97791E6845A729114AAB469C827CB79402490C333E84D043676A4740D6DD08284749117AC6A892F0951389B249416C0AD2C089E30F7C83B43ED73722C40C74F2459E612B8153E27C6062C99580BF7072DC09DBB6E0C968906A6812045C7BF04F08F4F437352A87E1EE9804FDCC34527DDC8BA56FFB56F2D67D8D2197A51652D01EE80EED0C961F41B79B72912FC',
    #     '3AB9D23F7A4B3C9B': '6KITC6GB63LXKLIVQRIQAHWK47OAWR3NWWD3KOLFRBL33N65QET7O4FBZU33M4A76DJDUJ7DCXOSEGN6WMH5LHDN6U',
    #     'RT': 'z=1&dm=jd.com&si=m6ch7sn725&ss=ksmne3gy&sl=1&tt=fqt',
    #     'shshshsID': '88df3b228ef297e5654dde8686e3877c_4_1629602886715',
    #     '__jdb': '122270672.7.16213886404871498490338|14.1629602597',
    # }
    headers = demjson.decode(jd_comment_header)
    # headers = {
    #     'Connection': 'keep-alive',
    #     'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    #     'sec-ch-ua-mobile': '?0',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    #     'Accept': '*/*',
    #     'Sec-Fetch-Site': 'same-site',
    #     'Sec-Fetch-Mode': 'no-cors',
    #     'Sec-Fetch-Dest': 'script',
    #     'Referer': 'https://item.jd.com/',
    #     'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    # }

    params = (
        ('referenceIds', comment_id),
    )
    response = requests.get(base_url, headers=headers, params=params, cookies=cookies)
    html = response.text

    good_rate = re.findall('"GoodRate":(.*?),', html)
    # print(good_rate)
    # rate_list.append()
    return good_rate


def fix_datalist_comment(datalist, count):
    string = []
    string.clear()
    for a in range(0, 30):
        if (a + count) < len(datalist):
            string.append(datalist[a + count][4])
        else:
            break

    new_string = ''
    # print(string)
    # print(len(string))
    for s in range(len(string)):
        new_string += (string[s] + ',')
    new_string = new_string.strip(',')
    # print(new_string)

    comment_list = []
    # print(get_jd_comment(new_string))
    for c in get_jd_comment(new_string):
        c = float(c) * 100
        comment_list.append(c)

    # print(comment_list)
    for b in range(0, len(comment_list)):
        datalist[b + count][4] = comment_list[b]

    return datalist

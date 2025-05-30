###########         AliExpress

import csv
import re
import time
import json
import scrapy
from lxml import etree
from scrapy import Selector


class AliExpress(scrapy.Spider):
    name = 'AliExpress'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'aeu_cid=ebb52f3cc5e04d06a054a32dc0c5575d-1709325012630-09485-_DkLOoVJ; af_ss_a=1; af_ss_b=1; e_id=pt70; cna=2ShpHr7x9EgCAba6XxwPYfAF; ali_apache_id=33.3.132.219.1709325021413.123500.2; _bl_uid=LalLquaj0Cte6ytUnphdon3j015v; xlly_s=1; _ga_save=yes; acs_usuc_t=x_csrf=xh2_nbocxc_y&acs_rt=43fc8152272d41628b310dbade734696; intl_locale=en_US; _mle_tmp_enc0=Ey%2Fp8LswzxA3J47VsqxI%2Bxira8P%2F%2F5eV1bpiuFB%2Fu8RqcZK7O2z0XUtAwV03w%2FaNr1YM79yYF1a0AFN4I3PBQs9wYkK2fPBvLn38vUPIn7xaTmXZbhWAm%2F8GWLtBGGWaOr81M1eIWodWQ58jKN2l7A%3D%3D; XSRF-TOKEN=ae52ad1f-1096-416a-82b6-e6ce721687e2; AB_DATA_TRACK=472051_617390; AB_ALG=; AB_STG=st_StrategyExp_1694492533501%23stg_687; _gid=GA1.2.1115201088.1711204197; _gcl_au=1.1.1877518665.1711204198; AKA_A2=A; x_router_us_f=x_alimid=2677341414; xman_us_t=x_lid=pk1078775417rcdae&sign=y&rmb_pp=syedhassanmujtabasherazi@gmail.com&x_user=eEi2qkBpRMGm2T7JALSML9PzlrMjl2pgiwjai8CJiFk=&ctoken=165kxjqip177z&l_source=aliexpress; sgcookie=E100VnDys6RxTL5rKYKNQU5tXonY+tMPDgUAR/0GSVLQpnoBa1HpQuo0UvvhAEmzoB9YjROuWaNRtDyQ5bryut6y25AfL2ldGomcoONbX5Zv67Y=; aep_common_f=0hps40OSNWpnBMImrJnraL08ZX5hdNROzN5lbLNE1upLSMU3tgSElw==; xman_f=K0tzKkS39w+XdDQbvkDt5AjAD9rGxwQiRBU4w9alW/3Ii+QqWYIvUcGtm1evjX2Zkmf3C5gs0RdDIR6CoW6nHppOAhwBToRSpzp9vPGBXpRBd7WaFtQRJzJ2mZQlx2oIF25tXl7CY1ivV8OUzZP07kd8PuAc6f0dxW4sioK1IIaIiAdl2OPHqKEZ+rD2PSMOQPImNc6AAJT7R+Oaq3i+nbvGQ7lHjDy89SIx+nfK/SeyJFh5x3IHlrDB1xEyQr2VVYrQGJCWGPkRTI5qIUOIAeNWhTw0jiTJMgORctYXFqSvJZcMIj/ypaZwN3z9Fzv9McDBLps/RKoFmSexsphIge/0+cVszNHy5GWTQFgMlPX1YKv86H4FcHCQ+L8LIk4vnElRsYSwhogofCMPHFu4q0t35NQsVKE8YnsZ2hxjxpOLsbnBkFJZz6A9HVR4Eop9MLiabtmaOLbglwrQYB7izM2bvhfAJCthHfcszy/OnqYRR8ghyM513Ht4cUNFS/I3lKfhAw5MT8a2rrpA14DTb3OIBlAI6yYU; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005003999468972%091005002570478408%091005003086323272; _m_h5_tk=71bb88dd695fe95acd4a445fde214d91_1711217603875; _m_h5_tk_enc=0f4e325e1cf92f72bbdb3b14939d86c7; aep_usuc_f=site=glo&c_tp=USD&x_alimid=2677341414&re_sns=google&isb=y&region=PK&b_locale=en_US&ae_u_p_s=2; ali_apache_track=mt=1|ms=|mid=pk1078775417rcdae; ali_apache_tracktmp=W_signed=Y; xman_us_f=x_locale=en_US&x_l=0&x_user=PK|Syed%20Hassan|Mujtaba%20Sherazi|ifm|2677341414&x_lid=pk1078775417rcdae&x_c_chg=1&x_as_i=%7B%22aeuCID%22%3A%22ebb52f3cc5e04d06a054a32dc0c5575d-1709325012630-09485-_DkLOoVJ%22%2C%22af%22%3A%223vEjIgH6VJjR%22%2C%22affiliateKey%22%3A%22_DkLOoVJ%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%221%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%220%22%2C%22pid%22%3A%224534051009%22%2C%22tagtime%22%3A1709325012630%7D&acs_rt=9190df693d0f4c0291be243c85f6145e; _ga_VED1YSGNC7=GS1.1.1711212726.4.1.1711215372.58.0.0; _ga=GA1.1.1760378831091101.1711038054064; tfstk=fY_xZ56xv82mi0UxYGZlb5BOnIPuEZCqPt5ISdvmfTBRO6kDfoWgWVCV1CjDnKjJBT6JhsvggNBJsC9scFT6F_O2tqO6hhMWVLBjSnXGWguOT170gFV2us8w5J23-JfVgF-fjdHLE_N6_qqqsVzhgsl7AfqQhy0OGhTrXd66c3iWOLgjCd66PLOBFqOslC97wC8qK5r8eRgwvwRbYZtc8lBhVIKvpmv-WVFMMnpCGLeQdaU9Dp1XeVwLtGjwBL7QEuCP_i6DaOULeesFeNKBWrHeMg1pPKYQl4TcussBfwwZfs8XFU_fvfg1wEpW2ZBjH8pCu__eP34Q9__Pns7Rsfa6Z9v5gZTTRW8vlKTR4r7hJoJSKpdic7F-bc-Xa2HlvlczyAOJwpVuZcow2tdJK7F-bc-XaQp3a9oZb3BA.; isg=BFBQBjKrASwV4t01wM-6nzj_IZ6iGTRjrjVgoEohHat-hfAv8ivD8VO9WVVlVew7; arp_scroll_position=125; JSESSIONID=D6D659D75B5353A4AD2E315424E8C7A7; intl_common_forever=uF6svlawDGHkKYS18pCEMFAJMcRxJx7i4s9mamGCwmlu0yCpQ/2QUA==; xman_t=CCjLHYgXR25/7fZhA5Br+W4mR7qL/s7WZw9fc85AHXF24C3u6J7C454KfvKDdMZiKe+qS9RpzZy7hAJm2UPX+kN3iBH6dHhG7TZUtPrlkwUmF4GszJ0cc7+lpRzidaq/QRA2scelIeV9ZzgoWyylUyDB9g8ZOAIDg844buyBaNEKWMs816SXujxgQsIC1q+pHWuYhDMJH9R7PvJ+MJUQweds8mnAQeULN0lvFGQ4lFveVHS4rvk0xsaaskkdUMrJ0Pmt/czfTijOlxsyhPkZpk9FJl6kR6U1EZWzHEWRRvmgmqepMBaGIdv91MiLWnfy6FysjiwWhc+yDAeiPiuHtUioAMMKx7hid2hs0uQ/LVpcaumyvwivkZGGXSOLDsxqB48c6OWPmPR81J6sAeIK3+5YNhHEJGQMey39LKfH4vYdgrvPkXZm99kfoiCNI9ihO63n9iDpzFJ70sq4J72Axx9vzKr9E3GuYPojO7vwiWBnOl656VuDNoqIfOPUFcmWf9uF1KVFYxjvTNu2HPiwOzNvIdmFA32Rap/TDuMq2dRhpWGUWIAS+5spzedXWQAzI8LnKrJIHXGAcTIGXuA1O/CiOXoMJcQ969X4U7cbMODyicWuoIiCZ2Ynpso0cwjK9Nz8tvnSdoqzJwcE0ytbv755B7LvtFU6Sa7Xs2px+BPFZZtB/Da1rYGJst9GREv1uVtjslnP4NMoAvlZD8F68q/yOfnWcqHGfmjJ+4mqVfbMYbkvZO5LS8w3vdQ+BwiPE8cuqoxx4LABh2IFH/3krtUQ5eCWfK/JbfCXv6YtVE744t2L2J8b1A==; RT="z=1&dm=aliexpress.com&si=65c32ea9-954d-4720-ab85-55e258f76489&ss=lu4dg4s9&sl=1&tt=7qj&rl=1&ld=7ql&ul=2zam"; AB_ALG=; AB_DATA_TRACK=472051_617390; AB_STG=st_StrategyExp_1694492533501%23stg_687; _m_h5_tk=e3e02cb7d68e5641e92a50701dbba704_1711054235953; _m_h5_tk_enc=36e2d3022d42dbb7b21b5dfeae479976; aep_usuc_f=site=glo&c_tp=USD&x_alimid=2677341414&re_sns=google&isb=y&region=PK&b_locale=en_US&ae_u_p_s=2; ali_apache_id=33.27.96.9.171104962843.534166.2; intl_common_forever=xLnDM4WpJweXgQezUilVTT1M9aaaXljKhpkZS7JqG30l75eYiO0Vuw==; intl_locale=en_US; xman_f=RJqu04DhFJGZ+rFzLVEqcQ9EPzevH60+KcblB0v9Iv44CL8tYeQZ7UzVXjr3ZsByhy7cMWPFjWh6e7SUiPRvVJJqYSrz40WVp+tx0tzYTcKv1QX4OkDbVA==; xman_t=5GeqOpnL5+9yBTTV7c17Yy75ogXeuUwrMZ20kaaAZHlY/WlEQiukf1dBjzoxvVhTiwaokCuiSAY6BvaD5M0tkcW8Ja+PzkbZ98Uk7xXercGPRyssjD4qzVSWK3tzRoSR8bGkrBi5fi8qOxOCY3DHJneP6OUSe6JhVWGXZMqVUZf5/T8VJ1d2NCfk4V7TGedTyKqYk1OKXyabL2afcXtoZGSDLI9cRNS2Ue4cG0asBGmrfTPG8PImbLUznz2uix+XJushQobQtg2bF4D/sYo4FHnDT7bT1JF8oRbSeC+1424RQ9b/clSIlBYEdbaYXBDWmtoFbiHnPRh9yC0Zf61mKe/492IPLQ2G+/ghGx5yFxHAjBftVRA4BBPS/wS6ppCMUatay4JPPTdvVjQtTx40JAwO2uQIAzlwy/AxRY8w8mtaETWLDdKa+4edJgDlCqcky+1zE4jJpJaxiJB6cMY3sQTe2VeCMWmymp/6UhMKePqZR7f+vVV/57pzAr0K39BBMsaBjhO4YSOcx3Z/T/6DYFKOALWv/jRm9bM+vT3OqkY3ho60Zababuhof2KMqWMTOMMLbEhr49DKSVy36blDis3Ad+P/+sf1I37LpLW6sG6HwPKVHSmLqmn4Y3m9hBJyj0mkdZm4m1vI2kGIu0Q79ffVdjTDYkNiLXTVb+1MNcs8jdQ+q9uAEzKKoTS05is+S28Y7dOvxFi9BTLhx5JcyeyqQb1Q/92+SOi8uHPwU1IjM3r3twDnFWVmaAhqcGHjKSnij1TAfmDOL7xWNkP9Rf9JqjtpM/H4dVdNct2l/fGmUIgiFMY37Q==; xman_us_f=x_locale=en_US&x_l=0&x_user=PK|Syed%20Hassan|Mujtaba%20Sherazi|ifm|2677341414&x_lid=pk1078775417rcdae&x_c_chg=1&x_as_i=%7B%22aeuCID%22%3A%22ebb52f3cc5e04d06a054a32dc0c5575d-1709325012630-09485-_DkLOoVJ%22%2C%22af%22%3A%223vEjIgH6VJjR%22%2C%22affiliateKey%22%3A%22_DkLOoVJ%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%221%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%220%22%2C%22pid%22%3A%224534051009%22%2C%22tagtime%22%3A1709325012630%7D&acs_rt=9190df693d0f4c0291be243c85f6145e; JSESSIONID=1599CF9A0950E485D033E58CD65F1F3E',
        'referer': 'https://www.aliexpress.com/item/1005003086323272.html?pdp_npi=4%40dis%21USD%21US%20%2469.00%21US%20%2465.55%21%21%2169.00%2165.55%21%402102f67717111318480783263e950d%2112000023994098510%21sh%21PK%210%21',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    headers2 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'ali_apache_id=33.3.7.195.171103833369.250834.0; xman_us_f=x_locale=en_US&x_l=0&x_c_chg=1&acs_rt=5775120e60e64cdd86082ba1f0b79eef; xman_t=tXrA5c4nAQynhFSFCr2D7D94wiSZb12ZxzxXDvsVry/yBXiCl5lyd5VGGDrtqLZI; xman_f=jm0f5jboJFzwa4OApHkbAVPKD0fh3IN2FpOLGlwpj6SlldHpvQTR0awUXLQfwIbqBshpMU8WswIBRj4qz+5QP3zEoKLMTiBL7OlhR1r8Pr8HwIUdECMwoQ==; cna=gE2DHvIILnICAba6W2XkPAiC; _bl_uid=6hlt8umh1pdggh1p4p0F4RaydCL9; aep_usuc_f=site=glo&c_tp=USD&region=PK&b_locale=en_US&ae_u_p_s=2; _gcl_au=1.1.649691157.1711039730; _ga=GA1.1.1103341790.1711039730; acs_usuc_t=x_csrf=133aocenjoezt&acs_rt=22e9e193a37c4eaf92592ea330a46997; intl_locale=en_US; AKA_A2=A; _m_h5_tk=5e17ac62e7d50c01434289a59d1f79ad_1711205896264; _m_h5_tk_enc=a965717076ff86e4a24fc2962cd48c3b; XSRF-TOKEN=f4ecc7e9-74ec-4c10-b0d3-161f3a908d8d; AB_DATA_TRACK=472051_617388; AB_ALG=; AB_STG=st_StrategyExp_1694492533501%23stg_687; _mle_tmp_enc0=Ey%2Fp8LswzxA3J47VsqxI%2B550XxyB5kykSJ2YVlpaAfdq5JC%2FC82nNvMUtC7jqPEUtVxHSPQMqO77SGciTl0m2TUTS0kX6OP30ZcuxvjA7M7ZyOeT%2BTZj79cLEbT7W5yh; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005005121226630%091005004966253444%091005002190149281%091005005654367888%091005003999468972; _ga_VED1YSGNC7=GS1.1.1711203768.6.1.1711204696.60.0.0; isg=BFNTgEAvMoR4lP5Sqt_MaNmU4td9COfKWVTDOQVwr3KphHMmjdh3GrHUuuzqJD_C; JSESSIONID=AD2F13280ACFCD536CFC7DFDE5FB4B0E; intl_common_forever=kPkqcoSY5eryOREbkbKUOzqIW/8hEQAJS5rSqSG2PaMTXCKehc4dkw==; AB_ALG=; AB_DATA_TRACK=472051_617388; AB_STG=st_StrategyExp_1694492533501%23stg_687; _m_h5_tk=e3e02cb7d68e5641e92a50701dbba704_1711054235953; _m_h5_tk_enc=36e2d3022d42dbb7b21b5dfeae479976; aep_usuc_f=site=glo&c_tp=USD&region=PK&b_locale=en_US&ae_u_p_s=2; ali_apache_id=33.27.96.9.171104962843.534166.2; intl_common_forever=6ERhZTEerRUTxr6tyLVvpn1U2w4TL7hpbUNdEgtpDXYNvqQ7wiHhsg==; intl_locale=en_US; xman_f=RJqu04DhFJGZ+rFzLVEqcQ9EPzevH60+KcblB0v9Iv44CL8tYeQZ7UzVXjr3ZsByhy7cMWPFjWh6e7SUiPRvVJJqYSrz40WVp+tx0tzYTcKv1QX4OkDbVA==; xman_t=N7/ete3/SSTdGIRU1z19ilVw5Cycex4mcyv+B9JWj2IXqZsDV78pWxHE9WlCeLjr; xman_us_f=x_locale=en_US&x_l=0&x_c_chg=1&acs_rt=5775120e60e64cdd86082ba1f0b79eef; JSESSIONID=79C8A2A833765CBE0FEC6963BF448740',
        'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    custom_settings = {
        'FEED_URI': 'Output/AliExpress (Complete Record).csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',

        # 'HTTPERROR_ALLOW_ALL': True,
        # "DOWNLOAD_HANDLERS": {
        #     "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        #     "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        # },
        # "DOWNLOADER_MIDDLEWARES": {
        #     "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        # },
        # "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # "ZYTE_API_KEY": "ee00661bba154a9f971a673b231b675f",  # Please enter your API Key here
        # "ZYTE_API_KEY": "",  # Please enter your API Key here
        # "ZYTE_API_TRANSPARENT_MODE": True,
        # # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def start_requests(self):
        file_path = "input/AliExpress_Bikes_urls.csv"
        addresses = []
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                address = row['URL']
                if address:
                    addresses.append(address)

        count = 1
        for address in addresses:#[20:40]:
            print(count, address)
            count += 1
            # address = address.replace('www.aliexpress.com','www.aliexpress.us')
            yield scrapy.Request(url=address, callback=self.parse, headers=self.headers,)

    def parse(self, response):          # Meta title, Image-(URL),  SKU,     Price,
        # Description,
        item = dict()
        data = None
        javascript_data = response.css('script::text').get('').strip()
        pattern = r'window.runParams\s*=\s*({.*?});\s*window.runParams\.is23'
        match = re.search(pattern, javascript_data, re.DOTALL)
        if match:
            json_data = match.group(1)
            json_data = re.sub(r'([\{\[,])\s*([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', '\\1"\\2"\\3', json_data)
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)


        name = data['data']['metaDataComponent']['title']
        item['Name'] = name.replace('AliExpress','').replace('Full Fairing Kits','').replace('|','')

        string = response.xpath("//meta[contains(@property,'og:title')]/@content").get('').strip()
        pattern = r'(\d+(\.\d+)?)US \$'
        # pattern = r'(\d+(\.\d+)?)PKR'
        match = re.search(pattern, string)
        if match:
            price = match.group(1)
            item['Price'] = price
        else:
            item['Price'] = ''

        make_model_image = response.xpath("//meta[contains(@property,'og:image')]/@content").get('').strip()
        url_elements = (make_model_image).split('-')
        collect_words = False
        extracted_elements = []
        for word in url_elements:
            if word == 'For' or word == 'for':
                collect_words = True
            elif word == 'Full':
                collect_words = False
                break
            elif collect_words:
                extracted_elements.append(word)

        item['Make'] = ''
        item['Model'] = ' '.join(element.strip().replace('.jpg','') for element in extracted_elements[1:])  # description
        item['Image (URL)'] = data['data']['imageComponent']['image640PathList']

        item['Description'] = ''
        for check in data['data']['productPropComponent']['props']:
            if check['attrName'] == 'SKU':
                item['SKU'] = check['attrValue']
            elif check['attrName'] == 'Motobike Make':
                item['Make'] = check['attrValue']
                # print('^^^^^^^^^Make^^^^^^^^^', check['attrValue'])

        item['Meta Title'] = response.xpath("//meta[contains(@property,'og:title')]/@content").get('').strip()
        item['Meta Description'] = response.xpath("//meta[contains(@property,'og:description')]/@content").get('').strip()

        description_url = data['data']['productDescComponent']['descriptionUrl']
        if description_url:
            yield scrapy.Request(url=description_url, callback=self.parse_desc, headers=self.headers2,meta={'item':item})
        else:
            yield item

    def parse_desc(self, response):          # Description
        item = response.meta.get('item')

        selector = Selector(text=response.text)
        description = selector.css('span::text').getall()
        print_D = ''
        lenn = len(description)
        for element in description[:lenn-1]:
            if element:
                print_D = print_D + ' ' + element.strip().replace('\xa0',' ')

        item['Description'] = print_D

        # print(item)
        yield item





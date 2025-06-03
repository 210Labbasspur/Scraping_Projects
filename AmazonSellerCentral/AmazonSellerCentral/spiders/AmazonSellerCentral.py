##############      AmazonSellerCentral

import csv
import time
import json
import scrapy
from copy import deepcopy

class AmazonSellerCentral(scrapy.Spider):
    name = 'AmazonSellerCentral'
    prefix = 'https://sellercentral.amazon.com'
    # url = "https://sellercentral.amazon.com/revenuecalculator/productmatch?searchKey=B07Y2LLF8L&countryCode=US&locale=en-US"
    url = "https://sellercentral.amazon.com/revenuecalculator/productmatch?searchKey={}&countryCode=US&locale=en-US"
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cookie': 'regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19602%7CMCMID%7C43557311998786081651059438907057470473%7CMCAAMLH-1694154863%7C6%7CMCAAMB-1694154863%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1693557265s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1693550067410-704954.47_0; i18n-prefs=USD; ubid-main=130-5240559-4511615; sp-cdn="L5Z9:NL"; sid="+Nd9Q9gfkf9hSF41ASbrMw==|4V3HHV5xbeg26g0v2I97O4mVNSq9g3+cXKXye2RmkNE="; __Host-mselc=H4sIAAAAAAAA/6tWSs5MUbJSSsytyjPUS0xOzi/NK9HLT85M0XM0dgl1NfMK9I6I9HN1VtJRykVSmZtalJyRCFKq52hs4mTuERHuHOnpYhwOUpeNrLAApCQkLMDF29M7wsDFNUipFgCCVa9CdQAAAA==; session-id=147-0972943-8726217; csm-hit=tb:XZPGMWE75EFPY4C22NYV+s-XZPGMWE75EFPY4C22NYV|1718037661541&t:1718037661542&adb:adblk_yes; session-id-time=2348757668l; x-main="uHkeOBhX7yBAE8Ism?S9@jeMZGgmmqlSADNb0uV2SxLmrENXKU0gZdBgH0cvKK4Y"; at-main=Atza|IwEBIH0bRNKKkoVyIMMY38d3nstAg1k13DLP83L6e7r6DM-MDz4TEiQ-hcuHYRK3wXoK54rAuKznKsNx4TwBh2btXxCyqTAUJ6JBOYybTir6cSwEQLId_kY3b7Ooxo7z4cSG2VZ79D_FuwV10HAfhxwqLNFI-aErYIPWBrcnXJHIwslcSa0GKQMQdnLEDhJDnEq_hT81fe6qsAh5EYid8e467qIYyg7JaRbrcPU15alKrkJJNw; sess-at-main="eB+XfcuBd+jR2vpnP6+XzM8Et1ojoeIBI4GHmXMXRNI="; sst-main=Sst1|PQE4sE8U7l3AvzQpY709NIxICXEhlXt9emjQUgBBsIpRjcQ8EUKqM-SaXj3K1GSxJZTpd30tLvB5z7xyplXAH6I6-KnzFrq0yYlC32SeEYDQkgItH03It_CLuoqqjT78uPdGKTVuA3jv3YOVqzpNfE-doFjlG19anPqQ3wxnrP1qjJHAZglXklogQsXyDYToAnxABgGJqcJLBWEEOlKET3Sl2l7VMkf1nqYgdN_CPBi1Ja7jTezWbyIGaSBxhW40zWqDIb9rQk8QpZJrnBNMTSbUOsOXGAhE5I3Hp0JbePRKNn0; session-token=wO8rym3QJ8t62Jh6L6j1bGqToT7C9kxsQcigEwFGRrVwbckNW9G123SVS0KoTunoOdN8N3sUDClqzwFzQjFzc9TVrFk6YGgbjgTuSRUKh7IRqck03Ov8wBpm/jpv/TNGpheFS49cDALZ/Mk0IvHkuDolYb0uHF1RShcJ9O5Rd8FQUILU37P3Eb3Gr82/jHhfE/hfCNMNibhZgaCZr3YTLL+zmRROy/Flzb8lnJP2R3Ctq0d3bUhCrCAWzL716y4YJt70cnk9iYE3j/B7kAxKEIORfvo3FAQIBV7rXWZZloQb6j+dWtF3j3ms9FIYIqqlZLhaiwycwx9IiKJ1seGwVVcS83loeu5UW5W8DSgfh24iqEvvE4uz91TotsvzQgbW; arp_scroll_position=405; session-id=140-9618907-8062131; session-token=oV9gTnEFnC/Akk1YTjT7TKNUmLbzJAonijU1Jy1k93n1qpchClMPYmhtsnLKsidjE5CGh+/Qh8K4hkHLC2CKDYun8DY6jUHBjBF1J4w/wNkW00SxonMaMku/QaAmMTGaMnXMiwR+4hB/23rdczSlLxYOdjYaN4vyMtjBZDUBU7uiwX9NOKmdziEq6rhFSoOIY0CG1aq4jHCm9+qsffSvbs9iWiEepyJkGi9l/g6JXawnVDYnk7ezlOzjj6TLuWrYTdrtRYtYr8IEZGvRGnFV0I7Q3Ng4RhsWL8Bo7ZeCD77qUV1OuTfPoszHgTThfemJpDUTfSMsDIBHTGQO0R9pW9hUhbLWDpaHZaRdTtt1rTceWeG3k0joQf/AYMOv97+c; ubid-main=135-2597626-2575268',
        'priority': 'u=1, i',
        'referer': 'https://sellercentral.amazon.com/revcal?ref=RC2nonlogin&mons_sel_dir_mcid=amzn1.merchant.d.ABNJ3QBZQRBQPXBKR76O3HZLREAQ&mons_sel_mkid=ATVPDKIKX0DER&mons_sel_dir_paid=amzn1.pa.d.AAH7EM5CDE36C2SJ5SNFOTIYGIAA&ignore_selection_changed=true',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    f_url = "https://sellercentral.amazon.com/revenuecalculator/getfees?countryCode=US&locale=en-US"
    f_headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        # 'anti-csrftoken-a2z': 'hMJx+ywvPyaAtz7+SliNbN/Vi2f3MZJPoa12zwI2HjNJAAAAAGZnY0M3MzRjYmI5Yi1jYzU5LTRjNmQtYjhmMi0yM2ZkZmM4YzNiNDU=',
        'content-type': 'application/json; charset=UTF-8',
        'cookie': 'regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19602%7CMCMID%7C43557311998786081651059438907057470473%7CMCAAMLH-1694154863%7C6%7CMCAAMB-1694154863%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1693557265s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1693550067410-704954.47_0; i18n-prefs=USD; ubid-main=130-5240559-4511615; sp-cdn="L5Z9:NL"; sid="+Nd9Q9gfkf9hSF41ASbrMw==|4V3HHV5xbeg26g0v2I97O4mVNSq9g3+cXKXye2RmkNE="; __Host-mselc=H4sIAAAAAAAA/6tWSs5MUbJSSsytyjPUS0xOzi/NK9HLT85M0XM0dgl1NfMK9I6I9HN1VtJRykVSmZtalJyRCFKq52hs4mTuERHuHOnpYhwOUpeNrLAApCQkLMDF29M7wsDFNUipFgCCVa9CdQAAAA==; session-id=147-0972943-8726217; csm-hit=tb:XZPGMWE75EFPY4C22NYV+s-XZPGMWE75EFPY4C22NYV|1718037661541&t:1718037661542&adb:adblk_yes; session-id-time=2348757668l; x-main="uHkeOBhX7yBAE8Ism?S9@jeMZGgmmqlSADNb0uV2SxLmrENXKU0gZdBgH0cvKK4Y"; at-main=Atza|IwEBIH0bRNKKkoVyIMMY38d3nstAg1k13DLP83L6e7r6DM-MDz4TEiQ-hcuHYRK3wXoK54rAuKznKsNx4TwBh2btXxCyqTAUJ6JBOYybTir6cSwEQLId_kY3b7Ooxo7z4cSG2VZ79D_FuwV10HAfhxwqLNFI-aErYIPWBrcnXJHIwslcSa0GKQMQdnLEDhJDnEq_hT81fe6qsAh5EYid8e467qIYyg7JaRbrcPU15alKrkJJNw; sess-at-main="eB+XfcuBd+jR2vpnP6+XzM8Et1ojoeIBI4GHmXMXRNI="; sst-main=Sst1|PQE4sE8U7l3AvzQpY709NIxICXEhlXt9emjQUgBBsIpRjcQ8EUKqM-SaXj3K1GSxJZTpd30tLvB5z7xyplXAH6I6-KnzFrq0yYlC32SeEYDQkgItH03It_CLuoqqjT78uPdGKTVuA3jv3YOVqzpNfE-doFjlG19anPqQ3wxnrP1qjJHAZglXklogQsXyDYToAnxABgGJqcJLBWEEOlKET3Sl2l7VMkf1nqYgdN_CPBi1Ja7jTezWbyIGaSBxhW40zWqDIb9rQk8QpZJrnBNMTSbUOsOXGAhE5I3Hp0JbePRKNn0; session-token=BaLUP8HV4lAEq+jyPTKaR1PC9s3uuNlS5BVcIYWI8UEElOxreBTJdj4MCDgbUa7foj9UDxB/98sehD2xV2QGXmVpFoGq/FlmDsxF8/STaKFJdBTh3F3wIE07IzvI4YyS0817s821xMP0QSTtVUWSu1IDQfsGAVIkclK4ASBN5r7mTkh6UNwvm0IpHsVjf8fsThE0bp59CVsRSNj50t+1rQQV7XYsGoy11YZchj1+xroqtDZDXORydNW3QPQxGe24u+9D2CqfHuMW9re06L7kIyUcW37b4mGLBqegYQhjXUDWFMxpYGhmqo00aO3q7hdrVIGh9F7m2WOAjHHcg8OxkZCGHug7gIPqqLpJoqeQsA+ZpE67wuSl75JucFmSUAQX; arp_scroll_position=505; session-id=140-9618907-8062131; session-token=oV9gTnEFnC/Akk1YTjT7TKNUmLbzJAonijU1Jy1k93n1qpchClMPYmhtsnLKsidjE5CGh+/Qh8K4hkHLC2CKDYun8DY6jUHBjBF1J4w/wNkW00SxonMaMku/QaAmMTGaMnXMiwR+4hB/23rdczSlLxYOdjYaN4vyMtjBZDUBU7uiwX9NOKmdziEq6rhFSoOIY0CG1aq4jHCm9+qsffSvbs9iWiEepyJkGi9l/g6JXawnVDYnk7ezlOzjj6TLuWrYTdrtRYtYr8IEZGvRGnFV0I7Q3Ng4RhsWL8Bo7ZeCD77qUV1OuTfPoszHgTThfemJpDUTfSMsDIBHTGQO0R9pW9hUhbLWDpaHZaRdTtt1rTceWeG3k0joQf/AYMOv97+c; ubid-main=135-2597626-2575268',
        'origin': 'https://sellercentral.amazon.com',
        'priority': 'u=1, i',
        'referer': 'https://sellercentral.amazon.com/revcal?ref=RC2nonlogin&mons_sel_dir_mcid=amzn1.merchant.d.ABNJ3QBZQRBQPXBKR76O3HZLREAQ&mons_sel_mkid=ATVPDKIKX0DER&mons_sel_dir_paid=amzn1.pa.d.AAH7EM5CDE36C2SJ5SNFOTIYGIAA&ignore_selection_changed=true',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    f_data = {
        'countryCode': 'US',
        'itemInfo': {
            'asin': 'B07Y2LLF8L',
            'merchantSku': 'ace-1014845',
            'fnsku': 'X003F1IZ1X',
            'glProductGroupName': 'gl_home',
            'packageLength': '7',
            'packageWidth': '3',
            'packageHeight': '2.5',
            'dimensionUnit': 'inches',
            'packageWeight': '0.5004',
            'weightUnit': 'pounds',
            'afnPriceStr': '15.95',
            'mfnPriceStr': '15.95',
            'mfnShippingPriceStr': '0',
            'currency': 'USD',
            'isNewDefined': False,
        },
        'programIdList': [
            'Core#0',
            'MFN#1',
        ],
        'programParamMap': {
            'Core#0': {
                'inboundingFeeParam': {
                    'regionLocationsMap': {
                        'West': 1,
                    },
                    'serviceOption': 'Premium',
                    'unitToInbound': 1,
                },
            },
        },
    }

    custom_settings = {
        'FEED_URI': 'output/AmazonSellerCentral (Record) .xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    count = 1

    def start_requests(self):
        file_path = "input/asin test list.csv"
        addresses = []
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                address = row['ASIN_No']
                if address:
                    addresses.append(address)
        # addresses = addresses[:90]
        for index, asin in enumerate(addresses):
            print(index, asin)
            time.sleep(2)
            yield scrapy.Request(url=self.url.format(asin), callback=self.parse, headers=self.headers )

    def parse(self, response):
        data = json.loads(response.text)
        if data.get('data').get('myProducts').get('products')[0]:
            item = dict()
            # item['Ser'] = self.count
            # self.count += 1
            asin = data.get('data').get('searchKey')
            item['ASIN'] = data.get('data').get('searchKey')
            item['Title'] = data.get('data').get('myProducts').get('products')[0].get('title')
            item['Weigt'] = data.get('data').get('myProducts').get('products')[0].get('weight')
            item['L'] = data.get('data').get('myProducts').get('products')[0].get('length')
            item['W'] = data.get('data').get('myProducts').get('products')[0].get('width')
            item['H'] = data.get('data').get('myProducts').get('products')[0].get('height')
            item['Price'] = data.get('data').get('myProducts').get('products')[0].get('price')

            ####        Payload to extract Fulfillment COST
            merchantSku = data.get('data').get('myProducts').get('products')[0].get('merchantSku')
            fnsku = data.get('data').get('myProducts').get('products')[0].get('fnsku')
            payload = deepcopy(self.f_data)
            payload['itemInfo']['asin'] = asin
            payload['itemInfo']['merchantSku'] = merchantSku
            payload['itemInfo']['fnsku'] = fnsku
            payload['itemInfo']['packageLength'] = data.get('data').get('myProducts').get('products')[0].get('length')
            payload['itemInfo']['packageWidth'] = data.get('data').get('myProducts').get('products')[0].get('width')
            payload['itemInfo']['packageHeight'] = data.get('data').get('myProducts').get('products')[0].get('height')
            payload['itemInfo']['packageWeight'] = data.get('data').get('myProducts').get('products')[0].get('weight')
            payload['itemInfo']['afnPriceStr'] = data.get('data').get('myProducts').get('products')[0].get('price')
            payload['itemInfo']['mfnPriceStr'] = data.get('data').get('myProducts').get('products')[0].get('price')

            #     # '''   Cookies using Scrapy  '''
            f_cookies = response.headers.getlist('Anti-Csrftoken-A2z')
            print(f'Headers2 Cookie: {f_cookies}')
            headers2 = self.f_headers  ##     Headers for Listing
            headers2['anti-csrftoken-a2z'] = f_cookies

            yield scrapy.Request(url=self.f_url, body=json.dumps(payload), method='POST', callback=self.f_pages, headers=headers2,
                                     meta={'item': item})

    def f_pages(self, response):
        item = response.meta['item']
        data = json.loads(response.text)
        if data.get('data').get('programFeeResultMap').get('Core#0').get('otherFeeInfoMap').get('FulfillmentFee'):
            item['Fulfillment Cost'] = (data.get('data').get('programFeeResultMap').get('Core#0').get('otherFeeInfoMap')
                                        .get('FulfillmentFee').get('feeAmount').get('amount'))

            print(self.count, item)
            self.count += 1
            yield item



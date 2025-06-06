

import csv
import scrapy
from copy import deepcopy
from scrapy.http import TextResponse
from scrapy.selector import Selector


class CatalogMannFilterDataSpider(scrapy.Spider):
    name = "catalog_mann_filter_data"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'cookie': 'JSESSIONID=5831B29CA6152921230A927C2C19FA37; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _gcl_au=1.1.78660972.1716318682; OptanonAlertBoxClosed=2024-05-21T19:11:38.074Z; _gid=GA1.2.730351489.1716318699; _gat_UA-84202635-11=1; arp_scroll_position=300; AWSALBAPP-0=AAAAAAAAAABVdrD1UpMc0kxEcxe5dtlFtZ7aAiEojv39PWbDG+KOY8QtI1PKcdRa++nMkmU8w5Syop0EXco5WSLh/b5BlKCc5mcS9fpTkhjR52uRUOqh82ag9LTcQY6n4aKPg/S6TrRS4w==; _ga=GA1.2.374264585.1716318682; OptanonConsent=isIABGlobal=false&datestamp=Wed+May+22+2024+01%3A16%3A33+GMT%2B0500+(Pakistan+Standard+Time)&version=6.26.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=%3B&AwaitingReconsent=false; _ga_1WLEWC49T8=GS1.1.1716318682.1.1.1716322597.0.0.0',
        'faces-request': 'partial/ajax',
        # 'origin': 'https://catalog.mann-filter.com',
        'priority': 'u=1, i',
        # 'referer': 'https://catalog.mann-filter.com/EU/tur/catalog/MANN-FILTER%20Katalog%20Europa/Ya%C4%9F%20filtresi/W%2011%20024',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    data1 = {
        'javax.faces.ViewState': '',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.render': '@component',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
        # 'javax.faces.source': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.execute': 'productDetail:productDetailUsageTab @component',
        'org.richfaces.ajax.component': 'productDetail:productDetailUsageTab',
        'productDetail:productDetailUsageTab': 'productDetail:productDetailUsageTab',
    }

    data2 = {
        'javax.faces.ViewState': '',
        'name': 'FORD',
        'javax.faces.source': '',
        'javax.faces.partial.execute': '',
        'org.richfaces.ajax.component': '',
        # 'productDetail:j_idt381': 'productDetail:j_idt381',
        'javax.faces.partial.render': '@component',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
    }
    data3 = {
        'javax.faces.ViewState': '',
        'name': '',
        'javax.faces.source': '',
        'javax.faces.partial.execute': '',
        'org.richfaces.ajax.component': '',
        # 'productDetail:j_idt383': 'productDetail:j_idt383',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.render': '@component',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
    }


    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": 'Enter_your_Zyte_API_Key' ,
        "ZYTE_API_TRANSPARENT_MODE": True,
        # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def start_requests(self):
        for input_dict in self.read_inputs_from_csv():
            url = input_dict.get('link')
            yield scrapy.Request(url=url, callback=self.parse, meta={'input_dict': input_dict})

    def parse(self, response, **kwargs):
        input_dict = response.meta.get('input_dict')
        page_url = input_dict['link']
        mann_codu = input_dict.get('\ufeffmann_codu')

        payload = "productDetail=productDetail&productDetail%3AproductDetailTabPanel-value=productDetail%3AproductDetailUsageTab&javax.faces.ViewState=IzNBZ%2BG%2BDBmaqTKjX%2FZ9LPo%2BcH1T255CBUgOOyiwC755zFz9C%2Fxcqlr2cnAHqA5jdjxLDBgDSsC%2B%2FgaKxNkCHKNS7k3PVo3opOyM4vZe%2Fl8Jahx5n0FwK6vMEELw%2BfozJFNsP1ja5iGfnUR3MBQSP63cijEeokpvIfus4wFHLJJIPvAfB2zCgALeLLFczSMxFHV%2FSMCDSpSmfg0835Ew4HIft3c49Iwqj9S375%2BNMq5m07xhpVNey%2Bd2qHCPe1d4%2BXeiPZcW2J4AdqhAaEwCT1GL%2By%2BUxhqVg2Tak5DwKkQSZ9A0tNAJxbB8zW9d0RNRx%2FP%2FO9ytnB94awjedCh4xCf1g4zFo%2FT3ump7LNXMAwtmqFdYqDC4hFXD%2BlkzC1MjRBCbpgtLTwAsO4K11%2BefFPrhAarC3f54YvrYdTBnu3p%2FAEqhnRPC2d5T2OtxfG6qn485HcMBNwe5eWAG5NWqwCxx3bW8NZXaT8DrJNZgv4YV38%2BmGsNoPCQPP50KY1qVZiPmjQ%2FELxXYbWloUiKjRcRSbzBYrgat45OPU10StC7q0ML%2BHktvL3MznpJM9QyjQ76kCeILTImsqtL3UExOW5dAGKl5%2BZbn29Hq1IuqFT3gO%2FenmU%2FhYylgSEWkLU%2B3ajYcsDpZoqAnRECa2MwXFYMwx3KMTY8iMlkBcZex7QqJjMycs39wZbg4BAFxAjijqdTRCmU8q82dFkClwLiKSqYEd%2BolMa3ncvgmkywXo3Qka2a3EZKzWwPt2gG%2BGYOa9pKMM%2FkWLxpqRxmQ9dXox32%2BJfKLYaqNtVs7uiQsqEDN%2BsIoGNWHfrqw96XO3y4AA8deitCZxYmwGAEoFJV0mpaZi5ljMSp1VRjufiXsvZ23Y5S%2BsSD3ZC8WFMqZNM7eJJ02ODFbxJksE5cufQ9vfLJQ0P%2BNAUWGIWDiPqKvgmRMw%2BrVfWQ3TReiBRxAcooSc0DJJW4Ls626p0oyrEbnsZLIq43WH0i0PKmjz12ivKEKJxEAuSExFeL6oRheOZDtfvwFs64%2FJ7oKX06NQ%2B4tbhsewdbXYwZFt3VwGDk%2BxfgJZ601rgkLshrhljkD3U0tLJnUulT76S%2F3FlWTjjHK7cu3qeZ6dN%2BuDvEZDfDxR8y31DZQsiDur%2Fy5efNR4H0ybGditonDL1W9fPxVLh78iJVZPNHARB4psOiypFP8IsVMOFXKoyERBBPM8KPnpByfwH5sxOzZ0SftRyCMbGt9JxuxiJBtgx9AlZBuc%2B7yjzqX3wAMOahyHDgtJJ0E05J7PQknT1Rzf%2F9o1%2Bgv637IOKQi48x12h%2FtoSubcnaQMszOwr6dX4LdIhvE6G%2FpFtVRgdRrGIEGA7VFFHskVkkiDe%2BBp7j5ocpOAAk%2BMiyGBwOHgHYVFbQRmnPrbs%2BvsCzJjlqLXpPjYpl2z1kGc3sPR%2FEY%2FX9jF%2B0VCnIpUYTInW06YCrv1Ka05EzUxe8J95UbtY3mwFHcTeVsxe7GnPNMucMQQigp9L2gtZzIdbZiKwLzWTq8weVfy2ObWpbmOc9bQkaZC%2BU0bjGy3qKftVzDsqtOZUk5AZYAFrLANB2L9XgU2fwYiVi2X6M6a5m%2BDjL5aYb70hadLM3G0DPBBIvkSV0b3hHM%2Fppr6Ev%2FzK%2BdzfnD8y6LanEsZCz3WVCEkCAzNQoBuybqDxYpagNWDeuRJSSb8W66OBynHJmYb7K1zdDXFAwY5tyqLKd%2FycNBelMaCuRxd3wFV8rTjJqSXqcyP5ewlkCI%2BqWSQ5kSI0tOn2k61rXj2i7aSMGLOFE%2BS9HUGy4nQfyoiqO%2FU5k55GU1So8zqUMNuZPAHMPf6R5umnjYTyYtMWYpEK4BZstZMXNKoEDzDjV9lL2tJtFs5bsONQ%2B3lDTPNGt9UZGTBKeg%2F224iCndwtJwd4iw1Ql4Cgg%2Bs5EA8aPr%2B8ZcppFOwH%2F1P0sPm1Mlfj%2FJuU%2BGeLITIki8RYXdf%2BI7Y3rRcyv7lIzPJeskOiTsIW1ijmb%2BKNaUm%2FqOsLajGIwq%2B%2Fi1qpmlVlV6LOlwbp4toN0WDQFJIElWAzu7z6LqvDT0uULPzKUGbHA8MXjAe5xQg80Vu0X8OtsRLM37O1NssjH%2B8d128XWJKMgHZz15r9QxWzYmDdOGSTId6BkjZYKInyNUNqKB9vgcXIc7hnC8ATfkNq8OOtOPo5P1oPgurZ%2FCz5g%2Fy%2BDoaEA%2BvbRcUJ%2BwdNlWTuiTahes8ThAX871RC6TvdbKKBsWmjZU0y%2FX1v9DwMJ4zQyW9dRCrlp504agSVP%2F7S03fylYtQwq8zKSSgJgN%2FsDFWprl%2F5J1R9fmDiSJlrF6yh8qjs57lkSBM5jOk9qrXfG7qGkCR0AAQhWgeh2GzNbktFY6lguxyEtjipK1MKzGVJOC%2FwRikacfMjaHs6B7yfVO63TpwEzDzHpa2wu%2BJDhIAj7OtPkMRLnyIDi2V7XfDWN3WmQoCQqXjiClkcHGdVQBP%2F4%2FImQvOu1BVv3bKYvNcLEYxl81TyZWuZxPemtLqBfcB%2BKhDqMIuluhcqQ6Taacgb7UWBimdAERozGZnMiZfXlM3dupU1xV8kI1%2BwldCI1dBj4kUMMEEwaNsofOQjid%2BZAoAWtVr9xbcu86pAYdKqN2zfpt7i8qE2HQJCpsH%2BDrjnoWeLWjMZ82Arh5iOGSBF0NcmejThujMe%2B%2Fs2ww8o%2FfQFTWpDlHu0l8SFrb0OwTZs%2BSXFUNNgXi5AvktBQNG1g%2F77zfvAycADKqzCz0tWWSYjqKO1FSqFqTgOEFk7qwky7qPrRHdsCV3FHrC6IXeOwUCYQ%2FkWnCMsPR1fX3A04h8doZ5%2Fpka1sg6DkWmLgDu%2FWVsN9v627Z%2F5KfM%2FTK1LUDEl0Gk0r4nL43Rez2%2FJvXDsyVr799ziTeJIFjBrnL%2B83j%2FjNSRO2bUhD1nMQ8Kc5PGwUsaqJCUJ9%2BRDR4qVofoji8fDBQV10FYqb%2BfWVUHmsCMN7Q3WmsqjGCOxaBg1QxYxH5WTmmc8KjflNZWy496p7C%2BnNynyYHq6GbRwwqnHTGbrmTvHkbYUA44nyUpiHtCP81VCZ7Bs6PJpmGoZsU8ziNM%2BeAXy%2BksNmYZuEexAn0A8QsroEEfE0vFqVYlB%2Fd63bI69ox51eHFtS6BBCq8be638JVW5glxzHVmsfj3MFq9v9rxkPyEXx9d1nBECCtQjlkiki%2BKkAYQPuiyDBM1hOaWZmu9pxoBMGmaGztAt%2BHgiPS43hHFTI9Kf3Lw3VzzYXySGnF9vrKBjWXEaRPiXWUFPAjyZh9i0Y%2F0r65KqPnSfR%2BKnT7Ijg1IFsTHmAQNXLdUzVIkVyfc%2FP3%2FXSIa6wU%2FPYImujyCgKYYXunyhilAbQo2KjkopajHYfaiD%2B6gyDJWMtmhVfczZfBp%2BI4DN%2Btob0CPCWci15s%2BG%2FmRv%2Fyj9n0tGzsxzDkltSAERulPZvOBzAem9w9Gq6swWIO0k9U4gCvWeyQWDuQMuoKR5oZeB680w4N17D7upyX8EwZc3NcXJeI3C2Px%2BPDMtQs8bwO5nnulWKuWmg1etFVpoO6Se4ZPdAnJf%2FA9ZuIxwUGT4svjXMidUapRLMAwfRa7Y6bXco8BzSemosDEa1BzKYv7v%2BC1TM2BPDm5Oenno%3D&javax.faces.source=productDetail%3AproductDetailUsageTab&javax.faces.partial.execute=productDetail%3AproductDetailUsageTab%20%40component&javax.faces.partial.render=%40component&org.richfaces.ajax.component=productDetail%3AproductDetailUsageTab&productDetail%3AproductDetailUsageTab=productDetail%3AproductDetailUsageTab&rfExt=null&AJAX%3AEVENTS_COUNT=1&javax.faces.partial.ajax=true"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': 'AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _fbp=fb.1.1715865419592.468009327; _gcl_au=1.1.213365692.1715865420; OptanonAlertBoxClosed=2024-05-16T13:17:07.235Z; _gid=GA1.2.441703802.1715865427; JSESSIONID=ED64D764283B0AAE4E61C740136675F1; OptanonConsent=isIABGlobal=false&datestamp=Fri+May+17+2024+18%3A07%3A11+GMT%2B0500+(Pakistan+Standard+Time)&version=6.26.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=%3B&AwaitingReconsent=false; _ga=GA1.2.1721240160.1715865420; AWSALBAPP-0=AAAAAAAAAAC/k8blnwhhVnqvzE9+Xr52fEduXntSAJHn7NBOHUSWXkycyVXjMVtU+9/HlJfT8WEZpngLwNbVvgTTWZ8Q8yCQmXDX5DB9pxlHOC0kx0hwpkqFkM8vK2/JeXR3sAEhRyPoww==; _gat_UA-84202635-11=1; _ga_1WLEWC49T8=GS1.1.1715949378.9.1.1715953973.0.0.0; AWSALBAPP-0=AAAAAAAAAABd3Gx6xc75DQHAq2LZiGk6uGJkEoQCfIJFYJbo4BVr5Bnd79ppN49u2oa8X3rwB6fsEsBPrnc/DOH6q2klt5Xi3hc0phBM1t7Wfw2DZAEXastmNLtiu4YJt3kkhHLUiR+vtQ==; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_',
            'faces-request': 'partial/ajax',
            'origin': 'https://catalog.mann-filter.com',
            'priority': 'u=1, i',
            'referer': 'https://catalog.mann-filter.com/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        check_mann_codu = response.css(".borderBottom::text").get()
        if check_mann_codu and check_mann_codu.strip() == mann_codu:
            # Extracting filter type
            filter_type = response.css(".d-2of3 .productInformation li h3:contains('Filtre Tipi') + span").xpath(
                'string()').get().strip()
            if filter_type:
                filter_type = filter_type.strip()
            else:
                filter_type = None

            # Extracting GTIN code
            gtin_code = response.css(".d-2of3 .productInformation li h3:contains('GTIN kodu') + span::text").get()
            if gtin_code:
                gtin_code = gtin_code.strip()
            else:
                gtin_code = None

            # Extracting shipment status
            shipment_status = response.css(
                ".d-2of3 .productInformation li h3:contains('Sevkiyat Durumu') + span::text").get()
            if shipment_status:
                shipment_status = shipment_status.strip()
            else:
                shipment_status = None

            # Extracting product details
            product_details = ' '.join(detail.strip() for detail in response.css("li:nth-child(4) .d-2of3").xpath(
                'string()').getall()) if response.css("li:nth-child(4) .d-2of3").xpath(
                'string()').getall() else None

            dimensions_data = {}
            dimension_items = response.css(".last li")

            for item in dimension_items:
                dimension_name = item.css("h3::text").get()
                dimension_value = item.css("span::text").get()

                dimension_name = dimension_name.strip() if dimension_name else None
                dimension_value = dimension_value.strip() if dimension_value else None

                if dimension_name and dimension_value:
                    dimensions_data[dimension_name] = dimension_value

            # Set dimensions_data to None if it's empty
            if not dimensions_data:
                dimensions_data = None

            yield scrapy.Request(url=page_url, headers=headers, body=payload, method='POST',
                                 callback=self.extract_applications_data,
                                 meta={'link': page_url, 'Filter Type': filter_type, 'GTIN code': gtin_code,
                                       'Shipment Status': shipment_status, 'Product Details': product_details,
                                       'dimensions_data': dimensions_data})

    def extract_applications_data(self, response):
        page_url = response.meta.get('link')
        filter_type = response.meta.get('Filter Type')
        gtin_code = response.meta.get('GTIN code')
        shipment_status = response.meta.get('Shipment Status')
        product_details = response.meta.get('Product Details')
        dimensions_data = response.meta.get('dimensions_data')

        applications_data = []

        # Create a TextResponse object from the response body to use CSS selectors
        text_response = TextResponse(url='', body=response.body, encoding='utf-8')

        # Use CSS selectors to extract the text
        applications = text_response.css('.advancedList_label .label_lv1::text').getall()

        # Clean and print the extracted text
        for application_ in applications:
            application = application_.strip()
            applications_data.append(application)

        if not applications_data:
            applications_data = None

        payload = "productDetail=productDetail&productDetail%3AproductDetailTabPanel-value=productDetail%3AproductDetailCompareTab&javax.faces.ViewState=noB4EMUome9fp5%2BWgsCpvlre76f4grae6YR9OQAoXSZXv73MpucRkpAp0UsCrPod5JzCRQF9ajpq%2B%2BDv0DoE4TIcalbORUHy9wZlPJfbMh3une4hvJcj0Ti5mtn3DVUyLFbWj4GSLFUcO9CO4gq5u2J8G4dPpuF2oSxdu1r%2FnvO%2BoBVtL7%2FSyrUQTatEtn5iYK4u0OSOvE%2BscYrZ9AVK3r1x3k4JRpKgMUDJce35Y3dv8p5NzV%2FktPkEWj%2BBdO3pnVVIiM8%2BUX0SZpREtsvB6UcTYEFK9dV1Z%2F8fGL3tTVWFdRJSzuxA0AqJjF6qlKtiwaxHQCWTvSWopXK%2F7qBcF2gujbDRRMxvpBxKOUblVzTPJj9D%2F%2FChAEj7TZCKCbxWUZ1sMfHvoI%2B2DnOMmhKhANXIIp4zz%2Fl2q6Lh%2BTL7nsr4DwHJS8lIS3YjahNTc7G9MpdGVIrF1nDjcS2C45ZhLyc77xhPuAhpxpqaq12aerByBt8%2FzefL4F%2B3LvDzBlgI7p4TzsRFQnzsIbe2zjYjghkRsUv9Qz4tY76Loq1Vk2pQavJiyzi1r6xltIbMl4mUHIL%2FFGNnhWszSMTg25EuqvH%2FS7EJJp1rvXXZQw5vayyXQo%2FPX02hbWZe53jO5JvqD6%2FV5oTRnnR0Gpcohe1KkT4SbBqtqe28t6xF1amVVt%2BrYp7KNdyKeO5A6iwMwJzvu1kJVGMMBA44qUnUZkf%2BMSK0rqXV1EHj2MGU1rzRyekKCDms1Exfar%2FOFhQrBzb6oWDADt%2Bgp%2F8cLwz55yn7GIJK%2BH5rmX%2Fy%2BvctM9y6XmTXCcmhCFsh78DdMO%2FBwYyTxfgP6Ewf5%2BiMszMsnDe5HbybRWADgoPiFkdtizpNTU1RfNJFirTo9yA0SDAGGXFMAH3JHDWXQAtomJ2DQmuva4cuYChsTEPRsiIfDk3vJoyDhZqur3SZIzNBmVH13kTqMELypsid64XaV37qZgBUMnl6LQ2w1HQJIaWRHCGe7F%2FpLaF%2FVJTJOzK1T56Qs0CiwLMVubSiXSBsTwSXGBJ%2BXbKEtEJPyXMM6CudLAhsc%2FDb6FnLabBHUmrHjXyzzdhR%2FUYFkP83HKW45AtsJ%2BJK4nPMJgL1%2FUhZXsVs9FxL21Onmb%2BK56EN9tquhPLY6fX4jhvU2%2BIGoGtvyHzbj5BCLPdBjKQnEnCBsw%2FS9tLDTJVY8Wf4hgF5vG8qb6pKp%2F7INhP1YmYPoIV2I215QnneXqizrVbgACqr6IVYOFluQS%2FBv3HLaCok4IZ%2Fhg4bEQnSZZGK9YZa0qeMhIytLC37yvrWJXJS7bWMxMQkKRYIByCvaR09%2BTUD8pQvEbQUzIeNbdTjjsM5Mh%2Fyju%2BIi84raLbE4YpzY10o1yz3pcoK5oCpY78kBXI2Ascw3qkTGAgdPw7kCuO0es1ES2c3OGmGUFV7CVfTY%2Fy9BDA3Wn%2F8LDtC87E8fm34hFuEpYhX2tngshAfzbsFDZNZh4Q%2Bm1ul%2FuzJ7IOaX5lMbGDAvHVqknZJaLmT9L7p0bJQUiB%2BD%2FOFT3Vp9AY95CgBKjDbW0et3Y9JRVZLj%2BFbSUlzag9lTKG2F%2BIYxqRTvJKOJQRf6XNFWBCEDchcW4E48v0kzoRAPeMjAKcMFozKut9OnZMSxTvSccZb02JfDgWQh7iu77YjPWlXbZRAEokqEK4rFmXr9dTNPV%2Be7Mz6U1BUeBb4vDYGhanxgsY3Q5pD7RPGgo%2B2agTo5mVBJUReK5ZOkwun291u2N4QsaEwxcmxbbWkP5HeADM%2FtXifQad7EXm%2Fvnxxzg6TA2HTyqStCxscMyaJbHtNbA1tDyTJakUmAvdHb%2FylNYpRgKlSFDYeLLbvqW5%2B9d3uOsJi8LJr%2FN%2BTfErUzvGYV477VHNhsS27fD6A8KZna4fhAK2hiRB889jqQgTQl8NVT36cHKVnKGJe6Uj8sOsbn8M6m58Km4RIBlQqzGkCu%2FyIQfNxS0wZ%2Ff8i6nSbUQeSL%2B8ohi%2BGu2l78NvUayvwNOmpSWhkVtG0RVujqSXVgShqdrx%2BebeIedN4ZdxKxEaae%2FoCQxxHzWeQIiKMUYdjap1xJh4vBAp%2BS6o0GwIyB%2F57cqXjDJdg9QplHxJmdAnL2O6He4Q3PYXw5UBJhiR%2Fmed8M81W9ddHDay3ZjQpSdza8jMDdDpPKFyvia5tj0woK1vgkuu%2F1f%2BBUon1a%2BTdMhIc06NVPgR%2Bo0zh60V1r%2BrYtG64ue0Eo0E3ipW%2B5hnIhMbVZ9eryZl%2FNEijHlz99lb4F%2FF8f%2FmumZVlGj6VoSlR7wDQj0G0r1Q7NfNntyZihczWe1QYscKu0m6ZStTAH7YGqCKm549BThYmPYF%2BFyh%2F5f4yKnrvuApGMU5blFVJH1eECA6F2nLwLRqv0AZp7pD3OPC8AyazkyzHG%2BfUIGu%2Bw5B400nSPvNOOOLlDVMAMQjKu8%2BSRIXxeIf3oReo7ZYh54ylbzV04IZd0i%2FWNGJRKzA5MB24AHR48AMjue7U6BUWFNC973Vi8762et6FdavWp47A49XrdlV81w3wM9IVIx9HuZgaf7Cc02AV9lS%2BGArgmnnE%2B76%2Fso1z7JVwfmLEGFRJphxJRqhR8z1yqk3LP5YxB%2F8ZFsR%2Ffv4bWYgtBhzK2evwl5BWWkNDP34x2WbiJgrpAuTer%2F4TDbcNqyyOTd%2FupcptYWs2xSlX9auYG4bK%2FeHMDiZ3BHvrZtq0wvf%2BVfOrZjZINoWCtfFgV%2Bhfp4Z%2FapSEGo2hzyLQWx%2FSrTuN5BLALium4eTfCWZf5x9XFy8pkEup85aO4t%2FTs375kHDGLmQwyGL8OFh66MzcS1jjSx10egYeT0HmrTD9VWpxkjOKFzQhfYi%2B%2BuHOIAgKImicHOlU34rw%2BnZypwIuisjjGhdmeF6pz5wUDT5SOQR3SaaS1aBw3Gosa8Hua93%2FvoVK0CQqDD4V0kW0RV8z%2FK1Q8Wxe4FiaS1nGgkLX2iQxDmc%2BaQoR6SHd2LkcowGYAy1SHT37x1%2Bj6Eh10c6iUTM5Cqk6ADca%2BXb0mJ13pcBGKZBtzC7CneifHxJtxE6dYzAEPIZKm4KQ61UwCExr1Ru%2B3%2F18SyPkmdGldGeX79G%2FLfu8XVLbQOLCiB9AxmIDoyHBL%2BhuXqKuaQoIRu4TUPte18qGONZZtgY3bWfIA9igbePharhu8ukQOi%2BlnolACBzw7HPUlnnrCn0QUJltl%2F8ZWFMPydAdFyxCN1DW6cG8nvwJU1xIV2dTsmn1sLKr%2BMDGlSxINpAr9hpbXxRffGGA6%2F6JOUVr1WJRCTLAbmBdr9k306fvO3MPegPui14TrS5kBdHvQwFwP52u2j9vXXALvB7J5J%2Bawwsl76UEnv1ksi9n9%2BuAcu01J2UGDdavjVJVBs%2FMnslsJRVRLDV0GS7u6cg9dUhxQEq738vvDzjHtdpzLdR5ENPL%2BXUWd%2BwT2sxqnfAos%2BjHGVx1Nq8S0ZRA%2FXHAtl0DKpNglh6J5ompVgn5%2FvSB%2B4QWpTa%2FdztjBgJ28dMdALIQ2q8iQPyOjGBGBucxWo8PUtnvZgztseXj65N4A8H4Kt%2BE8UkAFkhX9wh4v8f7RdqPchmuEl%2Faoj24orQs0TRyEevOQ4THOAPt3IzMoLkas6cT%2F90WSo6SQr1LfnUCy32pfvmF&javax.faces.source=productDetail%3AproductDetailCompareTab&javax.faces.partial.execute=productDetail%3AproductDetailCompareTab%20%40component&javax.faces.partial.render=%40component&org.richfaces.ajax.component=productDetail%3AproductDetailCompareTab&productDetail%3AproductDetailCompareTab=productDetail%3AproductDetailCompareTab&rfExt=null&AJAX%3AEVENTS_COUNT=1&javax.faces.partial.ajax=true"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cookie': 'AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _fbp=fb.1.1715865419592.468009327; _gcl_au=1.1.213365692.1715865420; OptanonAlertBoxClosed=2024-05-16T13:17:07.235Z; _gid=GA1.2.441703802.1715865427; JSESSIONID=ED64D764283B0AAE4E61C740136675F1; OptanonConsent=isIABGlobal=false&datestamp=Fri+May+17+2024+19%3A20%3A18+GMT%2B0500+(Pakistan+Standard+Time)&version=6.26.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=%3B&AwaitingReconsent=false; _ga=GA1.2.1721240160.1715865420; AWSALBAPP-0=AAAAAAAAAAAE6re46LV+Ql+KHmxo+OYY8CGvyIZBVEE2yGAfcZYpQlxZ2bQgSZrPI5yx/C9cWCQmqb6qoE7mjmubzIM7N+IzS04ndLJf75ioB7uwQ0fbz+S4FFjtRdD3KZEh88RJEyqc4g==; _gat_UA-84202635-11=1; _ga_1WLEWC49T8=GS1.1.1715966675.10.0.1715966675.0.0.0; AWSALBAPP-0=AAAAAAAAAAAjUqDrTpA2mrX/hugYWyZmYI2n8qiS7RFrgpKcBtWJZu5L7UbjPMlNvWSlkU6P8TzotiYud3Qc+RW41W15+9UYjc1uI/oxTv8iqsvzfwKOD+LAy07z66M7M47ZFar7L0aYIw==; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; JSESSIONID=1B96A5708445624EB20A41083633DE47',
            'faces-request': 'partial/ajax',
            'origin': 'https://catalog.mann-filter.com',
            'priority': 'u=1, i',
            'referer': 'https://catalog.mann-filter.com/EU/tur/catalog/MANN-FILTER%20Katalog%20Europa/Ya%C4%9F%20filtresi/ZR%20905%20z',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(url=page_url, headers=headers, body=payload, method='POST',
                             callback=self.cross_reference,
                             meta={'link': page_url, 'Filter Type': filter_type, 'GTIN code': gtin_code,
                                   'Shipment Status': shipment_status, 'Product Details': product_details,
                                   'dimensions_data': dimensions_data, 'applications_data': applications_data})

    # @staticmethod
    def cross_reference(self, response):
        page_url = response.meta.get('link')
        filter_type = response.meta.get('Filter Type')
        gtin_code = response.meta.get('GTIN code')
        shipment_status = response.meta.get('Shipment Status')
        product_details = response.meta.get('Product Details')
        dimensions_data = response.meta.get('dimensions_data')
        applications_data = response.meta.get('applications_data')

        text_response = TextResponse(url='', body=response.body, encoding='utf-8')
        cross_references = text_response.css('.advancedList_label .label_lv1::text').getall()
        cross_reference_data = []

        for cross_reference_ in cross_references:
            cross_reference = cross_reference_.strip()
            cross_reference_data.append(cross_reference)

        if not cross_reference_data:
            cross_reference_data = None

        item = dict()
        item['Link'] = page_url
        item['Filter Type'] = filter_type
        item['GTIN Code'] = gtin_code
        item['Shipment Status'] = shipment_status
        item['Product Details'] = product_details
        item['Dimensions_Data'] = dimensions_data
        item['Applications_Data'] = applications_data
        item['Cross_Reference_Data'] = cross_reference_data

        # yield {
        #     'link': page_url,
        #     'Filter Type': filter_type,
        #     'GTIN code': gtin_code,
        #     'Shipment Status': shipment_status,
        #     'Product Details': product_details,
        #     'dimensions_data': dimensions_data,
        #     'applications_data': applications_data,
        #     'cross_reference_data': cross_reference_data
        # }
        yield scrapy.Request(url='https://catalog.mann-filter.com/EU/tur', callback=self.parse,  #headers=self.headers
                             meta={'url':page_url})

    def parse(self, response):
        payload = deepcopy(self.data1)
        # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
        viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()

        payload['javax.faces.ViewState'] = viewstate_value
        url = response.meta['url']
        yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app, #headers=self.headers,
                                 meta={'url':url})

    def parse_app(self, response):
        selector = Selector(text=response.text)
        j_id_loop = selector.xpath("//span[contains(@id,'productDetail:j_idt')]/@id").getall()
        if j_id_loop:
            j_id2 = j_id_loop[-1]
            loop = selector.xpath("//*[contains(@class,'advancedLi li_lv_1')]")
            for index, categories in enumerate(loop):
                cat_name = categories.css('.label_lv1 ::text').get('').strip()

                req_j_id_text = categories.xpath("//span[contains(@id,'productDetail:j_idt')]/@id").get('').strip()
                payload = deepcopy(self.data2)
                # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
                viewstate_value = response.xpath(f'//*[@id="j_id1:javax.faces.ViewState:{index}"]/@value').get()

                payload['javax.faces.ViewState'] = viewstate_value
                payload['name'] = cat_name
                payload['javax.faces.source'] = req_j_id_text
                payload['javax.faces.partial.execute'] = f'{req_j_id_text} @component'
                payload['org.richfaces.ajax.component'] = req_j_id_text
                payload[req_j_id_text] = req_j_id_text

                url = response.meta['url']
                yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app_category, #headers=self.headers,
                                         meta={'url':url,'j_id2':j_id2, 'cookiejar': index})

    def parse_app_category(self, response):
        selector = Selector(text=response.text)
        for index, sub_categories in enumerate(selector.xpath("//*[contains(@class,'label_lv2')]")):
            sub_cat_name = sub_categories.css('::text').get('').strip()

            req_j_id_text = response.meta['j_id2']

            payload = deepcopy(self.data3)
            # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
            viewstate_value = response.xpath(f'//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()
            payload['javax.faces.ViewState'] = viewstate_value
            payload['name'] = sub_cat_name
            payload['javax.faces.source'] = req_j_id_text
            payload['javax.faces.partial.execute'] = f'{req_j_id_text} @component'
            payload['org.richfaces.ajax.component'] = req_j_id_text
            payload[req_j_id_text] = req_j_id_text
            url = response.meta['url']
            yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app_detail, #headers=self.headers,
                                     meta={'url':url,'cookiejar':response.meta['cookiejar']} )

    def parse_app_detail(self, response):
        selector = Selector(text=response.text)
        count = 1
        for Rows in selector.css('.row'):
            item = dict()
            item['Ser'] = count
            count += 1
            item['Vehicle Type'] = Rows.css('.vehicle_type a ::text').get('').strip()
            item['Vehicle Motor'] = Rows.css('.vehicle_motor .tableContent ::text').get('').strip()
            item['Vehicle Hub (ccm)'] = Rows.css('.vehicle_hub .tableContent ::text').get('').strip()
            item['Vehicle kW'] = Rows.css('.vehicle_kw .tableContent ::text').get('').strip()
            item['Vehicle HP (PS)'] = Rows.css('.vehicle_hp .tableContent ::text').get('').strip()
            item['Year of Manufacture'] = (Rows.css('.vehicle_year .tableContent ::text').get('').strip()
                                           .replace('\t','').replace('\n','').replace('→',''))
            yield item

    @staticmethod
    def read_inputs_from_csv():
        return list(csv.DictReader(open('inputs/Kitapp_sample_links.csv', 'r', encoding='utf-8')))

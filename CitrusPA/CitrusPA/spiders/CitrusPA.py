import scrapy
from copy import deepcopy
import datetime
import csv


class CitrusPA(scrapy.Spider):
    name = 'CitrusPA'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '1F7C5CA3',
            '__EVENTVALIDATION': 'RmRzyylF9zGi2sO8RzZHpYVVSbMSrD/a5E2XVl0JbGmCAOajKzYJyXQtXwItYOJgkllxKFGz3AOMFaAug80eACzLIyKi7P9pFrXEGu/AzM6MuDrqQn0H9+3CvdSwSzQw8yGBOhr26yDw5Ed+kzmjNFYPjC4JNrDWrxU20+cWg1sogcy7nuYxK2ynjbC/3rKCXw9OLyY5h5q2HjR6Ls0nd+O0jupOBshMy6cZ1EReInB1u7CTdMchGzXedy1G+DvZnyhjZJmveS76M1sPTeo5Xy89bXumZW2C1dRytJWCmBu7VZYxw4VU3D2Tt7NWwplvi1noFTcshjjtn4Ty+00TdCzzCQXBkP95BqdqsgWY1wzEVDUwLV4aoO6v8U9OkLq69tojoINqKm3P9ousIMRVb6P7rbChMKWg/ROhI+AdioaLKn4p7iRQB8f9EBsZbnNyAYJcslHiZoBdQsF+CYESSQmgaQw8J1HXaUxITKmjk75+vL6c1CtTwprz3EIeip79K6gtq9CIJYivjwXKCNJp6kxkEfPIsrxDOVP8MRWjFKsZFoCcbsFDw7PnKM9NEWo0lyOhW0A4dI2XA8hho3zOUg==',
            # 'hdCriteria': 'alt_id|18E16S330010  00030 0090',
            # 'txtCrit': '18E16S330010  00030 0090',
            'hdCriteria': 'alt_id|',
            'txtCrit': '',
            'PageNum': '',

            'SortBy': 'PARID',
            'SortDir': ' asc',
            'PageSize': '20',
            'hdTaxYear': '',
            'hdAction': '',
            'hdCriteriaLov': '',
            'hdCriteriaTypes': 'C|N|N|N|C|N|C|N|C|C|C|C|C|C|C|C|C|C|C|N|C|D|C|C|D|C|N|N|C|N|C|C|N|C',
            'hdLastState': '1',
            'hdReset': '',
            'hdName': '',
            'hdSelectedQuery': '0',
            'mode': '',
            'hdSearchType': 'AdvSearch',
            'hdListType': '',
            'hdIndex': '',
            'hdSelected': '',
            'hdCriteriaGroup': '',
            'hdCriterias': 'parid|sfla|bathrooms|bedrooms|class|busla|com_stories|com_yrblt|landclass|landclass_multi|Legal|addr1|oby_code|oby_code_multi|nbhd|nbhd_multi|owner|luc|luc_multi|user7|alt_id|permdt|res_class|yrblt|salesdate|instrtyp|salesprice|stories|adrstr|adrno|subdnum|taxdist|areasum|m_zip1',
            'hdSelectAllChecked': 'false',
            'ctl01$dlGroups': '4',
            'sCriteria': '21',
            'inpDistinct': 'on',
            'ctl01$cal1': '',
            'ctl01$cal1$dateInput': '',
            'ctl01_cal1_dateInput_ClientState': '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00","lastSetTextBoxValue":""}',
            'ctl01_cal1_calendar_SD': '[]',
            'ctl01_cal1_calendar_AD': '[[1900,1,1],[2099,12,30],[2024,8,21]]',
            'ctl01_cal1_ClientState': '{"minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00"}',
            'ctl01$cal2': '',
            'ctl01$cal2$dateInput': '',
            'ctl01_cal2_dateInput_ClientState': '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00","lastSetTextBoxValue":""}',
            'ctl01_cal2_calendar_SD': '[]',
            'ctl01_cal2_calendar_AD': '[[1900,1,1],[2099,12,30],[2024,8,21]]',
            'ctl01_cal2_ClientState': '{"minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00"}',
            'txtCrit2': '',
            'txCriterias': '21',
            'inpTaxyr': '2024',
            'selSortBy': 'PARID',
            'selSortDir': ' asc',
            'selPageSize': '50',
            'searchOptions$hdBeta': '',
        }
    custom_settings = {
        'FEED_URI': f'output/Citrus Property Appraiser - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def start_requests(self):
        parcel_ids = []
        with open('input/Parcel IDs.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                parcel_ids.append(row[0])

        for index, parcel_id in enumerate(parcel_ids):
            yield scrapy.Request(
                url='https://www.citruspa.org/_web/Search/Disclaimer.aspx?FromUrl=..%2fsearch%2fadvancedsearch.aspx%3fmode%3dadvanced',
                callback=self.agree_parse, dont_filter=True,
                meta={'parcel_id':parcel_id, 'cookiejar': index},
                )

    def agree_parse(self, response):
        parcel_id = response.meta['parcel_id']
        cookiejar = response.meta['cookiejar']

        data = {
            'btAgree': '',
            'hdURL': '../search/advancedsearch.aspx?mode=advanced',
            'action': '',
            '__VIEWSTATEGENERATOR': response.css('#__VIEWSTATEGENERATOR ::attr(value)').get('').strip(),
            '__EVENTVALIDATION': response.css('#__EVENTVALIDATION ::attr(value)').get('').strip(),
            '__VIEWSTATE': response.css('#__VIEWSTATE ::attr(value)').get('').strip(),
        }
        url = "https://www.citruspa.org/_web/Search/Disclaimer.aspx?FromUrl=..%2fsearch%2fadvancedsearch.aspx%3fmode%3dadvanced"
        # url = "https://www.citruspa.org/_web/search/advancedsearch.aspx?mode=advanced"
        yield scrapy.FormRequest(url=url, formdata=data, method='POST', callback=self.parse_search, headers=self.headers,
                                 meta={'parcel_id': parcel_id, 'cookiejar': cookiejar}, dont_filter=True,
                                 )

    def parse_search(self, response):
        parcel_id = response.meta['parcel_id']
        cookiejar = response.meta['cookiejar']

        payload = deepcopy(self.data)
        payload['__EVENTTARGET'] = response.css('#__EVENTTARGET ::attr(value)').get('').strip()
        payload['__EVENTARGUMENT'] = response.css('#__EVENTARGUMENT ::attr(value)').get('').strip()
        payload['__VIEWSTATE'] = response.css('#__VIEWSTATE ::attr(value)').get('').strip()
        payload['__VIEWSTATEGENERATOR'] = response.css('#__VIEWSTATEGENERATOR ::attr(value)').get('').strip()
        payload['__EVENTVALIDATION'] = response.css('#__EVENTVALIDATION ::attr(value)').get('').strip()
        payload['hdCriteria'] = f'alt_id|{parcel_id}'
        payload['txtCrit'] = parcel_id

        url = "https://www.citruspa.org/_web/search/advancedsearch.aspx?mode=advanced"
        yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse, headers=self.headers,
                                 meta={'parcel_id': parcel_id, 'cookiejar': cookiejar},
                                 dont_filter=True)


    def parse(self, response):
        parcel_id = response.meta['parcel_id']

        item = dict()
        table = response.xpath("//*[contains(@id,'Mailing Address')]")
        item['Parcel ID'] = parcel_id
        item['Name'] = table.xpath(".//td[contains(text(),'Name')]/following-sibling::td[1]/text()").get('').strip()
        item['Address'] = response.css(".DataletHeaderBottom+ .DataletHeaderBottom ::text").get('').strip()
        mailing_add1 = table.xpath(".//td[contains(text(),'Mailing Address')]/following-sibling::td[1]/text()").get('').strip()
        mailing_add2 = table.xpath(".//td[contains(text(),'Mailing Address')]/parent::tr[1]/following-sibling::tr[1]//td[2]/text()").get('').strip()
        item['Mailing Address'] = f'{mailing_add1}, {mailing_add2}'

        yield item

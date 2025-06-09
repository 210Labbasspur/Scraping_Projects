import csv
import json

import scrapy


class CourtsScraperSpider(scrapy.Spider):
    name = "courts_scraper" # this is the spider name
    base_url = "https://www.courts.mo.gov/cnet/caseNoSearch.do"
    parties_url = "https://www.courts.mo.gov/cnet/cases/party.do?caseNumber={case_no}&courtId=CT21&isTicket="
    custom_settings = {
        'FEED_URI': ' Courts_Records.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_FIELDS': ['Case Number','Filing Date',
                               'Style of Case', 'Case Type', 'Disposition', 'Decedent Name','Decedent Year Of Birth',
                               'Decedent Date Of Death',
                               'Decedent Address', 'Decedent City', 'Decedent State', 'Decedent Zip', 'Petitioner Name',
                               'Petitioner Year Of Birth', 'Petitioner Address', 'Petitioner City', 'Petitioner State', 'Petitioner Zip',
                               'Attorney for Petitioner','Heir1 Name',
                               'Heir1 Year Of Birth','Heir1 Address', 'Heir1 City', 'Heir1 State', 'Heir1 Zip',
                               'Heir2 Name','Heir2 Year Of Birth','Heir2 Address', 'Heir2 City', 'Heir2 State',
                               'Heir2 Zip', 'Heir3 Name','Heir3 Year Of Birth',
                               'Heir3 Address', 'Heir3 City', 'Heir3 State', 'Heir3 Zip', 'Heir4 Name','Heir4 Year Of Birth'
                               'Heir4 Address',
                               'Heir4 City', 'Heir4 State', 'Heir4 Zip']
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'JSESSIONID=0001zwDDM_caxzfzvTT-xZQ4ixX:2PA9SVSUFE; UJID=6079a09c-46ff-4089-8062-8e43b90ea2e4; UJIA=-797709050; _ga_DSVJ8DTRVZ=GS1.1.1692446421.1.0.1692446421.0.0.0; _ga=GA1.2.1661513730.1692446421; _gid=GA1.2.397922331.1692446424; UJIA=-797709050; UJID=6079a09c-46ff-4089-8062-8e43b90ea2e4',
        'Origin': 'https://www.courts.mo.gov',
        'Referer': 'https://www.courts.mo.gov/cnet/caseNoSearch.do',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        file_data = self.get_data()
        for data in file_data:
            yield scrapy.Request(url=self.parties_url.format(case_no=data['Case Number']),
                                 headers=self.headers,callback=self.parse)

    def parse(self, response,**kwargs):
        result_data = json.loads(response.text)
        item = {
            'Case Number': result_data.get('caseNumber',''),
            'Filing Date': result_data.get('filingDate',''),
            'Case Type': result_data.get('caseType',''),
            'Disposition': result_data.get('caseDispositionDetail',{}).get('dispositionDescription',''),
        }
        item.update(self.get_parties(result_data.get('partyDetailsList',[])))
        yield item

    def get_parties(self,data):
        count = 1
        data_dict = {}
        for info in data:
            desc = info.get('desc','')
            if desc == 'Decedent':
                data_dict['Style of Case'] = info.get('formattedPartyName','')
                data_dict['Decedent Name'] = info.get('formattedPartyName','')
                data_dict['Decedent Address'] = info.get('addrLine1','')
                data_dict['Decedent City'] = info.get('addrCity','')
                data_dict['Decedent State'] = info.get('addrStatCode','')
                data_dict['Decedent Zip'] = info.get('addrZip','')
                data_dict['Decedent Year Of Birth'] = info.get('formattedBirthDate','')
                data_dict['Decedent Date Of Death'] = info.get('formattedDeathDate','')
            if desc == 'Petitioner' or desc =='Applicant' or 'Personal Representative' in desc:
                data_dict['Petitioner Name'] = info.get('formattedPartyName','')
                data_dict['Petitioner Year Of Birth'] = info.get('formattedBirthDate','')
                data_dict['Petitioner Address'] = info.get('addrLine1', '')
                data_dict['Petitioner City'] = info.get('addrCity', '')
                data_dict['Petitioner State'] = info.get('addrStatCode', '')
                data_dict['Petitioner Zip'] = info.get('addrZip', '')
                attorney = info.get('attorneyList',[])
                if attorney:
                    attorney_info = attorney[0]
                    data_dict['Attorney for Petitioner'] = attorney_info.get('formattedPartyName','')
            if desc == 'Heir':
                data_dict[f'Heir{count} Name'] = info.get('formattedPartyName','')
                data_dict[f'Heir{count} Year Of Birth'] = info.get('formattedBirthDate','')
                data_dict[f'Heir{count} Address'] = info.get('addrLine1', '')
                data_dict[f'Heir{count} City'] = info.get('addrCity', '')
                data_dict[f'Heir{count} State'] = info.get('addrStatCode', '')
                data_dict[f'Heir{count} Zip'] = info.get('addrZip', '')
                count += 1
        return data_dict

    def get_data(self):
        with open('Input_file.csv','r',encoding='utf-8') as file:
            return list(csv.DictReader(file))


import scrapy
import json
import re
class DentalCorp(scrapy.Spider):
    name = 'DentalCorp'
    url = "https://dentalcorp.wd3.myworkdayjobs.com/wday/cxs/dentalcorp/dentalcorp/jobs"
    custom_settings = {
        'FEED_URI': 'DentalCorp.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    
    payload = json.dumps({
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": "Dentist"
    })
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'PLAY_SESSION=c1e868186206c7f8279d90d30e7a12f7a6a424fc-dentalcorp_pSessionId=bhcmfpg971v88peeqi9un7cmvs&instance=wd3prvps0001c; wday_vps_cookie=2602997258.58930.0000; timezoneOffset=-300; _ga=GA1.4.1974556363.1694605804; TS014c1515=01f6296304cc8458c405e38addfdf00db2e4cba316d77c0ff3cff97ba9f8d6ae0ae38bdce9380b443ed66b3acac368611524ff8d04; wd-browser-id=26b97077-de9e-4de9-9a79-ee297408edcb; CALYPSO_CSRF_TOKEN=9e18ff3c-ab51-41b8-a384-5cf50f9021e9; _ga_JZRRQMYMGN=GS1.4.1694605804.1.1.1694606718.0.0.0; PLAY_SESSION=c1e868186206c7f8279d90d30e7a12f7a6a424fc-dentalcorp_pSessionId=bhcmfpg971v88peeqi9un7cmvs&instance=wd3prvps0001c; TS014c1515=01f62963040e2740fb3785a1bc38bb96b285a40de17bb09a3c56bc254eb5ea030468f04da41671c3a1b68b4e9652d5227b646aaa42',
        'Origin': 'https://dentalcorp.wd3.myworkdayjobs.com',
        'Referer': 'https://dentalcorp.wd3.myworkdayjobs.com/en-US/dentalcorp/jobs?q=Dentist',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': '6b07599a-f8fd-46c6-b6d4-88e6a490c9c0',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    Ser = 0
    Total = 0
    prefix = "https://dentalcorp.wd3.myworkdayjobs.com/en-US/dentalcorp"
    api_url_prefix = 'https://dentalcorp.wd3.myworkdayjobs.com/wday/cxs/dentalcorp/dentalcorp'
    api_headers = {
      'Accept': 'application/json',
      'Accept-Language': 'en-US',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded',
      # 'Cookie': '_ga=GA1.4.1974556363.1694605804; PLAY_SESSION=28f8123c2e82c1c955c0fabfaa7bfc1eb8bad77b-dentalcorp_pSessionId=4a2dlk40denmnpk7t10v7derk4&instance=wd3prvps0007f; wday_vps_cookie=2166789642.1075.0000; timezoneOffset=-300; TS014c1515=01f6296304f633d85a108bc079d55d153cbfad42e5ca75fa3644304efe3ea2bf2bbd35fc4fae4963eef44c568eca77ff0bd8151120; wd-browser-id=fef0cd39-5018-44e4-a486-d5d9119dfba0; CALYPSO_CSRF_TOKEN=4a5dd60e-9b06-4d80-97f5-d782f7a480ce; _ga_JZRRQMYMGN=GS1.4.1694624464.3.0.1694625133.0.0.0; PLAY_SESSION=28f8123c2e82c1c955c0fabfaa7bfc1eb8bad77b-dentalcorp_pSessionId=4a2dlk40denmnpk7t10v7derk4&instance=wd3prvps0007f; TS014c1515=01f6296304091ca04c0916859c70b352b6898d522556338fbe71039bc09828ac5a4ebd3da0911a9310d0fa7d8a2545462072e03401',
      'Referer': 'https://dentalcorp.wd3.myworkdayjobs.com/en-US/dentalcorp/job/Dentistry-at-8-Nelson/Associate-Dentist---Dentistry-at-8-Nelson_JR6372-1?q=Dentist',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
      'X-CALYPSO-CSRF-TOKEN': '4a5dd60e-9b06-4d80-97f5-d782f7a480ce',
      'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, method="POST", body=self.payload, headers=self.headers,
                         callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        if data['total'] > 0:
            self.Total = data['total']
        for result in data['jobPostings']:
            self.Ser += 1
            item = dict()
            item['Ser'] = self.Ser
            # item['Title'] = result.get('title').strip()
            detail_url = self.api_url_prefix + result.get('externalPath').strip()
            yield response.follow(url=detail_url, callback=self.detail_page, headers=self.api_headers, meta={'item':item})

        if self.Ser < self.Total:      #   NEXT PAGE
            new_payload = json.loads(self.payload)
            new_payload["offset"] = self.Ser
            yield scrapy.Request(url=self.url, method="POST", body=str(new_payload), headers=self.headers,
                                 callback=self.parse)

    def detail_page(self, response):
        data = json.loads(response.body)
        job_data = data['jobPostingInfo']
        if job_data:
            item = response.meta['item']
            item['Job Title'] = job_data.get('title').strip()
            item['Location'] = job_data.get('location').strip()
            item['Country'] = job_data.get('country').get('descriptor').strip()
            item['Job Time type'] = job_data.get('timeType').strip()
            item['Start Date'] = job_data.get('startDate').strip()
            item['Job Req ID'] = job_data.get('jobReqId').strip()
            job_desc = job_data.get('jobDescription').strip()
            clean = re.compile('<.*?>')
            job_description = re.sub(clean, '', job_desc)
            item['Job Description'] = job_description.replace("\xa0",' ')

            yield item

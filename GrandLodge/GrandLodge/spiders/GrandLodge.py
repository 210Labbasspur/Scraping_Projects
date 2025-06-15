import csv
import scrapy
import re
class GrandLodges(scrapy.Spider):
    name = "GrandLodges"
    url = "https://lodges.glflamason.org/public/Lodge-Search"
    payload = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=FanWfu%2BMTJsjplG5f7UPB2srjelohFcxAUmjXXSCgvKY83TXut9la4WA5uikdfQw1V3iWxhRKm766QHIudf6EE%2F381HtHB1MtYF6ETEMcUJED1LjYOxeFgoAGEWST7FhxfZ8ofgEOL5h9UoROJ4d7vFqrYQEDdGl23nhKlHd47N6B3hMMOZAw1wDwbz09U0l%2F8kJGGP7iYH%2BDxks7j5WHTIFyzJyxfxX44pPyDCtuXsiRCOYc%2FsrHkYWhX%2BDvTO%2FbMpqgr2yDp2G984xM7Tl9Kut6sdqZhN7W3lg0xRJ83gH969mMRmz71voTt4pqaY9C3drVOnq3MHevC7eLGyWk9sby6egrrK7Txu7ZyOof5NtvyKuhF' \
              '6DEGopwx4XRlgRufSarZgjL9H9KmmgpKrlfjRGXVHnpf3L0qmMSv7nCpx0sLH2hr4ev4GMLSSZo7qMl791Mty8Sbr3cpMGb90WXyNPF5bVYBREmV4wd2xigEn7Jb' \
              '%2Bxs4em2r8Cv%2Ffn7UEZoeCKzpkf2dMFvCanRND2ncx8k6Ywtt297wSvo%2FhUj%2FOBUYqno1SGK2qMIZW3K721qCQbOMs%2BXLzIX4ONTQNls2LXEhdTLLXsOR1r3Kf8qIsi8VhDDHzWQqDNWZu7FEQDcr5nnjnBYzGg1Sm7H%2FHI3LZanyTHteewFa0lu3B%2FgbEqTNknJgtAkhnDjj9e' \
              'KsUTRYp9b%2F1v92wqDisOxC%2FbaoplS92iAyr%2Bbxf4FzrwyfaBpzecaYJ8T7Q8FrZU86yWC6WP2%2B9sxnhzUWLKCtda6wcHf3eaGV0YlG1nScb1kidkN3jG4ikHVtA%2FrOKlscSsECsHzjkec8JM2vFl7kU%2BOiSJIqD3%2FtJSC1vLIldK8CDIQIkLbP0J80IY8TGJLbMEis3UPJWosuPniOyzlYUcSCuY6teHGh6P7ntle77TpUUCSOkJdv0zCbm9d%2F1KNWmt57EnvVAdPWnODN3W5xwMFTfy' \
              '%2B431gkmEtjboSLXHuIiZesx%2BhIRuqQ6qDuQGjGOrDkYebaCJGDP6KXoAj5FaqxYZsHcE%2BQriGJ8O7txubssOtgDbH%2BaK0%2F5YFaIzm5pWOWXJ' \
              'Utt5iYbRsgSBoSraXrTYuAWTxIQCYmCPismu0H%2F0FiAtnWDn%2Bg3xGCp9PJZ8PYn9AtN01blaDxXAEUv1bmsoE30uemDdkibMotoEKborByg%2B&__VIEWSTATEGENERATOR=28F5BA94&__EVENTVALIDATION=WNjcU0gAjIxXMfSHyY90qua77sPDraqgKUIXt7P3fOFihfQzuQ3%2FszhT555fGN91ALHIIAU' \
              'ZSMt76b6JIzb34g5OFfXVSm3jF08HDsIBPpIgJR32KZfJvN5j84YiPhu0Dpb2Lp0A7Uf6vgqvW4erWMxAH1BmdK3ivLL19vM9g3rvfSITp02LL8AMaxRZ9IPtv4KEu2oERacVBKjqAMXMxS3pSgNgX9wnZ5br4MzyjuA3WDam6bXp%2FoLUtseWFSgmfD7OThuiSp0el%2FW0RxCd%2B2e71v5ueKXdB2Af6DINyWX4KzpMo8aKkg%2F1fs3WEPp43B3as%2FmQUZZ%2FXJVJAnRLATrKtsYuX%2FDaowpEl5z42ooVVINbnKJMu1AYO%2FpymqtsDqppx1GtbAmqp1pe7Kx0FeIbuN4FcviemXQ7Pniit%2BHH8TszCl402vWllKjtTLPCUH%2BK2wi%2Far1oQfQEwKWJAKHEg5nOXP7Shdf6tiCi4muembIYPJEA1c13GJV7J6k529%2BisvekZDGKnjOmmkB46Gp3PlYLzM6MgQVk33sZ%2FrYehNKlEzvjNW93cFnlDpTftSzSiyUaVzuyk5eJE2HOVxQGt57iM4p7ACbRaAarxyFVtdqq8%2FC1%2BQOEkVNd4Rbvkcb2OGiRrO3Upyzq&ctl00%24ContentPlaceHolder1%24HiddenFieldLatitude=&ctl00%24ContentPlaceHolder1%24HiddenFieldLongitude=&ctl00%24ContentPlaceHolder1%24MyAccordion_AccordionExtender_ClientState=3&ctl00%24ContentPlaceHolder1%24_content%24TextBoxSearchAddress=&ctl00%24ContentPlaceHolder1%24_content%24TBWE2_ClientState=&ctl00%24ContentPlaceHolder1%24AccordionPane1_content%24TextBoxSearchCity=&ctl00%24ContentPlaceHolder1%24AccordionPane1_content%24TextBoxWatermarkExtender1_ClientState=&ctl00%24ContentPlaceHolder1%24AccordionPane2_content%24TextBoxSearchLodgeNumber=&ctl00%24ContentPlaceHolder1%24AccordionPane2_content%24TextBoxWatermarkExtender2_ClientState=&ctl00%24ContentPlaceHolder1%24AccordionPane3_content%24' \
              'TextBoxSearchZip={zip_code}' \
              '&ctl00%24ContentPlaceHolder1%24AccordionPane3_content%24TextBoxWatermarkExtender3_ClientState=&ctl00' \
              '%24ContentPlaceHolder1%24AccordionPane3_content%24ButtonSearchZip=Search&ctl00%24ContentPlaceHolder1%24AccordionPane5_content%24TextBoxSearchDistrict=&ctl00%24ContentPlaceHolder1%24AccordionPane5_content%24TextBoxWatermarkExtender4_ClientState=&ctl00%24ContentPlaceHolder1%24AccordionPane6_content%24TextBoxSearchCounty=&ctl00%24ContentPlaceHolder1%24AccordionPane6_content%24TextBoxWatermarkExtender5_ClientState=&ctl00%24ContentPlaceHolder1%24AccordionPane4_content%24TextBoxSearchName=&ctl00%24ContentPlaceHolder1%24AccordionPane4_content%24TextBoxWatermarkExtender6_ClientState='
    headers = {
        'authority': 'lodges.glflamason.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'ASP.NET_SessionId=oaxfi5gcu5w3r2ivghq4255x',
        'origin': 'https://lodges.glflamason.org',
        'referer': 'https://lodges.glflamason.org/public/Lodge-Search',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    prefix = 'https://lodges.glflamason.org'

    custom_settings = {
        'FEED_URI': 'Updated GrandLodge.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_code = self.get_search_code()

    def get_search_code(self):
        with open('Florida_ZipCodes.csv', 'r', encoding='utf-8-sig') as reader:
            return list(csv.DictReader(reader))

    def start_requests(self):
        for check in self.request_code:
            zipcode = check['zip']
            yield scrapy.Request(url=self.url, method="POST", headers=self.headers, body=self.payload.format(zip_code=zipcode),
                                     callback=self.parse)

    def parse(self, response):
        item = dict()
        for names in response.css('#ctl00_ContentPlaceHolder1_GridViewResults_ctl02_HyperLinkLodge'):
            item['Name'] = names.css(' ::text').get('').strip()
            item['Address'] = response.css('#ctl00_ContentPlaceHolder1_GridViewResults td:nth-child(3) ::text').get('').strip()
            item['City'] = response.css('#ctl00_ContentPlaceHolder1_GridViewResults td:nth-child(4) ::text').get('').strip()
            item['State'] = response.css('#ctl00_ContentPlaceHolder1_GridViewResults td:nth-child(5) ::text').get('').strip()
            item['Zip'] = response.css('#ctl00_ContentPlaceHolder1_GridViewResults td:nth-child(6) ::text').get('').strip()

            post_url = response.css('#ctl00_ContentPlaceHolder1_GridViewResults_ctl02_HyperLinkLodge ::attr(href)').get('').strip()
            Url = self.prefix + post_url.replace('..','')

            yield response.follow(url=Url, callback=self.detail_page, headers=self.headers, meta={'item': item})


    def detail_page(self, response):
        item = response.meta['item']
        Lodge_Data = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelInfo1')]/text()").getall()
        item['Lodge Number'] = (Lodge_Data[0].replace('Lodge Number:','')).strip()
        item['District Number'] = (Lodge_Data[1].replace('District Number:','')).strip()
        item['Zone'] = (Lodge_Data[2].replace('Zone:','')).strip()
        item['Lodge County'] = (Lodge_Data[3].replace('Lodge County:','')).strip()
        item['Lodge Chartered on'] = (Lodge_Data[4].replace('Lodge Chartered On:','')).strip()
        item['Lodge Street Address'] = (Lodge_Data[5].replace('Lodge Street Address:','')).strip() +', '+ Lodge_Data[6].strip()
        item['Lodge Mailing Address'] = (Lodge_Data[7].replace('Lodge Mailing Address:','')).strip() +', '+ Lodge_Data[8].strip()

        email = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_HyperLinkEmailLodge')]/@href").get('').strip()
        email_pattern = r'mailto:([A-Za-z0-9_.]+@[A-Za-z0-9]+\.[A-Za-z]+)'
        match = re.search(email_pattern, email)
        if match:
            item['Email'] = match.group(1)

        Phone_No = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelInfo2')]/text()").get('').strip()
        item['Phone No'] = (Phone_No.replace('Lodge Phone Number:','')).strip()
        item['Lodge Driving Directions'] = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_HyperLinkDrivingDirections')]/@href").get('').strip()
        Lodge_Meeting = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelInfo3')]/text()").getall()
        item['Lodge Meetings'] = (Lodge_Meeting[0].replace('Lodge Meetings:','')).strip()
        item['Meeting Time'] = (Lodge_Meeting[1].replace('Meeting Time:','')).strip()

        # # Lodge Member Statistics
        Lodge_Stats = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelStats')]/text()").getall()
        item['Total Lodge Members'] = (Lodge_Stats[0].replace('Total members:','')).strip()
        item['Oldest Lodge Member'] = (Lodge_Stats[1].replace('Oldest member:','')).strip()
        item['Youngest Lodge Member'] = (Lodge_Stats[2].replace('Youngest member:','')).strip()
        item['Longest Good Time Member'] = (Lodge_Stats[3].replace('Longest good time member:','')).strip()
        item['Average Age of Members'] = (Lodge_Stats[4].replace('Average age of members:','')).strip()

        # # District Deputy Grand Master
        District_Deputy_Grand_Master = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelDDGM')]/text()").getall()
        item['District Deputy Name'] = (District_Deputy_Grand_Master[0]).strip()
        if District_Deputy_Grand_Master[1]:
            item['District Deputy Phone No'] = (District_Deputy_Grand_Master[1].replace('Phone.','')).strip()
        item['District Deputy Email'] = (response.css('#ctl00_ContentPlaceHolder1_LabelDDGM a::attr(href)').get('').replace('mailto:','')).strip()

        # # DI - District Instructor
        DI = response.xpath("//*[contains(@id,'ctl00_ContentPlaceHolder1_LabelDI')]/text()").getall()
        item['DI Name'] = (DI[0]).strip()
        if DI[1]:
            item['DI Phone No'] = (DI[1].replace('Phone.','')).strip()
        item['DI Email'] = (response.css('#ctl00_ContentPlaceHolder1_LabelDI a::attr(href)').get('').replace('mailto:','')).strip()

        # # Lodge Officers
        Lodge_Officers_Table = response.css('#ctl00_ContentPlaceHolder1_GridViewOfficers tr')
        for entry in Lodge_Officers_Table[1:]:
            row = entry.css('::text').getall()
            item['Officer Title']= row[1].strip()
            item['Officer First Name']= row[2].strip()
            item['Officer Last Name']= row[3].strip()
            item['Officer Phone No']= row[4].strip()
            item['Officer Email']= (entry.css('.pr5 a::attr(href)').get('').strip()).replace('mailto:','')

            yield item

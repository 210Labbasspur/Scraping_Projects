import scrapy
import datetime
from copy import deepcopy

class ArriveStreeterVille(scrapy.Spider):
    name = 'arrivestreeterville'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://arrivestreeterville.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://arrivestreeterville.com/floorplans/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'action': 'popup_fp',
        'id': '687901',
        'unit_cap': '5',
        'move_in_date': '',
    }

    custom_settings = {
        'FEED_URI': f'output/Arrive Streeterville Floorplans - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def start_requests(self):
        url = 'https://arrivestreeterville.com/floorplans/'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        count = 1
        for appartment in response.css("#floorplan_sorting_front_List tr"):
            availability = appartment.xpath(".//*[contains(@class,'btn btn-primary view-fp-details')]/@onclick").get('').strip()
            id_start = availability.find("'") + 1
            id_end = availability.find("'", id_start)
            availability_id = availability[id_start:id_end]
            print(count, availability_id)
            count += 1
            bed_bath = appartment.css('td:nth-child(3) ::text').get('').strip()

            cookies_header = "; ".join(
                f"{c.decode().split('=', 1)[0]}={c.decode().split('=', 1)[1].split(';')[0]}"
                for c in response.headers.getlist('Set-Cookie'))
            headers = self.headers
            headers['Cookie'] = cookies_header

            payload = deepcopy(self.data)
            payload['id'] = str(availability_id)
            url = 'https://arrivestreeterville.com/wp-admin/admin-ajax.php'
            yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.detail_parse, headers=headers,
                                     meta={'bed_bath':bed_bath})


    def detail_parse(self, response):
        bed_bath = response.meta['bed_bath']
        bed, bath = (int(x) if x.isdigit() else 0 for x in bed_bath.split(" / "))
        unit_size = response.css("h2 ::text").get('').strip()
        for appartment in response.xpath("//*[contains(@class,'table table-bordered')]/tbody/tr"):
            item = dict()
            item['Building Name'] = 'Arrive Streeterville'
            item['Unit size'] = unit_size
            item['Unit #'] = appartment.css("td:nth-child(3) ::text").get('').strip()
            item['Beds'] = bed
            item['Bath'] = bath
            item['Sq. Ft.'] = appartment.css("td:nth-child(5) ::text").get('').strip()
            if appartment.css("td:nth-child(1) ::text").get('').strip():
                item['Available Date'] = appartment.css("td:nth-child(1) ::text").get('').strip()
            else:
                item['Available Date'] = appartment.css("td:nth-child(1) strong ::text").get('').strip()
            item['12 month Price'] = appartment.css("td:nth-child(4) ::text").get('').strip()
            item['Best Value Price and term'] = ''

            yield item

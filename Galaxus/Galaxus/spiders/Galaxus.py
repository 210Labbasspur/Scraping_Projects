##############      Galaxus

import json
import scrapy
from copy import deepcopy
from unidecode import unidecode

class Galaxus(scrapy.Spider):
    name = 'Galaxus'
    prefix = 'https://www.galaxus.ch'
    # url = 'https://www.galaxus.de/api/graphql/get-sector-products'

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/json',
        'cookie': '.xpid=43d8df8d; .themeshade=light; .cid=215a4f5b-4f9e-45c0-b521-4238fa92c47f; .bid=d610d92a-1741-4a0c-af83-da2211b3cf9d; sp=28c98c39-37f4-44a3-9e59-33f0770052d8; _ga=GA1.1.602646983.1718128890; FPAU=1.2.1469678469.1718128891; _biAN=63023; _biBI=f1404d0c-f8ff-41eb-b574-da8a9223a802; _pin_unauth=dWlkPVlUa3pNemhqTldJdFptSmhZeTAwTUdZd0xXRmxOR1l0TWpZeVptRmlNakkwT0RSaw; _gcl_au=1.1.942243513.1718436961; RecentlyVisitedProducts_=13037848,13347993,11053597,6603160,10260321,16225077,37277415,17247780,9699914,7856927,20816978,6349412,20817030,5640354,21288238,37749048,19937698,13092275,5636771,20850866,20961105,32670365,22756326,21521731; _abck=AD15E4631FF12E12801DD6449636C9C8~-1~YAAQFE5DF9o4nwqQAQAAg4XYIgyW80V+pSUvpHl7Qv89DUAcqRGQVI4sft3b4XEil+9uB/GyJvfzctrpDAhaF0cpVMkOLDkITjJLRtswklRs/OYZJw9p4Teh30va49Q8D9kV36jp0gGio42F0ay1+Wkcs78bN43ORVLgZXmQBXaSryYOv/HoZES2UU5fjEYVBH/+Ha9QIFyrD+Sm9qXnZoYbv3tzidGGB6r1fPcms6ZdYzze7Hl/1VUtlyaQYLI+EFtWZKDmH30jej3ouP3YwS8crsIUNSM+1qT3dwSMos4fp0ISb+0uWPyn/+lcsi5D5agMBaLJOwvkCISFwprU8+m1eFm7kHmkFhZ3Qf5thqwd+ZbbhgiAVL3Mxboex/yYHwSDPaD+K/CFTw==~-1~-1~-1; ak_bmsc=AE721CE12F7E97CFFCBC1B26EDC9B1C7~000000000000000000000000000000~YAAQFE5DF9s4nwqQAQAAg4XYIhhfzSFtqO09mMIkRrIj3YtWsx/FBSbh3HmLl4PbCCqGGbM4L4WW6p6W5ZJ6/c6AS3hEtqdne3NEkGvHpFyJcMInECOp23ZFglL0XAVV0UBMySTDDAiBqMRZsrxxuovDeFvMhuVvyGM62OX5GvnPRDIQZYqEO2V4Jo68Z6JhUWgs/pIDNl540Tu4PdQk0kK9T9+5i08gBDGNmxW4fVTdWSdjniFE2m8A3/YIz/XQ0f5+DtA77FChcM2OXvwUj6iuwPMsD0WsoIX1wuJ6tVHGLHaeOt449cIkpGJrTrDf4ZyYpx96wLCFJ5eDG36P9t+q8oCs5YaOaPz53hLp4a99csgoKLKHBiMdWzvSVqORFaM7NcKEn/nQPw==; .ub.ses.0fce=*; .sid=f1121c95-252e-42ca-a21d-59287e897c40; .sidexp=1718578743; .bidexp=2034104343; bm_mi=F90FF489E7DF9034D8DB45CD75ED0C05~YAAQFE5DFzs8nwqQAQAA4bHYIhjL+fgokVw1/RMBDCBM1tMgb4PmcI4ros0v6OX1mA6jd8kTPf95f2f9h0srOpLL0GM0mGJU8iE+XdWmv0xbjWrG6dkW62RHNn0G7p2a26+tbYWIRB89ENGgt3JGoRRVaF6tsVlbos6avKtooXR66hSgv+7+ILqmfhV0HtBhiYg9zySPWpFMMHEr8NXGPN7HzUIyiZpHAGuG2G2sTuTUau8a2enpfojxIYE5GOZbcbpwwIq2jE0RK9q09+iZIhS8c67ll5e3qh8h56276ZqLphNBGzivIUv5U2uPHQi2~1; bm_sz=7A96682C2CA40E2D17450C840C14C5F2~YAAQFE5DFz08nwqQAQAA4rHYIhhL5tSl5leELCRMhI7HasFHVLnLQs8ZD2UGrzFhlnc4W6IQwtq/nwZXjooXuzzWoOyu4lFYHubgq9+l68dIHt4Ogxo3KTx1K/IDY+LW7KUelpdr6CZr5UrCqFGBhPGiP4CGIHIWjKH4GlB6e78IGLYRVEY6Gl+Uy2Yxu2Vxc8hWEgxJIVkitUDd9yEiw4dDr3LcWdH5jTRkoaQuW8zDaa9K4BBkbFE0qABlqmInO+ewWlozz23t/NtfrTW6VijdimPn0fdZ4Hlhq5+3NbJCx3U0oPRwywHEKRJJQiFftUETBSqETXq42b7EaAonD5hr9D7T7piET9MJKwAZL7NNbxUzcvS6z4OixIdXpeNk+0+N4EwcndQCqgF3R4ANup72~4338245~4408645; RedirectCountry=off; FPGSID=1.1718571555.1718571555.G-ZV404JM7L8.BSU1ZzgBdULW10_L1u0iug; _ga_ZV404JM7L8=GS1.1.1718571549.9.1.1718571555.0.0.2071139968; _uetsid=e07503802ae611ef80a70995e93cda69; _uetvid=a39e2110281c11efa6d3d1206e0c310c; _derived_epik=dj0yJnU9YUhWX0cyWHZXSGtxaWh3ejRKQ3YzZjB0amtrRk80STImbj1WMkJZbjhDdFJNV2NzbHVkdnhabDZnJm09MSZ0PUFBQUFBR1p2VWk0JnJtPTEmcnQ9QUFBQUFHWnZVaTQmc3A9Mg; bm_sv=F185C2FEA1A5DA09F888B40C3795A5FC~YAAQSKfLF+y8T/OPAQAAPk7ZIhi2xdH1YFUHyhaw8nCtrWbyNppyjk+1jMe3bko5/+Q0sPck6Wb1ec7BsxnuOsctQj0oI6aMd8TUH9SNe1H20qeC5on7FV0AeBuyhtRbK0EcU9OPuuB4w+3zN65QB7j/FXIhI/GtxEMuoEjQNkE697t6DxWISPrlzR9Xx4gyNooJNfcsGDW3Lf+Ef1+ZuvL9S38dILA0MGyZbxiF/qKBn9TxPRcXL1vkiN+u/asiXw==~1; .ub.id.0fce=56b173a6-2035-4e57-b4e5-350313680fb5.1718128880.8.1718571584.1718487471.4c7a39f3-cac3-4905-9c80-cfea1108cdd8.ccb21279-c601-4ea2-990e-a3d9c7ada81e.477c9d48-0ecd-4802-9ef7-d6442fbe97d8.1718571542773.13; arp_scroll_position=0; _dd_s=logs=0&expire=1718572483601',
        'origin': 'https://www.galaxus.ch',
        'priority': 'u=1, i',
        'referer': 'https://www.galaxus.ch/en/s6/sector/health-beauty-6',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"125.0.6422.142"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="125.0.6422.142", "Chromium";v="125.0.6422.142", "Not.A/Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-dg-correlation-id': 'b919ebf3-7035-4a3e-a3d6-89247f26cc8f',
        'x-dg-language': 'en-US',
        'x-dg-portal': '22',
        'x-dg-routename': '/sector/[titleAndSectorId]',
        'x-dg-scrumteam': 'StellaPolaris',
    }

    json_data_p = [
        {
            'operationName': 'GET_SECTOR_PRODUCTS',
            'variables': {
                'sectorId': 6,
                'offset': 0,
                'limit': 204,
                'sort': 'BESTSELLER',
            },
            'query': 'query GET_SECTOR_PRODUCTS($sectorId: Int!, $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {\n  sector(id: $sectorId) {\n    products(offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {\n      total\n      hasMore\n      resultsWithDefaultOffer {\n        id\n        ...ProductWithOffer\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductWithOffer on ProductWithOffer {\n  mandatorSpecificData {\n    ...ProductMandatorSpecific\n    __typename\n  }\n  product {\n    ...ProductMandatorIndependent\n    __typename\n  }\n  offer {\n    ...ProductOffer\n    __typename\n  }\n  isDefaultOffer\n  __typename\n}\n\nfragment ProductMandatorSpecific on MandatorSpecificData {\n  isBestseller\n  isDeleted\n  sectorIds\n  hasVariants\n  showrooms {\n    siteId\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMandatorIndependent on ProductV2 {\n  id\n  productId\n  name\n  nameProperties\n  productTypeId\n  productTypeName\n  brandId\n  brandName\n  averageRating\n  totalRatings\n  totalQuestions\n  isProductSet\n  images {\n    url\n    height\n    width\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImage {\n      url\n      height\n      width\n      __typename\n    }\n    __typename\n  }\n  seo {\n    seoProductTypeName\n    seoNameProperties\n    productGroups {\n      productGroup1\n      productGroup2\n      productGroup3\n      productGroup4\n      __typename\n    }\n    gtin\n    __typename\n  }\n  basePrice {\n    priceFactor\n    value\n    __typename\n  }\n  productDataSheet {\n    name\n    languages\n    url\n    size\n    __typename\n  }\n  __typename\n}\n\nfragment ProductOffer on OfferV2 {\n  id\n  productId\n  offerId\n  shopOfferId\n  price {\n    amountInclusive\n    amountExclusive\n    currency\n    __typename\n  }\n  deliveryOptions {\n    mail {\n      classification\n      futureReleaseDate\n      __typename\n    }\n    pickup {\n      siteId\n      classification\n      futureReleaseDate\n      __typename\n    }\n    detailsProvider {\n      productId\n      offerId\n      refurbishedId\n      resaleId\n      __typename\n    }\n    __typename\n  }\n  label\n  labelType\n  type\n  volumeDiscountPrices {\n    minAmount\n    price {\n      amountInclusive\n      amountExclusive\n      currency\n      __typename\n    }\n    isDefault\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isEndingSoon\n    validFrom\n    __typename\n  }\n  incentiveText\n  isIncentiveCashback\n  isNew\n  isSalesPromotion\n  hideInProductDiscovery\n  canAddToBasket\n  hidePrice\n  insteadOfPrice {\n    type\n    price {\n      amountInclusive\n      amountExclusive\n      currency\n      __typename\n    }\n    __typename\n  }\n  minOrderQuantity\n  __typename\n}',
        },
    ]

    custom_settings = {
        'FEED_URI': 'output/Galaxus Record (Health & Beauty) - Ver 3.xlsx',
        # 'FEED_URI': 'output/Galaxus Record (Sports).xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8'}

    count = 1
    def start_requests(self):
        b_url = 'https://www.galaxus.ch/api/graphql/get-sector-products'
        payload = deepcopy(self.json_data_p)
        offset = 5900
        payload[0]['variables']['offset'] = offset
        # print('Payload is :', payload)
        yield scrapy.Request(url=b_url, body=json.dumps(payload), method='POST', callback=self.parse, headers=self.headers,
                             meta={'offset':offset})


    def parse(self, response):
        offset = response.meta['offset']
        data = json.loads(response.text)
        # print(data)
        if data[0]['data']['sector']['products']['resultsWithDefaultOffer']:
        # if data[0]:
            x = 1
            for product in data[0]['data']['sector']['products']['resultsWithDefaultOffer']:

                brandName = product.get('product').get('brandName').replace(' ','-')
                name = product.get('product').get('name').replace(' ','-')
                productTypeName = product.get('product').get('productTypeName').replace(' ','-')
                id = product.get('product').get('productId')
                product_url_data = brandName +'-'+ name +'-'+ productTypeName +'-'+ str(id)
                product_url = 'https://www.galaxus.ch/en/s6/product/' + unidecode(product_url_data.lower().replace("'",''))

                x += 1
                print(x, product_url)
                yield scrapy.Request(url=product_url, callback=self.parse_detail, #headers=self.headers,
                                     )


            '''      Pagination      Start  '''
            total_p = data[0]['data']['sector']['products']['total']
            print('Total Products are :', total_p)
            if offset < total_p:
                b_url = 'https://www.galaxus.ch/api/graphql/get-sector-products'
                payload = deepcopy(self.json_data_p)
                offset = offset + 204
                payload[0]['variables']['offset'] = offset
                # print('Payload is :', payload)
                yield scrapy.Request(url=b_url, body=json.dumps(payload), method='POST', callback=self.parse,
                                     headers=self.headers,
                                     meta={'offset': offset})

    def parse_detail(self, response):
        item = dict()

        item['Ser'] = self.count
        self.count += 1

        #####   German
        # item['Title'] = response.xpath("//*[contains(@class,'sc-d963cb62-0 btKhJv')]/text()").get('').strip()
        # item['Hersteller'] = response.xpath("//*[contains(@class,'sc-97b41d14-0 wgwuz')]/strong/text()").get('').strip()
        # item['Herstellernr.'] = response.xpath("//*[contains(text(),'Herstellernr')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span/span/text()").get('').strip()
        # item['Kategorie'] = response.xpath("//*[contains(@class,'sc-ccd25b80-0 beNCEW sc-f40471c7-4 hKPleA') and contains(@href,'/producttype')]/text()").get('').strip()
        # item['Verkaufsrang in Kategorie'] = response.xpath("//*[contains(text(),'Verkaufsrang in Kategorie')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span[1]/span[1]/a[1]/text()").get('').strip()
        # item['Externe Links'] = response.xpath("//*[contains(text(),'Externe Links')]/following-sibling::td[1]/div[1]/div[1]/div/a[1]/@href").getall()
        # item['Medizinprodukt Klasse'] = response.xpath("//*[contains(text(),'Nahrungsergänzungsmittel')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span[1]/span[1]/text()").get('').strip()
        # item['Medizinische Fachanwendung'] = response.xpath("//*[contains(text(),'Anwendungsgebiet')]/following-sibling::td[1]/div[1]/div[1]/div/span[1]/span[1]/text()").get('').strip()
        # item['Number of Reviews'] = response.xpath("//*[contains(@class,'sc-a84ca9f0-2 iKVqPF')]/text()").get('').strip()
        # item['EAN'] = response.xpath("//*[contains(@property,'gtin')]/@content").get('').strip()
        # item['Price'] = response.xpath("//*[contains(@class,'sc-d112a1b0-5 hMnFnN')]/text()").get('').strip().replace('.–','').replace('–','')
        # item['Link'] = response.url

        #####    English
        item['Title'] = response.xpath("//*[contains(@class,'sc-d963cb62-0 btKhJv')]/text()").get('').strip()
        item['Manufacturer'] = response.xpath("//*[contains(@class,'sc-97b41d14-0 wgwuz')]/strong/text()").get('').strip()
        item['Manufacturer No'] = response.xpath("//*[contains(text(),'Manufacturer no.')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span/span/text()").get('').strip()
        item['Category'] = response.xpath("//*[contains(@class,'sc-ccd25b80-0 beNCEW sc-f40471c7-4 hKPleA') and contains(@href,'/producttype')]/text()").get('').strip()
        item['Sales Rank in Category'] = response.xpath("//*[contains(text(),'Sales rank in Category')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span[1]/span[1]/a[1]/text()").get('').strip()
        item['External Links'] = response.xpath("//*[contains(text(),'External links')]/following-sibling::td[1]/div[1]/div[1]/div/a[1]/@href").getall()
        item['Medical Device Class'] = response.xpath("//*[contains(text(),'Device type')]/following-sibling::td[1]/div[1]/div[1]/div[1]/span[1]/span[1]/text()").get('').strip()
        item['Medical Application'] = response.xpath("//*[contains(text(),'Field of application')]/following-sibling::td[1]/div[1]/div[1]/div/span[1]/span[1]/text()").getall()
        item['Number of Reviews'] = response.xpath("//*[contains(@class,'sc-a84ca9f0-2 iKVqPF')]/text()").get('').strip()
        item['EAN'] = response.xpath("//*[contains(@property,'gtin')]/@content").get('').strip()
        item['Price'] = response.xpath("//*[contains(@class,'sc-d112a1b0-5 hMnFnN')]/text()").get('').strip().replace('.–','').replace('–','')
        item['Link'] = response.url

        # print(item)
        yield item










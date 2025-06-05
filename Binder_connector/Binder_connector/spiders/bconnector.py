import scrapy

class BconnectorSpider(scrapy.Spider):
    name = 'bconnector'
    headers = {
        'authority': 'www.binder-connector.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        # 'cookie': '_gid=GA1.2.1207384818.1697977113; _ga_30F8GWX00F=GS1.1.1697977113.3.1.1697977115.0.0.0; _uetsid=1e29eea070d511ee92b78bb9187d21f0; _uetvid=50bf2b206de411eebb60e5d4f6c08a9b; _ga=GA1.2.1324915259.1697653787',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }
    url = 'https://www.binder-connector.com/en/products/automation-technology'
    base_url = 'https://www.binder-connector.com{}'
    custom_settings = {
        'FEED_URI': f'output/binder_connector_data.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, )

    def parse(self, response):
        for connector in response.css('div.productlist__item a.item__title'):
            listing_url = connector.css('::attr(href)').get()
            if listing_url:
                yield response.follow(url=listing_url, headers=self.headers, callback=self.parse_listing,
                                      dont_filter=True)

    def parse_listing(self, response):
        for item in response.css('div.productlist__item a.link-internal'):
            detail_url = item.css('::attr(href)').get()
            if detail_url:
                yield response.follow(url=detail_url, headers=self.headers, callback=self.get_available_connectors,
                                      dont_filter=True)

        next_page = response.css('li.pagination__item--next a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.parse_listing)

    def get_available_connectors(self, response):
        if response.css('ul[role="tablist"] li'):
            for connector in response.css('ul[role="tablist"] li'):
                detail_url = connector.css('::attr(href)').get()
                if detail_url:
                    yield response.follow(url=detail_url, headers=self.headers, callback=self.parse_details
                                          , dont_filter=True)
        else:
            self.parse_details(response)

    def parse_details(self, response):
        item = dict()
        item['Available numbers of contacts'] = response.css('ul[role="tablist"] li.poltabs__tab.active a::text').get(
            '').strip()
        item['Variants for number of contacts'] = ', '.join(option.css('::text').get('').strip() for option in response.css('div.variant-selector div option')).strip()
        item['Part no.'] = response.css('div.variant_orderingnumber::text').get('').replace('Part no.:', '').strip()
        item['Description'] = response.css('h1.variant_title::text').get('').strip()
        item['Category_title'] = response.css('div.category_title::text').get('').strip()
        item['picture_urls'] = ', '.join(self.base_url.format(image.css('::attr(href)').get()) for image in
                                         response.css('div.product__gallery__slide figure a'))
        item['Alternative part no.'] = response.css('div.variant__orderingnumber_old::text').get('').strip()
        item['Connector design'] = response.css('tr.field--BINDER_STECKVERBINDER_BAUFORM td.field__value::text').get(
            '').strip()
        item['Additional information'] = response.css('tr.field--BINDER_SONSTIGE_EIGENSCHAFTEN_LISTE td.field__value::text').get('').strip()
        item['Type standard'] = '\n'.join(response.xpath('//tr[@class="field--BINDER_BAUARTNORM"]/td['
                                                         '@class="field__value"]/text()').getall()).strip()
        item['Cable length '] = response.xpath('//tr[@class="field--BINDER_KABELLAENGE"]/td['
                                               '@class="field__value"]/text()').get('').strip()

        item['Version'] = response.xpath(
            '//tr[@class="field--BINDER_PS_AUSFUEHRUNG"]/td[@class="field__value"]/text()').get('').strip()
        item['Connector locking system'] = response.xpath('//tr[@class="field--BINDER_STECKVERBINDER_VERRIEGELUNG'
                                                          '"]/td[@class="field__value"]/text()').get('').strip()
        item['Termination'] = response.xpath('//tr[@class="field--BINDER_ANSCHLUSSART"]/td['
                                             '@class="field__value"]/text()').get('').strip()
        item['Degree of protection'] = response.xpath(
            '//tr[@class="field--BINDER_SCHUTZART_LISTE"]/td[@class="field__value"]/text()').get('').strip()
        item['Cross-sectional area'] = response.xpath(
            '//tr[@class="field--BINDER_ANSCHLUSSQUERSCHNITT"]/td[@class="field__value"]/text()').get('').strip()
        item['Temperature range from/to'] = response.xpath(
            '//tr[@class="field--BINDER_GRENZTEMPERATUR_C"]/td[@class="field__value"]/text()').get('').strip()
        item['Mechanical operation'] = response.xpath('//tr[@class="field--BINDER_MECHANISCHE_LEBENSDAUER"]/td['
                                                      '@class="field__value"]/text()').get('').strip()
        item['Weight (g)'] = response.xpath(
            '//tr[@class="field--BINDER_GEWICHT_G"]/td[@class="field__value"]/text()').get('').strip()
        item['Customs tariff number'] = response.xpath(
            '//tr[@class="field--BINDER_ZOLLTARIFNUMMER"]/td[@class="field__value"]/text()').get('').strip()
        item['Country of Origin'] = response.xpath(
            '//tr[@class="field--BINDER_URSPRUNGSLAND"]/td[@class="field__value"]/text()').get('').strip()
        item['Rated voltage'] = response.xpath(
            '//tr[@class="field--BINDER_MAX_BEMESSUNGSSPANNUNG_V"]/td[@class="field__value"]/text()').get('').strip()
        item['Rated impulse voltage'] = response.xpath(
            '//tr[@class="field--BINDER_BEMESSUNGS_STOSSSPANNUNG_V"]/td[@class="field__value"]/text()').get('').strip()
        item['Rated current'] = response.xpath(
            '//tr[@class="field--BINDER_BEMESSUNGSSTROM_A"]/td[@class="field__value"]/text()').get('').strip()
        item['Pollution degree'] = response.xpath(
            '//tr[@class="field--BINDER_VERSCHMUTZUNGSGRAD"]/td[@class="field__value"]/text()').get('').strip()
        item['Overvoltage category'] = response.xpath(
            '//tr[@class="field--BINDER_UEBERSPANNUNGSKATEGORIE"]/td[@class="field__value"]/text()').get('').strip()
        item['Insulating material group'] = response.xpath(
            '//tr[@class="field--BINDER_ISOLIERSTOFFGRUPPE"]/td[@class="field__value"]/text()').get('').strip()
        item['EMC compliance'] = response.xpath(
            '//tr[@class="field--BINDER_EMV_TAUGLICHKEIT"]/td[@class="field__value"]/text()').get('').strip()
        item['Housing material'] = response.xpath(
            '//tr[@class="field--BINDER_MATERIAL_GEHAEUSE"]/td[@class="field__value"]/text()').get('').strip()
        item['Contact body material'] = response.xpath(
            '//tr[@class="field--BINDER_KONTAKTKOERPER_LISTE"]/td[@class="field__value"]/text()').get('').strip()
        item['Contact material'] = response.xpath(
            '//tr[@class="field--BINDER_MATERIAL_KONTAKT"]/td[@class="field__value"]/text()').get('').strip()
        item['Contact plating'] = response.xpath(
            '//tr[@class="field--BINDER_KONTAKTOBERFLAECHE"]/td[@class="field__value"]/text()').get('').strip()
        item['Locking material'] = response.xpath(
            '//tr[@class="field--BINDER_MATERIAL_VERRIEGELUNG"]/td[@class="field__value"]/text()').get('').strip()
        item['REACH SVHC'] = response.xpath('//tr[@class="field--BINDER_SVHC"]/td[@class="field__value"]/text()').get(
            '').strip()
        item['SCIP number'] = response.xpath(
            '//tr[@class="field--BINDER_SCIP_NUMMER"]/td[@class="field__value"]/text()').get('').strip()
        item['eCl@ss 11.1'] = response.xpath(
            '//tr[@class="field--BINDER_ECLASS_111"]/td[@class="field__value"]/text()').get('').strip()
        item['ETIM 9.0'] = response.xpath('//tr[@class="field--BINDER_ETIM_90"]/td[@class="field__value"]/text()').get(
            '').strip()
        item['RoHS Directive'] = response.xpath(
            '//tr[@class="field--BINDER_ROHS_RICHTLINIE"]/td[@class="field__value"]/text()').get('').strip()
        item['Cable diameter'] = response.xpath(
            '//tr[@class="field--BINDER_KABELDURCHMESSER"]/td[@class="field__value"]/text()').get('').strip()
        item['Cross section'] = response.xpath(
            '//tr[@class="field--BINDER_QUERSCHNITT"]/td[@class="field__value"]/text()').get('').strip()
        item['Sheath material'] = response.xpath(
            '//tr[@class="field--BINDER_MATERIALMANTEL"]/td[@class="field__value"]/text()').get('').strip()
        item['Single-lead insulation'] = response.xpath(
            '//tr[@class="field--BINDER_ISOLATION_LITZE"]/td[@class="field__value"]/text()').get('').strip()
        item['Single-lead structure'] = response.xpath(
            '//tr[@class="field--BINDER_LITZENAUFBAU"]/td[@class="field__value"]/text()').get('').strip()
        item['Cable color'] = response.xpath(
            '//tr[@class="field--BINDER_MANTELFARBE"]/td[@class="field__value"]/text()').get('').strip()
        item['Conductor resistance'] = response.xpath(
            '//tr[@class="field--BINDER_LEITERWIDERSTAND"]/td[@class="field__value"]/text()').get('').strip()
        item['Bending radius, fixed cable'] = response.xpath(
            '//tr[@class="field--BINDER_BIEGERADIUS_KABEL_FEST"]/td[@class="field__value"]/text()').get('').strip()
        item['Bending radius, moving cable'] = response.xpath(
            '//tr[@class="field--BINDER_BIEGERADIUS_KABEL_BEWEGT"]/td[@class="field__value"]/text()').get('').strip()
        item['Bending cycles'] = response.xpath(
            '//tr[@class="field--BINDER_BIEGEZYKLEN"]/td[@class="field__value"]/text()').get('').strip()
        item['Permitted acceleration'] = response.xpath(
            '//tr[@class="field--BINDER_ZULAESSIGE_BESCHLEUNIGUNG"]/td[@class="field__value"]/text()').get('').strip()
        item['Travel distance, horizontal'] = response.xpath(
            '//tr[@class="field--BINDER_VERFAHRWEG_HORIZONTAL"]/td[@class="field__value"]/text()').get('').strip()
        item['Travel speed'] = response.xpath(
            '//tr[@class="field--BINDER_VERFAHRGESCHWINDIGKEIT"]/td[@class="field__value"]/text()').get('').strip()
        item['Temperature range cable in move from/to'] = response.xpath(
            '//tr[@class="field--BINDER_TEMPERATURBEREICH_KABEL_BEWEGT_C"]/td[@class="field__value"]/text()').get(
            '').strip()
        item['Temperature range cable fixed from/to'] = response.xpath(
            '//tr[@class="field--BINDER_TEMPERATURBEREICH_KABEL_FEST_C"]/td[@class="field__value"]/text()').get(
            '').strip()
        item['Wire Length'] = response.css('tr.field--BINDER_LITZENLAENGE td.field__value::text').get('').strip()
        item['Halogen free'] = response.xpath(
            '//tr[@class="field--BINDER_HALOGENFREI"]/td[@class="field__value"]/text()').get('').strip()
        datesheet = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "datasheet")]/@href').get('').strip()
        if datesheet:
            item['Data Sheet'] = self.base_url.format(datesheet)
        else:
            item['Data Sheet'] = ''
        reach = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "reach")]/@href').get('').strip()
        if reach:
            item['REACH'] = self.base_url.format(reach)
        else:
            item['REACH'] = ''
        rohs = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "rohs")][1]/@href').get('').strip()
        if rohs:
            item['RoHs'] = self.base_url.format(rohs)
        else:
            item['RoHs'] = ''
        china = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "chinarohs")]/@href').get('').strip()
        if china:
            item['China RoHs'] = self.base_url.format(china)
        else:
            item['China RoHs'] = ''
        declaration = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "rohsrichtlinie")]/@href').get(
            '').strip()
        if declaration:
            item['Declaration of conformity RoHS Directive'] = self.base_url.format(declaration)
        else:
            item['Declaration of conformity RoHS Directive'] = ''
        item['UKCA declaration of conformity Electrical Equipment'] = ''
        ukca = response.xpath('//div[@class="downloadlist"]/a[contains(@href, "ukca2012")]/@href').get('').strip()
        if ukca:
            item['UKCA declaration of conformity UK RoHS'] = self.base_url.format(ukca)
        else:
            item['UKCA declaration of conformity UK RoHS'] = ''
        item['Declaration of conformity Low Voltage Directive'] = ''
        cad = response.xpath(
            '//span[@class="download__meta"]/select/option[contains(text(),"STEP AP242")]/@data-url').get('').strip()
        if cad:
            item['CAD files'] = self.base_url.format(cad)
        else:
            item['CAD files'] = ''
        item['Insulation resistance'] = response.xpath(
            '//tr[@class="field--BINDER_ISOLATIONSWIDERSTAND_OHM"]/td[@class="field__value"]/text()').get('').strip()
        item['Detail_URL'] = response.url
        yield item

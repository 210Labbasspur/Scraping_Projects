import csv
import json
import scrapy
import datetime

class zillow_first_action(scrapy.Spider):
    name = 'zillow_first_action'
    prefix = 'https://www.zillow.com'
    url = 'https://www.zillow.com/async-create-search-page-state'
    headers = {'Content-Type': 'application/json'}

    custom_settings = {
        'FEEDS': {
            f'Output/First_Action/Zillow_First_Action - {datetime.datetime.now().strftime("%d-%m-%Y")}.json': {
            # f'Output/Zillow_First_Action - {datetime.datetime.now().strftime("%d-%m-%Y")}.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf-8',
            },
        }  # Zyte API
    }

    count = 1
    def start_requests(self):
        data_list = []
        with open('input/first_action/first_action_addresses_list.csv', 'r', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_list.append({'Address': row['Address']})

        for index, entry in enumerate(data_list, start=1):
            address = entry.get("Address").replace(',','').replace('  ','').replace(' ','-')
            url = f"https://www.zillow.com/homes/{address}_rb/"
            print(index,'# URL is : ', url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers )


    def parse(self, response):
        item = dict()
        json_data = response.css('#__NEXT_DATA__ ::text').get('').strip()
        data = json.loads(json_data)

        if data:
            zpid = data.get('props').get('pageProps',{}).get('componentProps',{}).get('zpid','')
            item['Zpid'] = data.get('props').get('pageProps',{}).get('componentProps',{}).get('zpid','')

            if data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'):
                zpid = int(data.get('props').get('pageProps',{}).get('componentProps',{}).get('zpid',''))
                r_data = json.loads(data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'))
                if r_data:
                    for value in r_data.values():
                        nested_dict = value if isinstance(value, dict) else None
                        property_dict = nested_dict.get('property') if nested_dict.get('property') else None

                        if property_dict:
                            item['Street_address'] = property_dict.get('address').get('streetAddress')
                            item['City'] = property_dict.get('address').get('city')
                            item['State'] = property_dict.get('address').get('state')
                            item['ZipCode'] = property_dict.get('address').get('zipcode')

                        item['Price'] = property_dict.get('price')
                        item['Beds'] = property_dict.get('bedrooms')
                        beds = property_dict.get('bedrooms')
                        baths = property_dict.get('bathrooms')
                        item['Baths'] = property_dict.get('bathrooms')
                        item['Sqr_feet'] = property_dict.get('livingArea')
                        item['Home_Status'] = property_dict.get('homeStatus')
                        item['Zestimate'] = property_dict.get('zestimate')
                        item['RentZestimate'] = property_dict.get('rentZestimate')
                        item['Days_on_zillow'] = property_dict.get('timeOnZillow')
                        item['Home_Type'] = property_dict.get('homeType')

                        item['Structure Area'] = property_dict.get('resoFacts', {}).get('buildingArea','')

                        ###########  Need to extract this data.
                        item['Type'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Type'),    '')
                        item["Year Built"] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Year Built'),    '')
                        item['Heating'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Heating'),    '')
                        item['Cooling'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Cooling'),    '')
                        item['Parking'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Parking'),    '')
                        item['HOA'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'HOA'),    '')
                        item['Lot'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Lot'),    '')
                        item['Price/sqft'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Price/sqft'),    '')
                        item["Offer Review Date"] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts',[]) if feature.get('factLabel') == 'Offer Review Date'),    '')

                        if property_dict.get('description'):
                            item['Event Description'] = property_dict.get('description').replace('\n', '').replace('\t', '')

                        item['Listing Photos'] = []
                        if property_dict.get('responsivePhotos'):
                            for images in property_dict.get('responsivePhotos'):
                                item['Listing Photos'].append(images.get('url'))


                        if property_dict.get('listingTypeDimension'):
                            item['Type_of_Listing'] =  property_dict.get('listingTypeDimension')

                        item['Price History'] = property_dict.get('priceHistory')

                        item['Tax History'] = property_dict.get('taxHistory')
                        item['Nearby Homes'] = []
                        try:
                            for nearby_home in property_dict.get('nearbyHomes',[]):
                                if 'sold' in nearby_home.get('homeStatus','').lower():
                                    if nearby_home.get('bedrooms') == beds and nearby_home.get('bathrooms') == baths:
                                        item['Nearby Homes'].append(nearby_home)
                        except:
                            print('Could not save Nearby Homes - ', item)

                        item['Comparable Homes'] = []
                        try:
                            if property_dict.get('homeValuation',{}):
                                for comp_home in property_dict.get('homeValuation',{}).get('comparables',{}).get('comps',[]):
                                    if 'sold' in comp_home.get('property',{}).get('homeStatus','').lower():
                                        if (comp_home.get('property',{}).get('bedrooms') == beds and
                                                comp_home.get('property',{}).get('bathrooms') == baths):
                                            item['Comparable Homes'].append(comp_home.get('property'))
                        except:
                            print('Could not save Comparable Homes - ', item)

                        item['Complete_url'] = response.url
                        item['URL'] = response.url
                        yield item

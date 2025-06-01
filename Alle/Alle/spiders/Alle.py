###############     Alle

import json
import scrapy
from copy import deepcopy

class Alle(scrapy.Spider):
    name = 'Alle'
    prefix = 'https://alle.com'
    url = 'https://api.alle.com/graphql'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'apollographql-client-name': 'consumer-web',
        'apollographql-client-version': '5.23.0',
        'content-type': 'application/json',
        'origin': 'https://alle.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    json_data1 = {
        'operationName': 'SearchQuery',
        'variables': {
            'limit': 10,
            'offset': 0,
            'searchInput': { 'sort': { 'column': 'DEFAULT',       'order': 'ASCENDING',       },
            'filters': { 'proximity': { 'geoPoint': { 'latitude': 34.0324632, 'longitude': -118.395863, }, 'radiusInMiles': 50, },
            'hours': {}, 'profile': {'productIds': ['7','8', ],'treatmentAreaIds': [],},    },  },  },
            'query': 'query SearchQuery($limit: Int!, $offset: Int!, $searchInput: ProviderSearchInput!) {\n  providerSearch(limit: $limit, offset: $offset, searchInput: $searchInput) {\n    offsetPageInfo {\n      totalResults\n      limit\n      offset\n      nextOffset\n      previousOffset\n      __typename\n    }\n    edges {\n      displayDistance\n      node {\n        id\n        providerOrganizationId\n        parentProviderOrganizationId\n        displayName\n        profileSlug\n        practiceType\n        address {\n          address1\n          address2\n          city\n          state\n          zipcode\n          __typename\n        }\n        avatarImageUrl\n        phoneNumber\n        productIds\n        treatmentAreaIds\n        geoLocation {\n          latitude\n          longitude\n          __typename\n        }\n        consultationRequestSettings {\n          feeTowardsTreatmentCost\n          __typename\n        }\n        indicators {\n          nodes {\n            label\n            slug\n            __typename\n          }\n          __typename\n        }\n        optInMarketingEvents {\n          nodes {\n            id\n            title\n            providerIsEnrolled\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
    }
    json_data2 = {
        'operationName': 'ProfileQuery',
        'variables': {
            'profileSlug': 'la-beauty-skin-center-or-toluca-lake-north-hollywood',
        },
        'query': 'query ProfileQuery($profileSlug: String!) {\n  locationPublicProfileBySlug(slug: $profileSlug) {\n    id\n    providerOrganizationId\n    parentOrganization {\n      id\n      __typename\n    }\n    displayName\n    shipToAccountNumber\n    profileSlug\n    practiceType\n    consultationRequestSettings {\n      consultationCostInCents\n      feeTowardsTreatmentCost\n      hideForm\n      __typename\n    }\n    businessHours {\n      nodes {\n        id\n        day\n        open\n        close\n        closed\n        appointmentRequired\n        __typename\n      }\n      __typename\n    }\n    contactInformation {\n      address\n      websiteUrl\n      emailAddress\n      phoneNumber\n      instagramHandle\n      facebookUrl\n      tikTokHandle\n      bookingUrl\n      __typename\n    }\n    products {\n      nodes {\n        id\n        name\n        slugName\n        type\n        treatmentAreas {\n          nodes {\n            id\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    avatarUrl\n    address {\n      city\n      state\n      __typename\n    }\n    geolocation {\n      latitude\n      longitude\n      __typename\n    }\n    galleryPhotos {\n      nodes {\n        id\n        url\n        altText\n        displayOrder\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  providerSearchIndicators(profileSlug: $profileSlug) {\n    nodes {\n      label\n      slug\n      __typename\n    }\n    __typename\n  }\n  treatmentGuides {\n    guides {\n      meta {\n        slug\n        __typename\n      }\n      content {\n        ... on TreatmentGuideContentLongForm {\n          factSheet {\n            title {\n              source\n              format\n              __typename\n            }\n            titleFact {\n              label\n              description\n              __typename\n            }\n            facts {\n              label\n              description\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    custom_settings = {'FEED_URI': 'output/Alle Record.csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    count = 1
    def start_requests(self):
        locations = [
            {"location": "Los Angeles, CA", "lat": 34.052235, "long": -118.243683},
            {"location": "New York City, NY", "lat": 40.712776, "long": -74.005974},
            {"location": "Chicago, IL", "lat": 41.878113, "long": -87.629799},
            {"location": "Dallas, TX", "lat": 32.776665, "long": -96.796989},
            {"location": "San Diego, CA", "lat": 32.715736, "long": -117.161087},
            {"location": "San Jose, CA", "lat": 37.338207, "long": -121.886330},
            {"location": "Houston, TX", "lat": 29.760427, "long": -95.369804},
            {"location": "Seattle, WA", "lat": 47.606209, "long": -122.332069},
            {"location": "Denver, CO", "lat": 39.739235, "long": -104.990250},
            {"location": "Nashville, TN", "lat": 36.162663, "long": -86.781601}
        ]
        for location in locations:#[:1]:
            payload = deepcopy(self.json_data1)
            payload['variables']['offset'] = 0
            payload['variables']['searchInput']['filters']['proximity']['geoPoint']['latitude'] = location['lat']
            payload['variables']['searchInput']['filters']['proximity']['geoPoint']['longitude'] = location['long']
            provider_no = 0
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse, headers=self.headers,
                                 meta={'provider_no':provider_no, 'payload':payload})

    def parse(self, response):
        provider_no = response.meta['provider_no']
        data = json.loads(response.text)
        for provider in data['data']['providerSearch']['edges']:
            provider_no += 1
            provider_name = provider.get('node').get('displayName')
            provider_slug = provider.get('node').get('profileSlug')
            print(self.count, provider_name, provider_slug)
            self.count += 1

            payload = deepcopy(self.json_data2)
            payload['variables']['profileSlug'] = provider_slug
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse_detail,
                                 headers=self.headers)

        '''     PAGINATION       '''
        total_providers = data['data']['providerSearch']['offsetPageInfo']['totalResults']
        print('Total Providers are : ', total_providers)
        if provider_no < total_providers:
            payload = response.meta['payload']
            payload['variables']['offset'] = data['data']['providerSearch']['offsetPageInfo']['nextOffset']
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse,
                                 headers=self.headers, meta={'provider_no': provider_no, 'payload':payload})

    def parse_detail(self, response):
        data = json.loads(response.text)
        item = dict()
        item['Name'] = data.get('data').get('locationPublicProfileBySlug').get('displayName')
        item['Location'] = data.get('data').get('locationPublicProfileBySlug').get('contactInformation').get('address') #Address
        item['Speciality'] = data.get('data').get('locationPublicProfileBySlug').get('practiceType') #practiceType : "MEDICAL_SPA"
        item['E-mail Address'] = data.get('data').get('locationPublicProfileBySlug').get('contactInformation').get('emailAddress')
        item['Website'] = data.get('data').get('locationPublicProfileBySlug').get('contactInformation').get('websiteUrl')
        item['Facebook'] = data.get('data').get('locationPublicProfileBySlug').get('contactInformation').get('facebookUrl')
        item['Instagram'] = data.get('data').get('locationPublicProfileBySlug').get('contactInformation').get('instagramHandle')

        item['No. Of Products'] = None
        no_of_products = 0
        for product in data.get('data').get('locationPublicProfileBySlug').get('products').get('nodes'):
            if product.get('type') == "AA_PRODUCT":
                no_of_products += 1
                item[f'Product {no_of_products}'] = product.get('name')

        item['No. Of Products'] = f"{no_of_products} Products"

        yield item
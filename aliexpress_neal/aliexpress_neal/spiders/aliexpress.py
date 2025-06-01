import csv
import json
from datetime import datetime

import scrapy


def get_variants(data):
    options = []
    for sku_property in data.get('priceComponent', {}).get('skuPriceList', []):
        image = ''
        price = sku_property.get('skuVal', {}).get('skuActivityAmount', {}).get('value')
        if price:
            pass
        else:
            price = sku_property.get('skuVal', {}).get('skuAmount', {}).get('value')

        all_options, var_images = get_all_options(data)
        var_images_keys = list(var_images.keys())
        selected_options = list()
        skus = sku_property.get('skuPropIds').split(',')

        for option in all_options:
            if str(option.get('option_value_id')) in skus:
                selected_options.append(option)
        for sku in skus:
            if str(sku) in var_images_keys:
                if var_images.get(str(sku)):
                    image = var_images.get(str(sku))
        options.append({
            'barcode': None,
            'sku': sku_property.get('skuPropIds'),
            'option_values': selected_options,
            'images': image if image else None,
            'price': price,
            'available_qty': sku_property.get('skuVal', {}).get('inventory', 0),
        })
    return options

def get_all_options(data):
    options = []
    variants_images = {}
    for sku_property in data.get('skuComponent', data.get('skuModule', {})).get('productSKUPropertyList', []):
        for variant_prop in sku_property.get('skuPropertyValues', []):
            options.append({
                'option_id': sku_property.get('skuPropertyId', ''),
                'option_value_id': variant_prop.get('propertyValueId', ''),
                'option_name': sku_property.get('skuPropertyName', ''),
                'option_value': variant_prop.get('propertyValueDisplayName', '')
            })
            variants_images[str(variant_prop.get('propertyValueId', ''))] = variant_prop.get('skuPropertyImagePath', '')
    return options, variants_images


class AliexpressSpider(scrapy.Spider):
    name = "aliexpress"
    start_urls = ['https://www.aliexpress.com/']
    custom_settings = {
        'FEED_URI': 'outputs/aliexpress_output.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        for input_dict in list(csv.DictReader(open('input/input_urls.csv', 'r'))):
            for i in range(1, 61):
                final_url = f"{input_dict.get('urls')}&page={i}"
                yield scrapy.Request(url=final_url, callback=self.parse_listing,
                                     meta={'listing_url': input_dict.get('urls')}, dont_filter=True)

    def parse_listing(self, response):
        json_data = json.loads(response.css('script::text').re_first(r'_init_data_\s*=\s*{\s*data:\s*({.+}) }'))
        category = json_data.get('data', {}).get('root', {}).get('fields', {}).get('pageInfo', {}).get('trace', {}).get('utLogMap', {}).get('query')
        for product_url in json_data.get('data', {}).get('root', {}).get('fields', {}).get('mods', {}).get('itemList',
                                                                                                           {}).get(
            'content', []):
            product_url = f"https://www.aliexpress.us/item/{product_url.get('productId')}.html?gatewayAdapt=glo2usa&_randl_shipto=US"
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'retry': 0, 'category': category}
            )

    def parse_product(self, response):
        try:
            json_data = json.loads(response.css('script').re_first('data: (.+)'))
            variants_data = get_variants(json_data)
            price = variants_data[0].get('price') if variants_data else 0
            options, var_images = get_all_options(json_data)
            item = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'url': response.url,
                'source': 'aliexpress_us',
                'product_id': json_data.get('productInfoComponent', {}).get('id'),
                'existence': True,
                'title': json_data.get('productInfoComponent', {}).get('subject'),
                'title_en': None,
                'description': '',
                'summary': None,
                'sku': json_data.get('productInfoComponent', {}).get('id'),
                'upc': None,
                'brand': json_data.get('sellerComponent', {}).get('storeName'),
                'specifications': [{'name': spec.get('attrName'), 'value': spec.get('attrValue')} for spec in
                                   json_data.get('productPropComponent', {}).get('props')],
                'categories': response.meta['category'],
                'images': ';'.join(json_data.get('imageComponent', {}).get('imagePathList', [])),
                'videos': None,
                'price': price,
                'available_qty': json_data.get('inventoryComponent', {}).get('totalAvailQuantity'),
                'options': options,
                'variants': variants_data,
                'returnable': None,
                'reviews': json_data.get('feedbackComponent', {}).get('totalValidNum'),
                'rating': json_data.get('feedbackComponent', {}).get('evarageStar'),
                'sold_count': json_data.get('tradeComponent', {}).get('formatTradeCount'),
                'shipping_fee': json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', [])[0].get('bizData', {}).get('displayAmount', '0') if json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', []) else '',
                'shipping_days_min': json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', [])[0].get('bizData', {}).get('deliveryDayMin')if json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', [])else '',
                'shipping_days_max': json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', [])[0].get('bizData', {}).get('deliveryDayMax') if json_data.get('webGeneralFreightCalculateComponent', {}).get('originalLayoutResultList', [])else '',
                'weight': json_data.get('packageComponent', {}).get('pound_weight'),
                'width': json_data.get('packageComponent', {}).get('inch_width'),
                'height': json_data.get('packageComponent', {}).get('inch_height'),
                'length': json_data.get('packageComponent', {}).get('inch_length'),

            }
            description_url = json_data.get('productDescComponent', {}).get('descriptionUrl')
            yield scrapy.Request(
                url=description_url,
                callback=self.parse_description,
                meta={'item': item}
            )
        except:
            retry = response.meta['retry']
            if retry < 5:
                retry = retry + 1
                yield scrapy.Request(
                    url=response.url,
                    callback=self.parse_product,
                    meta={'retry': retry, 'category': response.meta['category']}
                )

    def parse_description(self, response):
        item = response.meta['item']
        item['description'] = response.text
        yield item

import csv
import json
import scrapy

class Airbp(scrapy.Spider):
    name = 'Airbp'

    def start_requests(self):
        with open('inputs/test_JSON(2).json', 'r') as file:
            data = json.load(file)

        for element in data[0]['data']['fuelPrice']['prices']:
            if isinstance(element, dict):
                item = dict()
                item['GRN'] = data[0]['data']['fuelPrice']['grn']
                item['Airport'] = element.get('countryName') + ' , ' + element.get('locationName')
                item['IATA'] = element.get('iata')
                item['ICAO'] = element.get('icao')
                item['Fuel Type'] = element.get('fuelType')
                item['Effective From'] = element.get('price').get('effectiveFrom')
                item['Valid Until'] = element.get('price').get('effectiveTo')
                item['Delivery Area'] = element.get('deliveryArea')
                item['Into Plane Provider'] = element.get('fuelProvider')
                item['Pricing Basis'] = element.get('price').get('pricingBasis')
                item['Total Fuel Price (EUR/LT)'] = element.get('price').get('totalPrice')
                item['Single Fixed Charges (EUR/operation)'] = element.get('price').get('mandatoryFixed')

                # Calculate price for 150 & 300 liters
                price_for_150ltr = self.calculate_price(element, 150)
                price_for_300ltr = self.calculate_price(element, 300)

                # Add results to the 'item' dictionary
                item['Price for 150 Ltr Fuel (EUR)'] = price_for_150ltr
                item['Price for 300 Ltr Fuel (EUR)'] = price_for_300ltr

                csv_file = 'output/Airbp_updated_Sample(LPFR).csv'
                with open(csv_file, 'w', newline='') as file:
                    csv_writer = csv.DictWriter(file, fieldnames=item.keys())
                    csv_writer.writeheader()
                    csv_writer.writerow(item)

        yield scrapy.Request(url='https://example.com/', callback=self.parse)

    def parse(self, response):
        pass

    def calculate_price(self, element, volume):
        price = (volume * float(element.get('price').get('totalPrice'))) + float(element.get('price').get('mandatoryFixed'))
        price_before_tax = price

        # Process compulsory taxes and fees
        compulsory = element.get('taxesAndFees').get('compulsory')
        for comp in compulsory:
            if comp.get('chargeType') == 'Variable':
                price = price + (float(comp.get('value')) * volume)
            elif comp.get('chargeType') == 'Fixed':
                price = price + float(comp.get('value'))
            elif comp.get('chargeType') == 'Percentage':
                price = price_before_tax + (price_before_tax * float(comp.get('value')))

        # Process conditional taxes and fees
        conditional = element.get('taxesAndFees').get('conditional')
        for cond in conditional:
            if cond.get('chargeType') == 'Variable':
                price = price + (float(cond.get('value')) * volume)
            elif cond.get('chargeType') == 'Fixed':
                price = price + float(cond.get('value'))
            elif cond.get('chargeType') == 'Percentage':
                price = price_before_tax + (price_before_tax * float(cond.get('value')))

        return round(price, 2)


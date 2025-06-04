# #####           Market Records (Complete).csv
#
# import scrapy
# from scrapy import Selector
# import csv
# import datetime
#
# input_file_path = "Market Records (Complete).csv"
# output_file_path = "Modified_Market_Records.csv"
#
# # Read the CSV file
# with open(input_file_path, 'r') as infile:
#     reader = csv.DictReader(infile)
#     rows = list(reader)
#
# # Add a new column
# for row in rows:
#     row['Date Ingested'] = datetime.datetime.now().strftime("%Y-%m-%d")
#
#     # Split the 'Make & Model' column into 'Make' and 'Model'
#     make_model = row['Make & Model'].split(' - ', 1)
#     row['Make'] = make_model[0]
#     row['Model'] = make_model[1] if len(make_model) > 1 else ''
#
# # Write the modified data to a new CSV file
# fieldnames = ['Date Ingested', 'Make', 'Model'] + reader.fieldnames
#
# with open(output_file_path, 'w', newline='') as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(rows)
#
# print(f"File '{output_file_path}' has been created with the modifications.")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# '''
#
#
#
#
# file_path = 'draft_html_code.txt'
# with open(file_path, 'r', encoding='utf-8') as file:
#     html_content = file.read()
# response = Selector(text=html_content)
#
# # links = response.xpath('//a/@href').getall()
# # text_content = response.xpath('//div[@class="example-class"]/text()').get()
# print(html_content)
# item = dict()
#
# print(f'SHITTT IS', response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get(''), ' ********')
# print(f'SHITTT IS', response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get(''), ' ********')
# print(f'SHITTT IS', response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get(''), ' ********')
#
# print('%%%%%%%%^%*%*%%%%%%%%%%%%%%%*%%%%%%%%%%%%%%*%%%%%%%%%')
# DOM = response.css('.row-line::text').getall()
# print(DOM[-6:])
# print('%%%%%%%%^%*%*%%%%%%%%%%%%%%%*%%%%%%%%%%%%%%*%%%%%%%%%')
#
# item['Resale_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
# item['Resale_Retail (2023)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
# item['Resale_Retail (2022)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#
# item['Retail_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[1]/a/text()").get('')
# item['Retail_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[2]/a/text()").get('')
# item['Retail_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[3]/a/text()").get('')
#
# item['Dealer_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[1]/a/text()").get('')
# item['Dealer_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[2]/a/text()").get('')
# item['Dealer_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[3]/a/text()").get('')
#
# item['Other_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[1]/a/text()").get('')
# item['Other_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[2]/a/text()").get('')
# item['Other_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[3]/a/text()").get('')
#
# item['Net_Dealer_Inv (YTD)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[1]/text()").get('')
# item['Net_Dealer_Inv (2023)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[2]/text()").get('')
# item['Net_Dealer_Inv (2022)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[3]/text()").get('')
#
# item['DOM - Sold (Average) (YTD)'] = DOM[-6]
# item['DOM - Sold (Average) (2023)'] = DOM[-5]
# item['DOM - Sold (Average) (2022)'] = DOM[-4]
# item['DOM - Sold (Median) (YTD)'] = DOM[-3]
# item['DOM - Sold (Median) (2023)'] = DOM[-2]
# item['DOM - Sold (Median) (2022)'] = DOM[-1]
#
# print(item)
#
#
#
#
#
#
#
#
#
#
#
#
#                     # item['Transaction Market History'] = response.xpath("//*[contains(@class,'trans-history-horz-table')]/tr").extract()
#                     trans_history = response.xpath("//*[contains(@class,'trans-history-horz-table')]/tr").getall()
#                     print(f'\n*********************************\n{trans_history}\n***********************************')
#
#                     # trans_market_history_table = response.xpath("//*[contains(@class,'trans-history-horz-table')]/tr").extract()
#                     t_r = response.xpath("//*[contains(@class,'trans-history-horz-table')]/tr").extract()
#                     # for t_r in trans_market_history_table[1:]:
#                     item['Resale_Retail (YTD)'] = t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     item['Resale_Retail (2023)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     item['Resale_Retail (2022)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#
#                     item['Retail_to_Retail (YTD)'] = t_r[2].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     item['Retail_to_Retail (2023)'] =  t_r[2].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     item['Retail_to_Retail (2022)'] =  t_r[2].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#                     item['Dealer_to_Retail (YTD)'] = t_r[3].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     item['Dealer_to_Retail (2023)'] =  t_r[3].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     item['Dealer_to_Retail (2022)'] =  t_r[3].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#                     item['Other_to_Retail (YTD)'] = t_r[4].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     item['Other_to_Retail (2023)'] =  t_r[4].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     item['Other_to_Retail (2022)'] =  t_r[4].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#                     item['Net_Dealer_Inv (YTD)'] = t_r[5].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     item['Net_Dealer_Inv (2023)'] =  t_r[5].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     item['Net_Dealer_Inv (2022)'] =  t_r[5].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#
#                     # item['DOM - Sold (Average) (YTD)'] = t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     # item['DOM - Sold (Average) (2023)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     # item['DOM - Sold (Average) (2022)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#                     # item['DOM - Sold (Median) (YTD)'] = t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
#                     # item['DOM - Sold (Median) (2023)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
#                     # item['DOM - Sold (Median) (2022)'] =  t_r[1].xpath("//td[@class='row-line' and contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')
#
#
#
#
# '''
import json
import re
import csv
import scrapy
from copy import deepcopy
import urllib.parse

class FCA(scrapy.Spider):
    name = 'FCA'
    headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
  'cache-control': 'no-cache',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://register.fca.org.uk',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://register.fca.org.uk/s/search?q=804843&type=Companies',
  'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
  'x-sfdc-page-cache': '832ba63516c8737c',
  'x-sfdc-page-scope-id': '327519af-2dac-4d3e-9c54-5ae65deffcc3',
  'x-sfdc-request-id': '11155600000cd81cd1',
  'Cookie': 'CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}
    data = {
            "message": {
              "actions": [
                {
                  "id": "515;a",
                  "descriptor": "apex://ShPo_LEX_Reg_SearchController/ACTION$getFirmDetails",
                  "callingDescriptor": "markup://c:ShPo_LEX_Reg_SearchContainer",
                  "params": {
                    "searchValues": [
                      "804843"
                    ],
                    "pageSize": "20",
                    "pageNo": 1,
                    "typeOfSearch": "Companies",
                    "location": {
                      "longitude": '',
                      "latitude": '',
                    },
                    "orderBy": "",
                    "sectorCriteria": " includes ('Investment','Pensions','Mortgage')",
                    "hideUnauthFirm": True,
                    "hideIntroARVal": False,
                    "investmentTypes": [

                    ]
                  },
                  "storable": True,
                }
              ]
            },
            "aura.context": {
              "mode": "PROD",
              "fwuid": "eGx3MHlRT1lEMUpQaWVxbGRUM1h0Z2hZX25NdHFVdGpDN3BnWlROY1ZGT3cyNTAuOC4zLTYuNC41",
              "app": "siteforce:communityApp",
              "loaded": {
                "APPLICATION@markup://siteforce:communityApp": "vgD8vvaBHzgKYqb_JQjQdw",
                "COMPONENT@markup://instrumentation:o11ySecondaryLoader": "1JitVv-ZC5qlK6HkuofJqQ"
              },
              "dn": [

              ],
              "globals": {

              },
              "uad": False,
            },

            "aura.pageURI": "/s/search?q=804843&type=Companies",
            "aura.token": '',

            }

    custom_settings = {'FEED_URI': 'output/FCA.csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    database = []
    def start_requests(self):
        file_path = "input/20240812 Investment Firms Register.csv"
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                itemid = row['FRN']
                if itemid:
                    self.database.append(itemid)

        for index, frn in enumerate(self.database, start=1):
            print(index, ' FRN :', frn)

            url = "https://register.fca.org.uk/s/sfsites/aura?r=1&other.ShPo_LEX_Reg_Search.getFirmDetails=1"
            # payload = (f"message=%7B%22actions%22%3A%5B%7B%22id%22%3A%22515%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_SearchController%2FACTION%24getFirmDetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AShPo_LEX_Reg_SearchContainer%22%2C%22params%22%3A%7B%22searchValues%22%3A%5B%22"
            payload = (f"message=%7B%22actions%22%3A%5B%7B%22id%22%3A%22247%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_SearchController%2FACTION%24getFirmDetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AShPo_LEX_Reg_SearchContainer%22%2C%22params%22%3A%7B%22searchValues%22%3A%5B%22"
                       f"{frn}%22%5D%2C%22pageSize%22%3A%2220%22%2C%22pageNo%22%3A1%2C%22typeOfSearch%22%3A%22Companies%22%2C%22location%22%3A%7B%22longitude%22%3Anull%2C%22latitude%22%3Anull%7D%2C%22orderBy%22%3A%22%22%2C%22sectorCriteria%22%3A%22%20includes%20('Investment'%2C'Pensions'%2C'Mortgage')%22%2C%22hideUnauthFirm%22%3Atrue%2C%22hideIntroARVal%22%3Afalse%2C%22investmentTypes%22%3A%5B%5D%7D%2C%22storable%22%3Atrue%7D%5D%7D&"
                       f"aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22eGx3MHlRT1lEMUpQaWVxbGRUM1h0Z2hZX25NdHFVdGpDN3BnWlROY1ZGT3cyNTAuOC4zLTYuNC41%22%2C%22app%22%3A%22siteforce%3AcommunityApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%22vgD8vvaBHzgKYqb_JQjQdw%22%2C%22COMPONENT%40markup%3A%2F%2Finstrumentation%3Ao11ySecondaryLoader%22%3A%221JitVv-ZC5qlK6HkuofJqQ%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Afalse%7D&"
                       f"aura.pageURI=%2Fs%2Fsearch%3Fq%3D{frn}%26type%3DCompanies&aura.token=null")
            yield scrapy.Request(url=url, body=payload, method='POST', callback=self.parse, headers=self.headers)


    def parse(self, response):
        data = json.loads(response.text)
        # print(data)
        if data:
            item = dict()
            if data.get('actions',[]):
                if data.get('actions',[])[0].get('returnValue',{}).get('accDetails',[]):
                    id = data.get('actions',[])[0].get('returnValue',{}).get('accDetails',[])[0].get('acc',{}).get('Id')
                    item['Company Name'] = data.get('actions',[])[0].get('returnValue',{}).get('accDetails',[])[0].get('acc',{}).get('Name')
                    # print('Company Name is : ', item['Company Name'])

                    detail_url = 'https://register.fca.org.uk/s/sfsites/aura?r=0&other.ShPo_LEX_Reg_FirmDetail.initMethod=1&other.ShPo_LEX_Reg_GetMetadataContent.getFeatureListContent=2&other.ShPo_LEX_Reg_Utilities.getStaticResrouceFile=2&other.ShPo_LEX_Reg_Utility.GetGADetails=2&ui-communities-components-aura-components-forceCommunity-navigationMenu.NavigationMenuDataProvider.getNavigationMenu=1&ui-self-service-components-profileMenu.ProfileMenu.getProfileMenuResponse=1'
                    true = True
                    false = False
                    null = None
                    json_data = dict()
                    # json_data['actions'] = data['actions']
                    json_data['actions'] = {"actions":[{"id":"247;a","descriptor":"serviceComponent://ui.communities.components.aura.components.forceCommunity.navigationMenu.NavigationMenuDataProviderController/ACTION$getNavigationMenu","callingDescriptor":"UNKNOWN","params":{"navigationLinkSetIdOrName":"","includeImageUrl":false,"addHomeMenuItem":true,"menuItemTypesToSkip":["SystemLink","Event","Modal"],"masterLabel":"Default Navigation"},"version":"61.0","storable":true},{"id":"62;a","descriptor":"serviceComponent://ui.self.service.components.profileMenu.ProfileMenuController/ACTION$getProfileMenuResponse","callingDescriptor":"markup://selfService:profileMenuAPI","params":{},"version":"61.0"},{"id":"87;a","descriptor":"apex://ShPo_LEX_Reg_Utility/ACTION$GetGADetails","callingDescriptor":"markup://c:ShPo_LEX_Reg_GlobalRequirements","params":{"strProject":"NewRegister"}},{"id":"251;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"252;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"253;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"254;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"255;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"256;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"141;a","descriptor":"apex://ShPo_LEX_Reg_Utility/ACTION$GetGADetails","callingDescriptor":"markup://c:ShPo_LEX_Reg_SearchForm","params":{"strProject":"NewRegister"},"version":null},{"id":"257;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"258;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"259;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"260;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"309;a","descriptor":"apex://ShPo_LEX_Reg_GetMetadataContent/ACTION$getFeatureListContent","callingDescriptor":"UNKNOWN","params":{"featureList":["Masthead-Data"]},"storable":true},{"id":"261;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"262;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"310;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"ShPo_LEX_Reg_IllustrativeIcons"},"storable":true},{"id":"263;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true},{"id":"462;a","descriptor":"apex://ShPo_LEX_Reg_GetMetadataContent/ACTION$getFeatureListContent","callingDescriptor":"UNKNOWN","params":{"featureList":["Footer-Link-List-Left","Footer-Link-List-Right","Footer-Link-List-Bottom"]},"storable":true},{"id":"238;a","descriptor":"apex://ShPo_LEX_Reg_FirmDetailController/ACTION$initMethod","callingDescriptor":"markup://c:ShPo_LEX_Reg_FirmDetails","params":{"orgId":f"{id}"}},{"id":"463;a","descriptor":"apex://ShPo_LEX_Reg_Utilities/ACTION$getStaticResrouceFile","callingDescriptor":"UNKNOWN","params":{"file":"Symbols"},"storable":true}]}
                    # print('JSON Data :', json_data)
                    json_string = json.dumps(json_data)
                    final_string = f"message={urllib.parse.quote(json_string)}"
                    # print('Converted Data into encrypted string is : ', final_string)
                    payload = (f"{final_string}"
                    # payload = (f"message=%7B%22actions%22%3A%5B%7B%22id%22%3A%22247%3Ba%22%2C%22descriptor%22%3A%22serviceComponent%3A%2F%2Fui.communities.components.aura.components.forceCommunity.navigationMenu.NavigationMenuDataProviderController%2FACTION%24getNavigationMenu%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22navigationLinkSetIdOrName%22%3A%22%22%2C%22includeImageUrl%22%3Afalse%2C%22addHomeMenuItem%22%3Atrue%2C%22menuItemTypesToSkip%22%3A%5B%22SystemLink%22%2C%22Event%22%2C%22Modal%22%5D%2C%22masterLabel%22%3A%22Default%20Navigation%22%7D%2C%22version%22%3A%2261.0%22%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%2262%3Ba%22%2C%22descriptor%22%3A%22serviceComponent%3A%2F%2Fui.self.service.components.profileMenu.ProfileMenuController%2FACTION%24getProfileMenuResponse%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2FselfService%3AprofileMenuAPI%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A%2261.0%22%7D%2C%7B%22id%22%3A%2287%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utility%2FACTION%24GetGADetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AShPo_LEX_Reg_GlobalRequirements%22%2C%22params%22%3A%7B%22strProject%22%3A%22NewRegister%22%7D%7D%2C%7B%22id%22%3A%22251%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22252%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22253%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22254%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22255%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22256%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22141%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utility%2FACTION%24GetGADetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AShPo_LEX_Reg_SearchForm%22%2C%22params%22%3A%7B%22strProject%22%3A%22NewRegister%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%22257%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22258%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22259%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22260%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22309%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_GetMetadataContent%2FACTION%24getFeatureListContent%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22featureList%22%3A%5B%22Masthead-Data%22%5D%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22261%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22262%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22310%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22ShPo_LEX_Reg_IllustrativeIcons%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22263%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22462%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_GetMetadataContent%2FACTION%24getFeatureListContent%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22featureList%22%3A%5B%22Footer-Link-List-Left%22%2C%22Footer-Link-List-Right%22%2C%22Footer-Link-List-Bottom%22%5D%7D%2C%22storable%22%3Atrue%7D%2C%7B%22id%22%3A%22238%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_FirmDetailController%2FACTION%24initMethod%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AShPo_LEX_Reg_FirmDetails%22%2C%22params%22%3A%7B%22orgId%22%3A%220010X00004OktcCQAR%22%7D%7D%2C%7B%22id%22%3A%22463%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FShPo_LEX_Reg_Utilities%2FACTION%24getStaticResrouceFile%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22file%22%3A%22Symbols%22%7D%2C%22storable%22%3Atrue%7D%7D"
                               f"&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22eGx3MHlRT1lEMUpQaWVxbGRUM1h0Z2hZX25NdHFVdGpDN3BnWlROY1ZGT3cyNTAuOC4zLTYuNC41%22%2C%22app%22%3A%22siteforce%3AcommunityApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%22vgD8vvaBHzgKYqb_JQjQdw%22%2C%22COMPONENT%40markup%3A%2F%2Finstrumentation%3Ao11ySecondaryLoader%22%3A%221JitVv-ZC5qlK6HkuofJqQ%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Afalse%7D&aura.pageURI=%2Fs%2Ffirm%3F"
                               f"id%3D{id}&aura.token=null")
                    # print('Payload is :', payload)
                    yield scrapy.Request(url=detail_url, body=payload, method='POST', callback=self.detail_parse,
                                         headers=self.headers, meta={'item':item})


    def detail_parse(self, response):
        item = response.meta['item']
        data = json.loads(response.text)

        if data.get('actions',[]):
            for record in data.get('actions',[]):
                if record.get("id") == "238;a":
                    id = record.get('returnValue',{}).get('accnt',{}).get('Id','')
                    item['Company Name'] = record.get('returnValue',{}).get('accnt',{}).get('Name','')

                    # print('Company Name is : ', item['Company Name'])

                    item['Registered Company No'] = record.get('returnValue',{}).get('accnt',{}).get('ShGl_CompaniesHouseNumber__c','')

                    item['Phone'] = ''
                    phone_code = record.get('returnValue',{}).get('principalAddress',{}).get('ShGl_PhoneCountryCode__c','').replace('\xa0', '')
                    phone_no = record.get('returnValue',{}).get('principalAddress',{}).get('ShGl_PhoneNumber__c','').replace('\xa0', '')
                    if phone_no:
                        phone_no = f"({phone_no[:3]}) {phone_no[3:6]} {phone_no[6:]}"
                        item['Phone'] = f'{phone_code} - {phone_no}'

                    item['Email'] = record.get('returnValue',{}).get('principalAddress',{}).get('ShGl_EmailAddress__c','')
                    item['Website'] = record.get('returnValue',{}).get('principalAddress',{}).get('ShGl_WebsiteAddress__c','')
                    item['Status'] = record.get('returnValue',{}).get('accnt',{}).get('ShGl_Status__c','')
                    item['Type'] = record.get('returnValue',{}).get('accnt',{}).get('ShGl_BusinessType__c','')

                    # individuals = record.get('returnValue', {}).get('currentIndividualsList', [])
                    # item['Individuals'] = []
                    # for individual in individuals:
                    #     for smf in individual.get('Approved_Controlled_Functions__r', []):
                    #         order = smf.get('ShGl_InvolvementType__r', {}).get('ShPo_Lex_Reg_Firm_Rec_CF_Ordering__c')
                    #         if order in [16, 1, 3]:
                    #             item['Individuals'].append(individual.get('Name'))
                    individuals = record.get('returnValue',{}).get('currentIndividualsList',[])
                    smf_16 = []
                    smf_1 = []
                    smf_3 = []
                    for individual in individuals:
                        for smf in individual.get('Approved_Controlled_Functions__r'):
                            if smf.get('ShGl_InvolvementType__r',{}).get('ShPo_Lex_Reg_Firm_Rec_CF_Ordering__c') == 16:
                                smf_16.append(individual.get('Name'))
                            elif smf.get('ShGl_InvolvementType__r',{}).get('ShPo_Lex_Reg_Firm_Rec_CF_Ordering__c') == 1:
                                smf_1.append(individual.get('Name'))
                            elif smf.get('ShGl_InvolvementType__r',{}).get('ShPo_Lex_Reg_Firm_Rec_CF_Ordering__c') == 3:
                                smf_3.append(individual.get('Name'))
                    if smf_16:
                        item['Individual'] = ', '.join(smf_16)
                    elif smf_1:
                        item['Individual'] = ', '.join(smf_1)
                    elif smf_3:
                        item['Individual'] = ', '.join(smf_3)

                    # item['Detail_URL'] = f'https://register.fca.org.uk/s/firm?id={id}'
                    yield item

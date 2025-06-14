######  FightOdds

import re
import csv
import copy
import scrapy
import pymongo
import mimetypes
from parsel import Selector
from datetime import datetime
import requests, json, time, threading, queue, os
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import NoCredentialsError, ClientError
class FightOdds(scrapy.Spider):
    name = 'FightOdds'
    url = "https://api.fightinsider.io/gql"
    data = json.dumps({
        "query": "query OddsEventMenuQrQuery {\n  promotions: allPromotions(isActive: true) {\n    ...OddsEventMenu_promotions\n  }\n  upcomingEvents: allEvents(upcoming: true, orderBy: \"date\", isCancelled: false) {\n    ...OddsEventMenu_events\n    edges {\n      node {\n        straightOfferCount\n        promotion {\n          id\n        }\n        id\n      }\n    }\n  }\n  sportsbooks: allSportsbooks(hasOdds: true) {\n    ...OddsEventMenu_sportsbooks\n  }\n  eventOfferTable(nextEvent: true, isCancelled: false) {\n    ...OddsEventMenu_eventOfferTable\n    id\n  }\n}\n\nfragment EventOfferTable_eventOfferTable on EventOfferTableNode {\n  name\n  pk\n  fightOffers {\n    edges {\n      node {\n        id\n        fighter1 {\n          firstName\n          lastName\n          slug\n          id\n        }\n        fighter2 {\n          firstName\n          lastName\n          slug\n          id\n        }\n        bestOdds1\n        bestOdds2\n        slug\n        propCount\n        isCancelled\n        straightOffers {\n          edges {\n            node {\n              sportsbook {\n                id\n                shortName\n                slug\n              }\n              outcome1 {\n                id\n                odds\n                ...OddsWithArrowButton_outcome\n              }\n              outcome2 {\n                id\n                odds\n                ...OddsWithArrowButton_outcome\n              }\n              id\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment EventOfferTable_sportsbooks on SportsbookNodeConnection {\n  edges {\n    node {\n      id\n      shortName\n      slug\n    }\n  }\n}\n\nfragment OddsEventMenu_eventOfferTable on EventOfferTableNode {\n  pk\n  ...EventOfferTable_eventOfferTable\n}\n\nfragment OddsEventMenu_events on EventNodeConnection {\n  edges {\n    node {\n      pk\n      id\n      name\n      slug\n      date\n      straightOfferCount\n      promotion {\n        id\n      }\n    }\n  }\n}\n\nfragment OddsEventMenu_promotions on PromotionNodeConnection {\n  edges {\n    node {\n      id\n      shortName\n      logo\n    }\n  }\n}\n\nfragment OddsEventMenu_sportsbooks on SportsbookNodeConnection {\n  ...EventOfferTable_sportsbooks\n}\n\nfragment OddsWithArrowButton_outcome on OutcomeNode {\n  id\n  ...OddsWithArrow_outcome\n}\n\nfragment OddsWithArrow_outcome on OutcomeNode {\n  odds\n  oddsPrev\n}\n",
        "variables": {},
    })

    data2 = json.dumps({
        "query": "query FightPropOfferSubTableQrQuery(\n  $fightSlug: String!\n) {\n  sportsbooks: allSportsbooks(hasOdds: true) {\n    ...FightPropOfferSubTable_sportsbooks\n  }\n  fightPropOfferTable(slug: $fightSlug) {\n    ...FightPropOfferSubTable_fightPropOfferTable\n    id\n  }\n}\n\nfragment FightPropOfferSubTable_fightPropOfferTable on FightPropOfferTableNode {\n  propOffers {\n    edges {\n      node {\n        propName1\n        propName2\n        bestOdds1\n        bestOdds2\n        offerType {\n          id\n          offerTypeId\n        }\n        offers {\n          edges {\n            node {\n              sportsbook {\n                id\n              }\n              outcome1 {\n                id\n                odds\n                ...OddsWithArrowButton_outcome\n              }\n              outcome2 {\n                id\n                odds\n                ...OddsWithArrowButton_outcome\n              }\n              id\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment FightPropOfferSubTable_sportsbooks on SportsbookNodeConnection {\n  edges {\n    node {\n      id\n      shortName\n      slug\n    }\n  }\n}\n\nfragment OddsWithArrowButton_outcome on OutcomeNode {\n  id\n  ...OddsWithArrow_outcome\n}\n\nfragment OddsWithArrow_outcome on OutcomeNode {\n  odds\n  oddsPrev\n}\n",
        "variables": {"fightSlug": "bill-algeo-vs-kyle-nelson-52226"}
    })
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://fightodds.io',
        'referer': 'https://fightodds.io/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        # 'Cookie': 'csrftoken=2mgXk1axsLtcI05SL8ywOAhjLUQfIxTZbayP3sPT5Rv0aqzJ4BroW0k7T4Cvnxw7'
        }
    count = 0
    fields_to_assign = ["Bet","BetOnline", "BetOnline Move","Bovada", "Bovada Move", "Pinnacle", "Pinnacle Move",
                        "Betway", "Betway Move", "MyBookie", "MyBookie Move","BetUS", "BetUS Move", "SXBet", "SXBet Move",
                        "Jazz", "Jazz Move", "Cloudbet", "Cloudbet Move","Unibet", "Unibet Move", "DraftKings", "DraftKings Move",
                        "FanDuel", "FanDuel Move", "BetAnySports", "BetAnySports Move"]

    custom_settings = {
        'FEED_URI': 'Output/FightOdds (Sample).csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',}

    def start_requests(self):
        payload = json.loads(self.data)
        yield scrapy.Request(url=self.url, method='POST', body=self.data, headers=self.headers, callback=self.parse)
        # yield scrapy.FormRequest(url=self.url, formdata=payload, method='POST',    headers=self.headers)

    def parse(self, response):
        print('Welcome to parse Method')
        data = json.loads(response.text)
        for Matches in data['data']['eventOfferTable']['fightOffers']['edges']:
            item = {    "Event": None, "Fight": None}

            fighter1 = Matches.get('node').get('fighter1')
            fighter1_fn = f"{fighter1['firstName']} {fighter1['lastName']}"
            fighter2 = Matches.get('node').get('fighter2')
            fighter2_fn = f"{fighter2['firstName']} {fighter2['lastName']}"

            event = f"UFC on ESPN {fighter1['lastName']} vs {fighter2['lastName']}"
            item['Event'] = event
            fight = f"{fighter1_fn} , {fighter2_fn}"
            item['Fight'] = fight


            '''         Extracting further data                 '''
            payload1 = json.loads(self.data2)
            slug = Matches.get('node').get('slug')
            payload1['variables'] = {"fightSlug": f"{slug}"}
            payload = json.dumps(payload1)
            yield scrapy.Request(url=self.url, method='POST', body=payload, headers=self.headers,
                                 callback=self.further_parse, meta={'event':event,'fight':fight})

    def further_parse(self, response):
        print(" Lets print its further values. ")
        data = json.loads(response.text)

        event = response.meta.get('event')
        fight = response.meta.get('fight')
        item = {"Event": event, "Fight": fight, "Bet": None, "BetOnline": None, "BetOnline Move": None,
                "Bovada": None, "Bovada Move": None, "Pinnacle": None, "Pinnacle Move": None,
                "Betway": None, "Betway Move": None, "MyBookie": None, "MyBookie Move": None,
                "BetUS": None, "BetUS Move": None, "SXBet": None, "SXBet Move": None,
                "Jazz": None, "Jazz Move": None, "Cloudbet": None, "Cloudbet Move": None,
                "Unibet": None, "Unibet Move": None, "DraftKings": None, "DraftKings Move": None,
                "FanDuel": None, "FanDuel Move": None, "BetAnySports": None, "BetAnySports Move": None}

        cat = dict()
        for category in data['data']['sportsbooks']['edges']:
            Name = category.get('node').get('shortName')
            id = category.get('node').get('id')
            cat[f"{id}"] = Name

        for BET in data['data']['fightPropOfferTable']['propOffers']['edges']:#[1:]:

            bet_name1 = BET.get('node').get('propName1')
            bet_name2 = BET.get('node').get('propName2')

            # Assign the value to the specified fields
            for field in self.fields_to_assign:
                item[field] = None
            for bet1 in BET.get('node').get('offers').get('edges'):
                item['Bet'] = bet_name1
                name_id = bet1['node']['sportsbook']['id']
                name = cat[f'{name_id}']
                item[name] = bet1['node']['outcome1']['odds']
                movec = bet1['node']['outcome1']['odds']
                movep = bet1['node']['outcome1']['oddsPrev']
                if movep:
                    if movec > movep:
                        item[f"{name} Move"] = 1
                    elif movec == movep:
                        item[f"{name} Move"] = 0
                    elif movec < movep:
                        item[f"{name} Move"] = -1
                else:
                    item[f"{name} Move"] = 0
            self.count += 1
            print(self.count, item)  # Yield here
            yield item


            # Assign Empty value to the specified fields
            for field in self.fields_to_assign:
                item[field] = None
            for bet2 in BET.get('node').get('offers').get('edges'):
                item['Bet'] = bet_name2
                name_id = bet2['node']['sportsbook']['id']
                name = cat[f'{name_id}']
                if bet2['node']['outcome2']:
                    item[name] = bet2['node']['outcome2']['odds']
                    movec = bet2['node']['outcome2']['odds']
                    movep = bet2['node']['outcome2']['oddsPrev']
                    if movep:
                        if movec > movep:
                            item[f"{name} Move"] = 1
                        elif movec == movep:
                            item[f"{name} Move"] = 0
                        elif movec < movep:
                            item[f"{name} Move"] = -1
                    else:
                        item[f"{name} Move"] = 0
            self.count += 1
            # print(self.count, item)  # Yield here
            yield item

#######          CleaningTheGlass
import csv
import time
import scrapy
from scrapy.selector import Selector

class CleaningTheGlass(scrapy.Spider):
    name = 'CleaningTheGlass'
    url = "https://cleaningtheglass.com/stats/team/{}/gamelogs"
    headers = {
        'authority': 'cleaningtheglass.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cookie': 'wordpress_logged_in_cfb45adfd4102bd74a046b78d76db012=bryce612893%7C1742166567%7CzbLjiH6eGjvPdWzgRusENyjmyUrazJHWmxQSa2oUsPA%7C502989c199986b12e8ca1d206b595ae5c2428623bd2f59eb147e6dff63700027; '
                  'sessionid=0oppks7uofuop9t5okfelw0gve0n3h7b; '
                  'csrftoken=nGIByj7eUrVwY0IUsPH85EU2LJdCJD1FNBHp3ShUz6ZoYkfaRbdVMdBfrCo2xHox',
        'referer': 'https://cleaningtheglass.com/stats/team/1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    custom_settings = {
            'FEED_URI': 'Output/CleaningtheGlass Record.csv',
            'FEED_FORMAT': 'csv',
            'FEED_EXPORT_ENCODING': 'utf-8-sig',
        }

    def start_requests(self):
        team_count = 1
        yield scrapy.Request(url=self.url.format(team_count), headers=self.headers, callback=self.parse,
                             meta={'team_count':team_count})

    def parse(self, response):
        keys = [
            'Team','Category', 'Date', 'vs', 'Opp', 'Game Result', 'Team Pts', 'Opp Pts', 'Spread', 'eFG #', 'eFG %',
            'Rim #', 'Rim %', 'Short Mid #', 'Short Mid %', 'Long Mid #', 'Long Mid %', 'All Mid #', 'All Mid %',
            'Corner Three #', 'Corner Three %', 'Non Corner #', 'Non Corner %','All Three #', 'All Three %',
            'Pts/Poss %', 'Pts/Poss #', 'ALL TRANSITION Pts+/Poss %', 'ALL TRANSITION Pts+/Poss #',
            'ALL TRANSITION Freq #', 'ALL TRANSITION Freq %', 'ALL TRANSITION Pts/Poss %', 'ALL TRANSITION Pts/Poss #',
            'OFF STEALS Pts+/Poss %', 'OFF STEALS Pts+/Poss #', 'OFF STEALS Freq #', 'OFF STEALS Freq %',
            'OFF STEALS Pts/Poss %', 'OFF STEALS Pts/Poss #','OFF LIVE REBOUNDS Pts+/Poss %', 'OFF LIVE REBOUNDS Pts+/Poss #',
            'OFF LIVE REBOUNDS Freq #', 'OFF LIVE REBOUNDS Freq %', 'OFF LIVE REBOUNDS Pts/Poss %', 'OFF LIVE REBOUNDS Pts/Poss #'
        ]
        team_abbreviations = {
            "ATLANTA": "ATL", "BOSTON": "BOS", "BROOKLYN": "BRK", "CHARLOTTE": "CHO",
            "CHICAGO": "CHI", "CLEVELAND": "CLE", "DALLAS": "DAL", "DENVER": "DEN",
            "DETROIT": "DET", "GOLDEN STATE": "GSW", "HOUSTON": "HOU", "INDIANA": "IND",
            "LA CLIPPERS": "LAC", "LA LAKERS": "LAL", "MEMPHIS": "MEM", "MIAMI": "MIA",
            "MILWAUKEE": "MIL", "MINNESOTA": "MIN", "NEW ORLEANS": "NOP", "NEW YORK": "NYK",
            "OKLAHOMA CITY": "OKC", "ORLANDO": "ORL", "PHILADELPHIA": "PHI", "PHOENIX": "PHO",
            "PORTLAND": "POR", "SACRAMENTO": "SAC", "SAN ANTONIO": "SAS", "TORONTO": "TOR",
            "UTAH": "UTA", "WASHINGTON": "WAS"
        }

        # team_fullname = response.xpath("//*[contains(@class, 'tab-current-label tab-select-header team-name-select-header')]/span[contains(@class,'hidden-mobile')]/text()").get('').strip()
        team = ''
        team_name = response.xpath("//*[contains(@class, 'tab-current-label tab-select-header team-name-select-header')]/span[contains(@class,'visible-mobile')]/text()").get('').strip()
        if team_name in team_abbreviations:
            team = team_abbreviations[team_name]

        '''     1        Offense > Shooting Frequency                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_offense_shooting_frequency')]/tbody/tr"):
            item['Category'] = 'Offense: Shooting Frequency'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['eFG #'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['eFG %'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['Rim #'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['Rim %'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['Short Mid #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['Short Mid %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['Long Mid #'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['Long Mid %'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['All Mid #'] = data.css('td:nth-child(17) ::text').get('').strip()
            item['All Mid %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['Corner Three #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['Corner Three %'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['Non Corner #'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['Non Corner %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['All Three #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['All Three %'] = data.css('td:nth-child(24) ::text').get('').strip()
            yield item

        '''      2       Offense > Shooting Accuracy                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_offense_shooting_accuracy')]/tbody/tr"):
            item['Category'] = 'Offense: Shooting Accuracy'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['eFG #'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['eFG %'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['Rim #'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['Rim %'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['Short Mid #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['Short Mid %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['Long Mid #'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['Long Mid %'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['All Mid #'] = data.css('td:nth-child(17) ::text').get('').strip()
            item['All Mid %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['Corner Three #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['Corner Three %'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['Non Corner #'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['Non Corner %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['All Three #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['All Three %'] = data.css('td:nth-child(24) ::text').get('').strip()
            yield item

        '''      3      Offense > Play Context: Transition                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_offense_transition')]/tbody/tr"):
            item['Category'] = 'Offense: Play Context: Transition'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['Pts/Poss %'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['Pts/Poss #'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['ALL TRANSITION Pts+/Poss %'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['ALL TRANSITION Pts+/Poss #'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['ALL TRANSITION Freq #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['ALL TRANSITION Freq %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['ALL TRANSITION Pts/Poss %'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['ALL TRANSITION Pts/Poss #'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['OFF STEALS Pts+/Poss %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['OFF STEALS Pts+/Poss #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['OFF STEALS Freq #'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['OFF STEALS Freq %'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['OFF STEALS Pts/Poss %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['OFF STEALS Pts/Poss #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts+/Poss %'] = data.css('td:nth-child(25) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts+/Poss #'] = data.css('td:nth-child(26) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Freq #'] = data.css('td:nth-child(27) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Freq %'] = data.css('td:nth-child(28) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts/Poss %'] = data.css('td:nth-child(29) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts/Poss #'] = data.css('td:nth-child(30) ::text').get('').strip()
            yield item

        '''      4       Defense > Shooting Frequency                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_defense_shooting_frequency')]/tbody/tr"):
            item['Category'] = 'Defense: Shooting Frequency'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['eFG #'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['eFG %'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['Rim #'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['Rim %'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['Short Mid #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['Short Mid %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['Long Mid #'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['Long Mid %'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['All Mid #'] = data.css('td:nth-child(17) ::text').get('').strip()
            item['All Mid %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['Corner Three #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['Corner Three %'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['Non Corner #'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['Non Corner %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['All Three #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['All Three %'] = data.css('td:nth-child(24) ::text').get('').strip()
            yield item

        '''      5       Defense > Shooting Accuracy                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_defense_shooting_accuracy')]/tbody/tr"):
            item['Category'] = 'Defense: Shooting Accuracy'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['eFG #'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['eFG %'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['Rim #'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['Rim %'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['Short Mid #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['Short Mid %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['Long Mid #'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['Long Mid %'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['All Mid #'] = data.css('td:nth-child(17) ::text').get('').strip()
            item['All Mid %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['Corner Three #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['Corner Three %'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['Non Corner #'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['Non Corner %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['All Three #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['All Three %'] = data.css('td:nth-child(24) ::text').get('').strip()
            yield item

        '''      6       Defense > Play Context: Transition                '''
        item = {key: '' for key in keys}
        item["Team"] = team
        for data in response.xpath("//*[contains(@id,'team_game_log_defense_transition')]/tbody/tr"):
            item['Category'] = 'Defense: Play Context: Transition'
            item['Date'] = data.css('td:nth-child(1) a::text').get('').strip()
            item['vs'] = data.css('td:nth-child(2) ::text').get('').strip()
            item['Opp'] = data.css('td:nth-child(3) a::text').get('').strip()
            item['Game Result'] = data.css('td:nth-child(4) ::text').get('').strip()
            item['Team Pts'] = data.css('td:nth-child(5) ::text').get('').strip()
            item['Opp Pts'] = data.css('td:nth-child(6) ::text').get('').strip()
            item['Spread'] = data.css('td:nth-child(7) ::text').get('').strip()
            item['Pts/Poss %'] = data.css('td:nth-child(8) ::text').get('').strip()
            item['Pts/Poss #'] = data.css('td:nth-child(9) ::text').get('').strip()
            item['ALL TRANSITION Pts+/Poss %'] = data.css('td:nth-child(11) ::text').get('').strip()
            item['ALL TRANSITION Pts+/Poss #'] = data.css('td:nth-child(12) ::text').get('').strip()
            item['ALL TRANSITION Freq #'] = data.css('td:nth-child(13) ::text').get('').strip()
            item['ALL TRANSITION Freq %'] = data.css('td:nth-child(14) ::text').get('').strip()
            item['ALL TRANSITION Pts/Poss %'] = data.css('td:nth-child(15) ::text').get('').strip()
            item['ALL TRANSITION Pts/Poss #'] = data.css('td:nth-child(16) ::text').get('').strip()
            item['OFF STEALS Pts+/Poss %'] = data.css('td:nth-child(18) ::text').get('').strip()
            item['OFF STEALS Pts+/Poss #'] = data.css('td:nth-child(19) ::text').get('').strip()
            item['OFF STEALS Freq #'] = data.css('td:nth-child(20) ::text').get('').strip()
            item['OFF STEALS Freq %'] = data.css('td:nth-child(21) ::text').get('').strip()
            item['OFF STEALS Pts/Poss %'] = data.css('td:nth-child(22) ::text').get('').strip()
            item['OFF STEALS Pts/Poss #'] = data.css('td:nth-child(23) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts+/Poss %'] = data.css('td:nth-child(25) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts+/Poss #'] = data.css('td:nth-child(26) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Freq #'] = data.css('td:nth-child(27) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Freq %'] = data.css('td:nth-child(28) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts/Poss %'] = data.css('td:nth-child(29) ::text').get('').strip()
            item['OFF LIVE REBOUNDS Pts/Poss #'] = data.css('td:nth-child(30) ::text').get('').strip()
            yield item

        ''' NEXT TEAM TO BE CALLED FROM HERE    '''
        selector = Selector(response)
        options = selector.xpath('//select[@id="team-name-select-desktop"]/option')
        Total_teams = len(options)
        team_count = response.meta.get('team_count')
        if team_count < Total_teams:
            team_count += 1
            yield scrapy.Request(url=self.url.format(team_count), headers=self.headers, callback=self.parse,
                                 meta={'team_count':team_count})

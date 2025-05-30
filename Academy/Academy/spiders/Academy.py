import json
import scrapy

class AcademySportsOutdoors(scrapy.Spider):
    name = 'AcademySportsOutdoors'
    url = "https://www.academy.com/"
    prefix = 'https://www.academy.com'
    handle_httpstatus_list = [403]
    headers = {
        'authority': 'www.academy.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'USERTYPE=G; akamai_ch=A; isBarcodeScannerV2=true; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; klarnaTender=true; dMOnQV=true; ACADEMY_PLCC_USER=true; enableCheckoutSignInOtp=true; akacd_www_pr=3863685326~rv=82~id=28ce3b557171ad51688d59eaa5667e57; rxVisitor=16862325296572OTMI9NFFFVRMNG02S6DEQSB5J5PRIDB; _ALGOLIA=anonymous-26551303-bdc7-451a-a495-7f3ccf4bd7a4; dtCookie=v_4_srv_10_sn_Q6DFJNQINOECB9VNHGS9R3M8MQOU4L2B_perc_100000_ol_0_mul_1_app-3Ac941cf92b69f2e35_0; __utmzz=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; popularSearches=["soccer cleats","nike","yeti","cooler","gun safe"]; s_fid=71067D81CE76CFEF-17CCA71D96056965; s_cc=true; pxcts=2cb04268-0604-11ee-aaed-664845737059; _pxvid=2cb03431-0604-11ee-aaed-d5034527372a; __ogfpid=d1062c0f-0566-4e36-9186-090bd9526fc1; xdVisitorId=139EkpRQaJ08QnncQVpxi8wy3H0aRSKvM6Ddhpo4nKwpcog906E; atgRecVisitorId=139EkpRQaJ08QnncQVpxi8wy3H0aRSKvM6Ddhpo4nKwpcog906E; channel=-; ACC_USER=false; contentstack=true; LAT_LONG=33.70,73.17; bm_mi=21A444FFC529BD91C04D3BD1D77F09CD~YAAQ9fAoF6nYN4+IAQAAvHNSmxRh0FbDzJUSoL6oAoALWEayP8OQg4CaCHP69suKA2A9h0bUCHKh6pSx6eaw9c41C7OnhS9hExPYY+lgr7dzAmFDIj3m3laKiRu6RxbY+0CZuWveUYI/2xzd2CbSQ9+qS9VdoruDIB2pbva9zx3q1awyOjh29epagDPamhfNmyjOCxqUb73A4Ywq/VgVSw7T0Xj1QsBCvKXIShmRLVgGGS5Bm04NZVzDpX35th5/mMz+kWDstNQclR7D0SoppR4XNwpAiqr8IgW/T7NYpI/GaXu65Bxp1xLhqJo7NptLDzThjaOkBojZM+g=~1; bm_sv=9AD904DC7E45109EEAB142E3BDDED300~YAAQ9fAoF63ZN4+IAQAAI5BSmxQecEnitmM1GYyEg3q3TRDuBSUAu+xi/j7+9z318lxJRUAuuoNH867/3xZOf6fjKtST0GxDS4m4mKToRkke+HamqZksluV8v4jVbvTjsw7ixXMin/BYMVJn/6ec0mudXlFS5uld8RTOK9rNnCJVvNJCnoHQSrd2FUSIXt2Q4LK4WCeRzZCuOLPXcvQNycDTwI4gGmjZQjyBognSue/LKTn1TYPFMnSkjdV7caeVTjs=~1; ak_bmsc=49A3872966295193AAB8963B5AB72959~000000000000000000000000000000~YAAQ9fAoFwXgN4+IAQAAoPJSmxTcQwqi8A1rgMn3Rv37PH2d2VdnwYtmOzFC8drDbACywGDBRcOUWxNdZZNdaXWLYn7CiBimhEpPZYBbTO39vSLNxrO7kF26HKZZ6T8p+VYdOgm7lu7bsYZS644CLsGQkeSjrXPAXFl8KB2/AhoSJCAdnYGl6RAkfObP6ZQwnRP9NTtVdq3XPcws3Yb6sdRXviSDW9lJ389i4PVbd0g9nJ9X9651DVUtak23XTp4PdLD7NSfEN4cTcqahDmkuYBNgXLiU7aylIvDxSDRHNTOIyZSHomtuZOOhJZ8Y/6/eoILbBsAahK4bgz8tHzivuWhZ4GonyDFp2KLyoishB8fEcKEEcIQU9vidZGdzudmOaqlGTV9YoDjeJrYUNigvg04ITqHc1bcWSEviNmaHRTx50zSNc5q2HRJFEA=; BVBRANDID=ac668c48-80ec-4007-8cd0-13a026f35ae2; BVImplmain_site=9102; rxvt=1686237371993|1686235571993; correlationId=AA-rwf0dk1lu1Iu35fh2xTwzLt5Up1lluyR; session_expiry=asosession; JSESSIONID=0000xK_JApOTXD4wqHg5pTKMBDh:1cab4qrpk; s_inv=2132; s_vnc365=1717771576975%26vn%3D2; s_ivc=true; atgRecSessionId=c-ebeQpqnHBZVwPgIMXZyL8Doqmtc998H9DhrXytgKbzzIEzyNKf!1505962530!-1671225262; BVBRANDSID=442a9841-3cb5-46b0-8856-edac532d04f9; dtPC=10$235571978_380h1p10$235619323_76h1p10$235703161_599h1p10$235755448_707h1p10$235813765_432h1p10$235830063_76h1p10$235846650_376h1p10$236089822_187h1p10$236113916_492h1vFDTUFKMVFAEJNPHMJFUVUHKUQRRFENRJ-0e0; s_nr30=1686236123707-Repeat; s_nr365=1686236123711-Repeat; s_tslv=1686236123728; _px3=811449c9c2874a788c215498a14e811b15970284b603dbea683e9aefb1f309b3:I+505qjtV+iZ2sKC04prFGv9tBBlL1uvP6zBGWLra32gDuM+JAqjP5ndeoOL9xjK4kYL81YE7ZPQ9MSV8wwZiQ==:1000:/nf1jfOIWeXgNVnTCtl3xtJmZ2FrbFDOBooDLBWNW2bd8s244fPIXvxZKCw2wRZavd40zjonjNdctCcaigm4058RGgTQsru+7sIrnrpyK0a4hXgE2p+71t+6/wGEIXnF9hRYzHnY51XAKT8KZVJCjpLEowguOEkVRI1pwOuKLOks3fG3adHLm9oslzSUPj+vVUu56vuGzD/lK51Ttl2WqQ==; s_ips=293; s_sq=academyglobal%3D%2526c.%2526a.%2526activitymap.%2526page%253Dmens%252520%25257C%252520academy%2526link%253DRight%252520Arrow%2526region%253DproductGrid%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dmens%252520%25257C%252520academy%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.academy.com%25252Fc%25252Fmens%25253Fpage_2%2526ot%253DA; utag_main=v_id:01889b4abad000652481f6ec54cc0506f00180670086e$_n:2$_e:49$_s:0$_t:1686238112110$_revpage:%2Fc%2Fmens%7Cplp%7Cloadnextrow%3Bexp-1686239912118$vapi_domain:academy.com$ses_id:1686235576234%3Bexp-session$_n:9%3Bexp-session$academy_visitorId:guest%3Bexp-session$dc_visit:1$dc_event:9%3Bexp-session; s_tp=4748; s_ppv=mens%2520%257C%2520academy%2C97%2C6%2C4592%2C2%2C16; akavpau_wd=1686236927~id=8c23402199e6ef38e6e85ee148b0fd53; bm_sv=9AD904DC7E45109EEAB142E3BDDED300~YAAQL/V0aEmxnpqIAQAAFbxRmxSJjx/2b2Ixf7YYmr1gejDf8B6WdzIA8OT+hMO9sc2nBgPBm4GdZLuR8E6tFqJEuEd6UL4UGJLrouZQhKc0zzM4WftX0AM+yXyTV5wvfFZh6x2Fc+2WTojQM4YRVbKjev9uMezj7GTjgLwRdUqMABwa8pDy36Kgmj73Dt9KuVEULi+5WILZ4wV5UBsb+Z72qJX3ypo+Um29vfojVOfPMVknTIbliR1R3F+D6M8bdTs=~1; akavpau_wd=1686237074~id=c96fd412c890550ced464cd2999c5f9f; dMOnQV=true; enableCheckoutSignInOtp=true; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; isBarcodeScannerV2=true; klarnaTender=true',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    custom_settings = {
        'FEED_URI': 'Academy.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    api_url = "https://www.academy.com/api/category/v2/{}" \
              "?web=true&displayFacets=true&recordsPerPage=23&orderBy=topSeller&pageNumber={}"
    api_headers = {
        'authority': 'www.academy.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        # 'cookie': 'USERTYPE=G; akamai_ch=A; isBarcodeScannerV2=true; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; klarnaTender=true; dMOnQV=true; ACADEMY_PLCC_USER=true; enableCheckoutSignInOtp=true; akacd_www_pr=3863685326~rv=82~id=28ce3b557171ad51688d59eaa5667e57; ak_bmsc=49A3872966295193AAB8963B5AB72959~000000000000000000000000000000~YAAQLO8uFwW8HY+IAQAA3HhKmxSrFot9dnowooDZrYWoy/HwjHXuHXqAUoFnw6VOh2hzUy9EFVomyoa90PDAQoQScb+wyB+D17OVGxlZH4Bn0yo5oVfXaR1yXbH+01vZTxcoTLr5PhnB3BgrezfewJvhCnUww9gbF1LFj/Kn+CYa/1RbSxqAXa3p34Tx2T4YztImyVU/IcE1gIrQih7lzHccO/WGeShl4NFRsju3NhGftxZM0lnRXFy69hM03N+a3zopS9DYI6ZRS+INFCeVmtgD7MmXFEJvk7DOnM0J//Stb1FuHq+R9bKVSbNbiPQEGSR9IFCgqT400whVNTZ1jqbgcZ57/YE8BkNTwaxzmmQmV82inv9MYxJZUhxAfLcrW1XXqhXg8DP4; rxVisitor=16862325296572OTMI9NFFFVRMNG02S6DEQSB5J5PRIDB; rxvt=1686234329660|1686232529660; _ALGOLIA=anonymous-26551303-bdc7-451a-a495-7f3ccf4bd7a4; dtCookie=v_4_srv_10_sn_Q6DFJNQINOECB9VNHGS9R3M8MQOU4L2B_perc_100000_ol_0_mul_1_app-3Ac941cf92b69f2e35_0; correlationId=AA-Re10EjmBbfKlSO5pKUvIlcAFHhOmLUQw; session_expiry=asosession; JSESSIONID=0000IR_W3Y0dM2cgKSYgVF6dB1E:1cab4qrpk; __utmzz=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; popularSearches=["soccer cleats","nike","yeti","cooler","gun safe"]; s_inv=0; s_vnc365=1717768548915%26vn%3D1; s_ivc=true; s_fid=71067D81CE76CFEF-17CCA71D96056965; s_cc=true; pxcts=2cb04268-0604-11ee-aaed-664845737059; _pxvid=2cb03431-0604-11ee-aaed-d5034527372a; __ogfpid=d1062c0f-0566-4e36-9186-090bd9526fc1; xdVisitorId=139EkpRQaJ08QnncQVpxi8wy3H0aRSKvM6Ddhpo4nKwpcog906E; atgRecVisitorId=139EkpRQaJ08QnncQVpxi8wy3H0aRSKvM6Ddhpo4nKwpcog906E; channel=-; ACC_USER=false; contentstack=true; LAT_LONG=33.70,73.17; atgRecSessionId=cxqbTWYAXkpy-q9fuCVGmh4FLBXgvlYXQ01BYHMyDMo4i7c3Mrso!1505962530!-1671225262; bm_mi=21A444FFC529BD91C04D3BD1D77F09CD~YAAQLggQAtZ1fm+IAQAAsgxPmxRtSPIbd5nA9vbdbPi/HfXFi4ebqtDIJIPBLPLlankwPhRmvsFpwyAsUJLtPISJ8OYi05kRXw2q2aiCkMWxCzLi9hKZUMnOOPq4lLWb0i6BG4KxW8bSrVH7Qz23UcfqoVnWgRAaq2vPCqx/fFs3uWHb3GZu9DT+SrhKNUg6FnePUEqU9d3LbjFRGpOORAGyMo8Mt/0TwkS6XSIrl7JsjzPRaTAyNw3h21WkzMwlZNwpqQ7fzeH0yk43zeQqqNDi1lYzg59F8TeCWD+iCEm1DQpkjX9ut6EddX8Puhg=~1; dtPC=10$232529640_299h1p10$232659045_616h1p10$232660548_547h1p10$232716056_825h1p10$232720485_59h1p10$232721311_279h1p10$232829761_882h1p10$232834273_716h1vHNONNTGCBLMJDIVVLSUMBMHGAIPUMHKF-0e0; s_nr30=1686232841780-New; s_nr365=1686232841781-New; s_tslv=1686232841789; _px3=9ce0b8a57c26a269dbb06755e086396377a58c96f0fab43f49edc674d4ad5b18:/fGPNSoi010YQnntiUFfWr6/GLFX3JMPMU0kjCR+6hsQK3ukXMGTuGiO39UGIOiFxBbGOcXbaES38NEEJnW91Q==:1000:cMxQ3NG5a/vRUyLuvSjc9RcA0pxJt0R/NczjZx8AMi4Bvz70PzCt2eCt22TcSq0Nd3psBtUgDRIWCAfUTYeR7n9CfjQfziL9e5mzdjqM8vkyt2PAPZ/LHbO7Ro9nD6knoqOqReEH0cJ+NCk48a0bSL+uK8MbpYtoHTr9Ca8StlfLU18ulWR7FkYJgrvc6+ebe0j89AlBSpcfT82IKN+VVA==; utag_main=v_id:01889b4abad000652481f6ec54cc0506f00180670086e$_n:1$_e:24$_s:0$_t:1686234724314$ses_id:1686232546002%3Bexp-session$_n:8%3Bexp-session$academy_visitorId:guest%3Bexp-session$_revpage:%2Fc%2Fshops%2Fsale%7Cplp%7Cloadnextrow%3Bexp-1686236524324$vapi_domain:academy.com; s_ips=4040; s_tp=4793; akavpau_wd=1686233525~id=1da5f0a7e7bfb81fe7e56665419881a1; s_ppv=sale%2520%257C%2520academy%2C100%2C84%2C4793%2C20%2C20; bm_sv=9AD904DC7E45109EEAB142E3BDDED300~YAAQ9fAoF4K7N4+IAQAAFIZQmxQIMmnCpKQYIC+iV9awpOPOrNRGDS9LWP1BjHvAVzVGYkUQhzDwYDp0zlG5Y3GaKSiPOsMjG01UMSrzd8LkxT59w01yEdjqdlHQj3VGMsztklCk/FQq3RwbCzcJ926pzknfTIsTNNI+DoRbRzs3RXX+yp4Z1hTWsVdj5N5jXD15Wul6S5fFAMzEv062ktdwYAe9oVhgKxxme5UU/O5JvPqeLeGmjfjGb9W0m4jZQU4=~1; s_sq=academyglobal%3D%2526c.%2526a.%2526activitymap.%2526page%253Dsale%252520%25257C%252520academy%2526link%253D2%2526region%253DproductGrid%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dsale%252520%25257C%252520academy%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.academy.com%25252Fc%25252Fshops%25252Fsale%25253Ficid%25253Dhp_fc_mac_50poff%252526page_2%2526ot%253DA; bm_sv=9AD904DC7E45109EEAB142E3BDDED300~YAAQL/V0aEmxnpqIAQAAFbxRmxSJjx/2b2Ixf7YYmr1gejDf8B6WdzIA8OT+hMO9sc2nBgPBm4GdZLuR8E6tFqJEuEd6UL4UGJLrouZQhKc0zzM4WftX0AM+yXyTV5wvfFZh6x2Fc+2WTojQM4YRVbKjev9uMezj7GTjgLwRdUqMABwa8pDy36Kgmj73Dt9KuVEULi+5WILZ4wV5UBsb+Z72qJX3ypo+Um29vfojVOfPMVknTIbliR1R3F+D6M8bdTs=~1; akavpau_wd=1686233605~id=6294eb51c2fb42763a6c55ee180221bc; dMOnQV=true; enableCheckoutSignInOtp=true; enablePriceRangeAttributes=true; enableShowPriceSwatch=true; isBarcodeScannerV2=true; klarnaTender=true',
        # 'referer': 'https://www.academy.com/c/shops/sale?icid=hp_fc_mac_50poff&page_2',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        count=1
        for category in response.xpath("//*[contains(@class, 'me-4 text-decoration-none')]"):   #[:1]:
            category_url = category.css('::attr(href)').get('')
            if category_url:
                print(count,':',self.prefix+category_url)
                count=count+1
                yield response.follow(url=category_url, callback=self.category_page, headers=self.headers)

    def category_page(self, response):
        code = response.xpath("//*[contains(@class, 'container bvSpotlight pb-3 text-center position-relative')]//"
                              "div[contains(@data-bv-show, 'spotlights')]/@data-bv-subject-id").get('')
        updated_code = code.replace('SL-','')
        if updated_code:
            print('Updated SL using html: ',updated_code)
            yield response.follow(url=self.api_url.format(str(updated_code),'1'), headers=self.api_headers,
                              callback=self.listing_parse, meta={'updated_code': updated_code})

    def listing_parse(self, response):
        updated_code = response.meta['updated_code']
        data = json.loads(response.body)

        for result in data['hits']:
            if result.get('name') is not None:
                item = dict()
                item['Name'] = result.get('name','').strip()
                item['Brand'] = result.get('facet_Brand','')
                item['Max-Price'] = result.get('maxProductPrice','')
                item['Min-Price'] = result.get('minProductPrice','')
                item['Rating'] = result.get('averageRating','')
                item['Promo_Msg'] = result.get('promoMessage','')

                for variant in result.get('industrySubGroup_ImageSku'):
                    if variant is not None:
                        item['Image url'] = variant.get('image','')
                        item['Color'] = variant.get('color','')
                        item['Identifier'] = variant.get('skuIdentifier','')
                        yield item

        page = data['page']
        total_pages = data['nbPages']
        if page<total_pages:
            yield response.follow(url=self.api_url.format(updated_code,str(page+1)),headers=self.api_headers,
                                  callback=self.listing_parse, meta={'updated_code': updated_code})












































'''
        url = 'https://www.academy.com/c/shops/sale?icid=hp_fc_mac_50poff&page_2'
        html_text = requests.get(url).text

        data = re.search(r'window\.__WEB_CONTEXT__=(.*?});', html_text).group(1)
        # data = data.replace('pageManifest', '"pageManifest"')
        data = json.loads(data)
        print(data)
'''

'''
        mp4 = re.compile(r"(?<=mp4:\s\[')(.*)'\]")
        print(mp4.findall(text)[0])
        
'''

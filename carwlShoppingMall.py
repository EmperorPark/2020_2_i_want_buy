import sys
if __name__ == '__main__':
    print ('직접실행불가')
    sys.exit(0)

import requests
from bs4 import BeautifulSoup
import json
import time

import utils

class CarwlShoppingMall:

    def getGoodsPurchaseAvailableByURL(self, site_url):
        ''' 상품 구매 가능여부 사이트별 라우팅 함수'''
        rtn_str = ''
        if 'http'.lower() not in site_url.lower():
            rtn_str = '사이트 URL에는 http:// 혹은 https:// 가 포함되어야 합니다.'
        elif 'coupang.com'.lower() in site_url.lower():
            rtn_str = self.getGoodsPurchaseAvailableByURLFromCoupang(site_url) + '\n'
        elif 'ssg.com'.lower() in site_url.lower():
            rtn_str = self.getGoodsPurchaseAvailableByURLFromSSG(site_url) + '\n'
        else:
            rtn_str = '!!!예외: site 불명확({}),  상품 구매 가능여부 확인 미실행'.format(site_url) + '\n'
            print(rtn_str)
        
        return '\n' + rtn_str

    def getGoodsPurchaseAvailableByURLFromCoupang(self, site_url):
        '''쿠팡 URL의 상품 구매 가능 확인 함수'''
        rtn_str = ''
        print('===================쿠팡 URL 확인 시작===================')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://www.coupang.com/',
        }

        url = site_url
        
        response_html = self.webRequest(method='GET', url=url, header_dict=headers)
        
        soup_obj = BeautifulSoup(response_html, "html.parser")
        
        div_sold_out = soup_obj.find("div", {"class": "prod-atf"}).find("div", {"class": "sold-out"})

        buyBtn = soup_obj.find("button", {"class": "prod-buy-btn"})

        if buyBtn != None and div_sold_out == None:
            rtn_str += '구매가능' + '\n'
            print('구매가능')
        else:
            rtn_str += '구매불가' + '\n'
            print('구매불가')
        
        print('===================쿠팡 URL 확인 끝===================')
        return '\n' + rtn_str

    def getGoodsPurchaseAvailableByURLFromSSG(self, site_url):
        '''신세계 URL의 상품 구매 가능 확인 함수'''
        rtn_str = ''
        print('===================신세계 URL 확인 시작===================')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'http://www.ssg.com/',
        }

        url = site_url
        
        response_html = self.webRequest(method='GET', url=url, header_dict=headers)
        
        soup_obj = BeautifulSoup(response_html, "html.parser")
        
        oriCart = soup_obj.find("div", {"id": "oriCart"})

        if oriCart != None:
            actionPayment = oriCart.find("a", {"id":"actionPayment"})
            if actionPayment != None:
                rtn_str += '구매가능' + '\n'
                print('구매가능')
            else:
                rtn_str += '구매불가' + '\n'
                print('구매불가')
        else:
            rtn_str += '구매불가' + '\n'
            print('구매불가')

        print('===================신세계 URL 확인 끝===================')
        return '\n' + rtn_str

    def getGoodsRegisteredBySearch(self, searchWord):
        ''' 상품등록 검색 함수 각 사이트별 검색함수 실행 '''
        rtn_str = ''
        if len(searchWord.split()) < 2:
            rtn_str = '검색어를 2단어 이상 입력해 주세요' + '\n'
            print('검색어를 2단어 이상 입력해 주세요')
            return '\n' + rtn_str
        rtn_str += self.getGoodsRegisteredBySearchFromCoupang(searchWord) + '\n'
        rtn_str += self.getGoodsRegisteredBySearchFromSSG(searchWord) + '\n'
        
        return rtn_str

    def getGoodsRegisteredBySearchFromCoupang(self, searchWord):
        ''' 쿠팡 등록 검색함수 '''
        rtn_str = '===================쿠팡 검색 시작===================' + '\n'
        print('===================쿠팡 검색 시작===================')
        rtn_str += '검색 유사도: (검색어 갯수//2) 이상 포함' + '\n'
        print('검색 유사도: (검색어 갯수//2) 이상 포함')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://www.coupang.com',
        }

        url = "https://www.coupang.com/np/search"
        data = {'component':'',
        'q': searchWord,
        'channel':'user'
        }
        
        keywords = searchWord.split()
        search_dict = self.searchForeignLang(keywords)

        search_list = self.getCombinationSearchResult(search_dict)

        response_html = self.webRequest(method='GET', url=url, header_dict=headers, params_dict=data)
        # with open('StudyScripting/Coupang/result.html', 'w') as file_handle:
        #         file_handle.write(str(response_html))

        # print(response_html)
        soup_obj = BeautifulSoup(response_html, "html.parser")
        
        lis = soup_obj.find("ul", {"id": "productList"}).findAll("li")
        for li in lis:
            product = li.find("div", {"class": "name"})
            em = li.find("em", {"class": "sale"})
            priceStr = ''
            if em != None:
                price = em.find(
                    "strong", {"class": "price-value"}
                )
                priceStr = price.text.strip()
            
            count_tmp = 0
            count = 0
            for each_list in search_list:
                for str in each_list:
                    if str.lower() in product.text.strip().lower():
                        count_tmp += 1
                        # print(str)
                if count_tmp > count:
                    count = count_tmp
                
                # print(count)
                # print('clear')
                count_tmp = 0    
            
            if len(keywords) > 2:
                if count >= len(keywords)//2:
                    rtn_str += "상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr + "\n"
                    print("상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr)
            else:
                if count >= 2:
                    rtn_str += "상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr + "\n"
                    print("상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr)

        rtn_str += '===================쿠팡 검색 끝===================' + '\n'
        print('===================쿠팡 검색 끝===================')
        return '\n' + rtn_str

    def getGoodsRegisteredBySearchFromSSG(self, searchWord):
        '''신세계 등록 검색함수'''
        rtn_str = '===================신세계 검색 시작===================' + '\n'
        print('===================신세계 검색 시작===================')
        rtn_str += '검색 유사도: (검색어 갯수//2) 이상 포함' + '\n'
        print('검색 유사도: (검색어 갯수//2) 이상 포함')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'http://www.ssg.com/',
        }

        url = "http://www.ssg.com/search.ssg"
        data = {'target': 'all',
        'query': searchWord
        }
        
        keywords = searchWord.split()
        search_dict = self.searchForeignLang(keywords)

        search_list = self.getCombinationSearchResult(search_dict)

        response_html = self.webRequest(method='GET', url=url, header_dict=headers, params_dict=data)
        # with open('StudyScripting/Coupang/result.html', 'w') as file_handle:
        #         file_handle.write(str(response_html))

        # print(response_html)
        soup_obj = BeautifulSoup(response_html, "html.parser")
        
        lis = soup_obj.find("ul", {"id": "idProductImg"}).findAll("li")
        for li in lis:
            li_title = li.find("div", {"class": "title"})
            a_title = li_title.find("a")
            product = a_title.find("em", {"class": "tx_ko"})

            li_price = li.find("div", {"class": "opt_price"})
            
            priceStr = ''
            if li_price != None:
                em_price = li_price.find("em", {"class": "ssg_price"})
                priceStr = em_price.text.strip()
            
            count_tmp = 0
            count = 0
            for each_list in search_list:
                for str in each_list:
                    if str.lower() in product.text.strip().lower():
                        count_tmp += 1
                        # print(str)
                if count_tmp > count:
                    count = count_tmp
                
                # print(count)
                # print('clear')
                count_tmp = 0    
            
            if len(keywords) > 2:
                if count >= len(keywords)//2:
                    rtn_str += "상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr + "\n"
                    print("상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr)
            else:
                if count >= 2:
                    rtn_str += "상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr + "\n"
                    print("상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr)

        rtn_str += '===================신세계 검색 끝===================' + '\n' 
        print('===================신세계 검색 끝===================')
        return '\n' + rtn_str
    
    def searchForeignLang(self, keywords):
        '''영어나 왜래어를 왜래어 사전을 통해 영어 또는 한국어로 받아 딕셔너리로 반환'''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://kornorms.korean.go.kr/example/exampleList.do?regltn_code=0003',
        }
        trans = {}

        for keyword in keywords:
            
            url = "https://kornorms.korean.go.kr/example/exampleList.do?regltn_code=0003"
            data = {'example_no':'',
            'example_search_list[0].searchCondition':'all',
            'example_search_list[0].searchEquals':'equal',
            'example_search_list[0].searchKeyword':keyword,
            'allCheck1':'all',
            's_foreign_gubun':'0003',
            '_s_foreign_gubun':'on',
            's_guk_nm':'',
            's_lang_nm':'',
            'pageUnit':'10',
            'pageIndex':'1' }

            response_html = self.webRequest(method='POST', url=url, header_dict=headers, params_dict=data)
            soup_obj = BeautifulSoup(response_html, "html.parser")
            table = soup_obj.findAll("table", {"class": "tableList01"})
            tbody = table[0].findAll("tbody")
            tr = tbody[0].findAll("tr")
            a = tr[0].findAll("a", {"class": "korean"})
            tds = tr[0].findAll("td")
            if utils.isHangul(keyword):
                if len(a) > 0:
                    trans[keyword] = tds[2].text
                else:
                    trans[keyword] = ''
            else:
                if len(a) > 0:
                    trans[keyword] = a[0].text
                else:
                    trans[keyword] = ''
        
        return trans

    def webRequest(self, method, url, header_dict, params_dict={}, is_urlencoded=True):
        """Web Get/Post에 따라 Web request 후 결과를 dictionary로 반환
        이 클래스의 검색 타겟에 맞춰 최적화 함, 범용성 낮음
        """
        res = requests.session() # 세션 유지
        method = method.upper() # 편의 및 통일성을 위해 대문자로 통일
        if method not in ('GET', 'POST'):
            raise Exception('WebRequst Method 비정상: {}'.format(method))
        
        if method == 'GET':
            response = res.get(url=url, headers=header_dict, params=params_dict)
            # response = res.get(url=url, headers=header_dict, params=params_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")
        elif method == 'POST':
            if is_urlencoded is True:
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                response = res.post(url=url, headers=header_dict, data=params_dict)
                # response = res.post(url=url, headers=header_dict, data=params_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")
            else:
                
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/json'
                response = res.post(url=url, data=json.dumps(params_dict), headers=header_dict)
                # response = res.post(url=url, data=json.dumps(params_dict), headers=header_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")

        
        rtn_meta = {'status_code':response.status_code, 'ok':response.ok, 'encoding':response.encoding, 'Content-Type': response.headers['Content-Type']}
        
        if response.ok:
            if 'json' in str(response.headers['Content-Type']):
                return {**rtn_meta, **response.json()}
            elif 'text/html' in str(response.headers['Content-Type']):
                return response.content
            else:
                return {**rtn_meta, **{'text':response.text}}
        else:
            return rtn_meta

    def getCombinationSearchResult(self, dict):
        '''검색어 조합 알고리즘을 수행하여 이차원 리스트로 반환하는 함수'''
        temp_dict = {}
        exclude_key = []
        for key in dict.keys():
            if dict[key] != '':
                temp_dict[key] = dict[key]
            else:
                exclude_key.append(key) 

        keys = list(temp_dict.keys())
        rtn_list = []
        for i in range(2 ** len(temp_dict) -1, -1, -1):
            a = i
            temp_list = []
            cnt = 0
            while cnt < len(temp_dict):
                if temp_dict[keys[cnt]] == '':
                    temp_list.append(keys[cnt])
                else:
                    if a % 2 == 0:
                        temp_list.append(keys[cnt])
                    else:
                        temp_list.append(temp_dict[keys[cnt]])
                a >> 1
                cnt += 1
                
            for key in exclude_key:
                temp_list.append(key)

            rtn_list.append(temp_list)

        return rtn_list


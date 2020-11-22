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
    def __init__(self):
        self.shoppingMallList = []

    def appendShoppingMallList(self):
        """ShoppingMall 목록을 로드한다."""
        self.shoppingMallList = [] # 목록 초기화
        with open('Services/URL_List.txt', 'r') as file_handle:
            line_txt = file_handle.readline()
            self.shoppingMallList.append(line_txt)
        if len(self.shoppingMallList) == 0:
            print ('!!!예외: shoppingMallList 없음. 프로그램 종료')
    
    def getGoodsPurchaseAvailableByURL(self, site):
        if site == 'Coupang':
            self.getGoodsPurchaseAvailableByURLFromCoupang()
        elif site == 'SSG':
            self.getGoodsPurchaseAvailableByURLFromSSG()
        else:
            print('!!!예외: site 불명확({}), getDataBySearch 미실행'.format(site))

    def getGoodsPurchaseAvailableByURLFromCoupang(self):
        print('구현중')

    def getGoodsPurchaseAvailableByURLFromSSG(self):
        print('구현중')

    def getGoodsRegisteredBySearch(self, searchWord):
        if len(searchWord.split()) < 2:
            print('검색어를 2단어 이상 입력해 주세요')
            return
        self.getGoodsRegisteredBySearchFromCoupang(searchWord)
        self.getGoodsRegisteredBySearchFromSSG(searchWord)
        
    def getGoodsRegisteredBySearchFromCoupang(self, searchWord):
        print('===================쿠팡 검색 시작===================')
        print('검색 유사도: 검색어 2개 이상 포함')
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
        search_dict = self.foreignLangSearch(keywords)

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
            
            count = 0
            for each_list in search_list:
                for str in each_list:
                    if str in product.text.strip():
                        count += 1
            
            if count >= 2:
                print("상품명: " + product.text.strip() + " / " + "상품가격: " + priceStr)

        
        print('===================쿠팡 검색 끝===================')



    def getGoodsRegisteredBySearchFromSSG(self, searchWord):
        print('구현중')
    
    def foreignLangSearch(self, keywords):
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

    def webRequest(self, method, url, header_dict, params_dict, is_urlencoded=True):
        """Web Get/Post에 따라 Web request 후 결과를 dictionary로 반환"""
        res = requests.session() # 세션 유지
        method = method.upper() # 편의 및 통일성을 위해 대문자로 통일
        if method not in ('GET', 'POST'):
            raise Exception('WebRequst Method 비정상: {}'.format(method))
        
        if method == 'GET':
            # response = res.get(url=url, headers=header_dict, params=params_dict)
            response = res.get(url=url, headers=header_dict, params=params_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")
        elif method == 'POST':
            if is_urlencoded is True:
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                # response = res.post(url=url, headers=header_dict, data=params_dict)
                response = res.post(url=url, headers=header_dict, data=params_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")
            else:
                
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/json'
                # response = res.post(url=url, data=json.dumps(params_dict), headers=header_dict)
                response = res.post(url=url, data=json.dumps(params_dict), headers=header_dict, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem")

        
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


if __name__ == '__main__':
    print ('직접실행불가')
    exit()

import requests
from bs4 import BeautifulSoup
import json


class carwlShoppingMall:
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
            getGoodsPurchaseAvailableByURLFromCoupang()
        elif site == 'SSG':
            getGoodsPurchaseAvailableByURLFromSSG()
        else:
            print('!!!예외: site 불명확({}), getDataBySearch 미실행'.format(site))

    def getGoodsPurchaseAvailableByURLFromCoupang(self):
        print('구현중')

    def getGoodsPurchaseAvailableByURLFromSSG(self):
        print('구현중')

    def getGoodsRegisteredBySearch(self, site):
        if site == 'Coupang':
            getGoodsRegisteredBySearchFromCoupang()
        elif site == 'SSG':
            getGoodsRegisteredBySearchFromSSG()
        else:
            print('!!!예외: site 불명확({}), getDataBySearch 미실행'.format(site))

    def getGoodsRegisteredBySearchFromCoupang(self):
        print('구현중')

    def getGoodsRegisteredBySearchFromSSG(self):
        print('구현중')

    def webRequest(self, method, url, header_dict, params_dict, is_urlencoded=True):
        """Web Get/Post에 따라 Web request 후 결과를 dictionary로 반환"""
        method = method.upper() # 편의 및 통일성을 위해 대문자로 통일
        if method not in ('GET', 'POST'):
            raise Exception('WebRequst Method 비정상: {}'.format(method))
        
        if method == 'GET':
            responce = requests.get(url=url, headers=header_dict, params=params_dict)
        elif method == 'POST':
            if is_urlencoded is True:
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                response = requests.post(url=url, headers=header_dict, data=params_dict)
            else:
                if 'Content-Type' not in header_dict.keys():
                    header_dict['Content-Type'] = 'application/json'
                response = requests.post(url=url, data=json.dumps(params_dict), headers=header_dict)

        rtn_meta = {'status_code':response.status_code, 'ok':response.ok, 'encoding':response.encoding, 'Content-Type': response.headers['Content-Type']}

        if 'json' in str(responce.headers['Content-Type']):
            return {**rtn_meta, **response.json()}
        elif 'text/html' in str(response.headers['Content-Type']):
            return response.content
        else:
            return {**rtn_meta, **{'text':response.text}}
    


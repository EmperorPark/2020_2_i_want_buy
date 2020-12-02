import sys
from multiprocessing import Process, Queue

import carwlShoppingMall
import teleGramBotManager

def main():
    
    print('=======================================================')
    print('         =======================================       ')
    print('              ========================                 ')
    print('telegram에서 @EmperorPurchaseAvailableBot을 추가하세요!')
    print('              ========================                 ')
    print('         =======================================       ')
    print('=======================================================')

    q = Queue()

    objTeleGramBotManager = teleGramBotManager.TeleGramBotManager(1, q)
    
    # q = Queue()
    # th1 = Process(target=teleGramBotManager.TeleGramBotManager, args=(1, q))
    # th1.start()

    objCarwlShoppingMall = carwlShoppingMall.CarwlShoppingMall()
    
    # 수행 루틴 오토마타
    print('=======================================================')
    print('0: 종료')
    print('1: 상품 등록 확인/상품 판매 확인 선택')
    
    choice = input('실행하고자 하는 번호를 입력해주세요 >> ')
    if choice.isdecimal():
        choice = int(choice)
    else:
        exitErrorInput()


    if choice == 0:
        sys.exit(0)
    elif choice == 1: # 상품 등록 확인/상품 판매 확인 선택
        print('1: 상품 등록 확인')
        print('2: 상품 판매 확인')
        sel = input('실행하고자 하는 번호를 입력해주세요 >> ')
        if sel.isdecimal():
            sel = int(sel)
        else:
            exitErrorInput()
        if sel == 1: # 등록 확인
            print('등록확인 모드(지원 사이트: 쿠팡(www.coupang.com), 신세계(www.ssg.com))')
            print('ex) 아이폰 12 미니 자급제')
            searchWord = str(input('상품 검색(띄어쓰기 구분이 명확할수록 검색 정확도가 높음) >> '))
            objCarwlShoppingMall.getGoodsRegisteredBySearch(searchWord)

        elif sel == 2:
            print('판매확인 모드(쿠팡(www.coupang.com), 신세계(www.ssg.com)), 현재는 PC버전 홈페이지만 지원합니다.')
            print('모바일에서 링크 확인시 쇼핑몰 웹페이지 하단의 pc버전 보기 기능을 이용해 주세요')
            checkurl = str(input('상품 url입력 >> '))
            objCarwlShoppingMall.getGoodsPurchaseAvailableByURL(checkurl)
            
        else:
            print ('오입력이 발생 하였습니다. 다시 수행해주세요')
            sys.exit(0)

    # th1.terminate()

def exitErrorInput():
    print('오입력 발생')
    print('종료')
    sys.exit(0)


if __name__ == '__main__':
    main()
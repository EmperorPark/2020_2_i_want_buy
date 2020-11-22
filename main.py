import sys

import carwlShoppingMall

def main():
    print('telegram에서 EmperorPurchaseAvailableBot을 추가하세요!')
    
    objCarwlShoppingMall = carwlShoppingMall.CarwlShoppingMall()
    
    # 수행 루틴 오토마타
    print('=======================================================')
    print('0: 종료')
    print('1: 상품 등록 확인/상품 판매 확인 선택')
    
    choice = int(input('실행하고자 하는 번호를 입력해주세요 >> '))
    if choice == 0:
        sys.exit(0)
    elif choice == 1: # 상품 등록 확인/상품 판매 확인 선택
        print('1: 상품 등록 확인')
        print('2: 상품 판매 확인')
        sel = int(input('실행하고자 하는 번호를 입력해주세요 >> '))
        if sel == 1: # 등록 확인
            print('등록확인 모드(쿠팡(www.coupang.com), 신세계(www.ssg.com))')
            print('ex) 아이폰 12 미니 자급제 64GB')
            searchWord = str(input('상품 검색(띄어쓰기 구분이 명확할수록 검색 정확도가 높음) >> '))
            objCarwlShoppingMall.getGoodsRegisteredBySearch(searchWord)

        elif sel == 2:
            print('판매확인 모드(쿠팡(www.coupang.com), 신세계(www.ssg.com))')
            checkurl = str(input('상품 url입력 >> '))
            if 'coupang.com' not in checkurl and 'ssg.com' not in checkurl:
                print ('미지원 쇼핑몰입니다. 다시 수행해주세요')
                sys.exit(0)
            
            print ('구현중')
        else:
            print ('오입력이 발생 하였습니다. 다시 수행해주세요')
            sys.exit(0)
    elif choice == 2: # 
        print ('구현중')
    elif choice == 3: # 
        print ('구현중')
    elif choice == 4: # 
        print ('구현중')


if __name__ == '__main__':
    main()
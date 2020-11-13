import sys

import carwlShoppingMall

def main():
    objCarwlShoppingMall = carwlShoppingMall.CarwlShoppingMall()
    
    # 수행 루틴 오토마타
    print('0: 종료')
    print('1: 상품 등록 확인/상품 판매 확인 선택')
    
    choice = int(input('실행하고자 하는 번호를 입력해주세요 >> '))
    if choice == 0:
        sys.exit(0)
    elif choice == 1: # 상품 등록 확인/상품 판매 확인 선택
        sel = int(input('등록 확인시에는 1입력, 판매 확인시에는 2입력 >> '))
        if sel == 1: # 등록 확인
            print('등록확인 모드')
            searchWord = str(input('상품 검색(띄어쓰기 구분이 명확할수록 검색 정확도가 높음) >> '))
            keywords = searchWord.split()
            data = objCarwlShoppingMall.foreignLangSearch(keywords)
            print(data)
            print ('구현중')
        elif sel == 2:
            print('판매확인 모드')
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
# 사고싶다 봇 서버
쇼핑몰(쿠팡, SSG)에서 원하는 상품이 등록되어 있는지, 원하는 상품이 구매가능한지 확인하는 준서버형 프로그램입니다.

크롤링 및 외부 API기반으로 만들어져 사이트 및 API변화에 대응이 바로 안될 수 있습니다.

프로그램을 구동하신 뒤(종료되면 안됨) 텔레그램에서 @EmperorPurchaseAvailableBot(https://t.me/EmperorPurchaseAvailableBot) 을 친구추가 하시고 /help명령의 설명에따라 사용하시면 됩니다.

상품 구매 확인 기능은 PC버전 웹페이지를 입력해야 동작합니다.(모바일 웹페이지 지원 미정)

텔레그램 API키는 암호화 되어 있음으로 해독키가 없으신분들은 자신의 봇을 따로 생성하시고 코드를 수정해서 쓰셔야 합니다.


---
# 환경
작성언어: python

설치 모듈: 

python -m pip install python-telegram-bot --upgrade

이외에는 import나 from문에 따라 그대로 설치하면 됨


실행 테스트: Windows 10 2004(19041.630), python 3.8.3 x64, Anoconda

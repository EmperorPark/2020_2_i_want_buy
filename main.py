import carwlShoppingMall

def main():
    objCarwlShoppingMall = carwlShoppingMall.CarwlShoppingMall()

    keywords = ['iphone', '12', 'mini']
    data = objCarwlShoppingMall.foreignLangSearch(keywords)

    print(data)

if __name__ == '__main__':
    main()
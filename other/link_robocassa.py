import hashlib
from urllib.parse import quote

price = 199
telegram_id = 1868032797
phone = 1236547

def make_hash(price, phone, telegram_id):

    hash_obj = hashlib.md5(f"infsectest_ru:{price}:0'.':qNI1cl89rPWbFMkb9Ls0'.':Shp_phone={phone}:Shp_telegram={telegram_id}".encode())
    return hash_obj.hexdigest()

def get_description(service, price):
    description = f'Оплата за оказание услуги "{service}". Сумма на оплату: {price} рублей'
    result = quote(description, safe='/')
    # result = description.replace(' ', '%20')
    # print(result)
    return result

def make_link(phone, telegram_id):
    # $shp_item = '234234235';
    # $shp_phone = '79522329395';
    # $sum = 1;
    # $desc = urlencode('Тест на взлом: email [sjdhfkjsd@dsfsdad.ru]');
    # echo $md5 = md5('infsectest_ru:'.$sum.':0'.':qNI1cl89rPWbFMkb9Ls0'.':Shp_phone='.$shp_phone.':Shp_telegram='.$shp_item);
    # echo '<br>';
    # echo 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=infsectest_ru&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone='.$shp_phone.'&Shp_telegram='.$shp_item.'&OutSum='.$sum.'&Description='.$desc.'&SignatureValue='.$md5;
    
    # phone = data['phone']
    # telegram_id = data['telegram_id']
    # service = data['service']
    # social_net = data['social_net']
    # link = data['link']

    # final_price = get_final_price(service)
    # price = price
    price = 199
    service = 'Название услуги'
    md5 = make_hash(price, phone, telegram_id)
    description = get_description(service, price)

    # post_data_to_email()
    link_to_pay = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=infsectest_ru&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone='{phone}'&Shp_telegram='{telegram_id}'&OutSum='{price}'.&Description='{description}'.&SignatureValue={md5}"
    return link_to_pay


if __name__ == '__main__':
    res = make_link(phone, telegram_id)
    print(res)
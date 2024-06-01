from yay_automation import Yay
from kukulu import Kukulu #これはこのリポジトリのやつを使ってください
import json
import random
import string
from time import sleep

path="path to 保存するjsonファイル"
パスワード="ランダムでもいいけど僕は統一派"
while True:
    try:
        random_string = ''.join(random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 10))
        kukulu=Kukulu("csrf_token","sessionhash")#詳しい説明はm.kuku.lu generatorをみてください
        newmail=kukulu.specify_address("ここにアドレス@以降")
        yay=Yay()
        yay.register(newmail)
        sleep(1)
        try:
            code=kukulu.check_top_mail(newmail)
        except:
            sleep(3)
            code=kukulu.check_top_mail(newmail)
        token=yay.register_code(code=code,password=パスワード,nickname=random_string,biography="テストgen")
        accounts=json.load(open(path))
        accounts[newmail]=パスワード
        json.dump(accounts, open(path,"w"))
        print(token)
        sleep(1200)#正直何秒がいいかわからないです、これはかなりテキトーな数字
    except Exception as e:
        print(e)
        sleep(1200)
        continue
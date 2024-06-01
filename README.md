# yay-automation
yay!というSNSに使えるAPIラッパー  
WebSocketはないよ (そもそもアカウント大量生産とかいいね爆とかが目的だし、これ)
### >>```pip install yay-automation```<<
## 必須モジュール  
- requests
  
#### アカウントジェネレーターを使う場合
- kukulu.py
## Example.py
```py
from yay_automation import Yay

yay=Yay()
yay.register(email="メールアドレス")
yay.register_code(code="メールされた6桁のコード",password="パスワード",nickname="アカウント名",biography="自己紹介",birth_date="2000-05-02",gender=-1,prefecture="都道府県",referral_code="招待コード？")
yay=Yay(email="メールアドレス",password="パスワード")#,access_token="ベアラートークン",proxy="dict")#これがログイン、トークンをつけるとログインをスキップする
yay.post(text="本文",tags=["リスト、タグ？使ったことない"],choices=["これもリスト","5個まで","選択肢を","設定","できる"],font_size="0",color="0",post_id="返信先のポストID")#本文しか書かなくていい
yay.repost(text="本文",post_id="リポストするポストID",tags=["リスト"])
yay.change_profile(nickname="アカウント名",biography="自己紹介",prefecture="都道府県")
yay.like("いいねするポストのID")
yay.unlike("いいねけすポストのID")
yay.add_to_bookmark("ブックマークするポストのID")
yay.remove_from_bookmark("ブックマークけすポストのID")
yay.report(post_id="通報するポストのID",reason="理由、絶対いるらしい",category_id=0,opponent_id="通報するポスト主のユーザーID")
#↑カテゴリーIDは0～6までそれぞれ、不快なコンテンツ・煽り・暴言=0、スパム=1、他サイトへ誘導・ID交換=2、仕事・勧誘などの業者=3、出会い厨=4、なりすまし・権利侵害=5、その他=6
```  
...書いてある以上のことはないです、ただ必ず要求する引数は少なめ  
## 返り値
ブックマーク消すだけステータスコードで他はdict、でも返り値で重要なものはナッシング  
強いていうなら```.register```とログインの時に返ってくるベアラートークンくらい -> ```print(yay.token)```  
でも有効期限あるしログインを実行すると無限に貰えるのでそこまで重要かは不明
## 他の話
### アカウント作成のレート制限が非常に厳しい
3アカウント作成すると激長レート制限に突入、30分ほどアカウント作成ができなくなる  
### しかもこの時返ってくる値はなんと```IP BANNED```  
書き方悪すぎ、平然と嘘つくんじゃないよ、ほんと  
### VPN / 1部のプライベートプロキシも使用不可
1部のプライベートプロキシもブロックされるガッチガチぶりには驚いた  
正直納得がいくまでアカウントを生産するのは難しそう
### 捨てアドレスで判定されるメールアドレスは使用不可
これはm.kuku.luにて指定アドレスでメアド作成をすれば回避可能 ( もちろん回避できるドメインで )  
まあ、ということはm.kuku.luも自動化しないといけないです
## アカウントジェネレーター
```py
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
```
yay!ジェネレーター用に作ったkukulu.pyがあるのでそれを使ってください  
### [kukuluモジュールの仕様はここから](https://github.com/taka-4602/m.kuku.lu-Generator)
正直検知されないプロキシがないと効率は見込めない、プロキシなしでやるには時間が必要  
これで作ったアカウントたちをfor文とかでまわしていいね爆、荒らし ( 推奨してるわけじゃない ) ができる  
なにかいい案があればいつでも待ってます  
## コンタクト  
Discord サーバー / https://discord.gg/aSyaAK7Ktm  
Discord ユーザー名 / .taka.  

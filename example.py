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
yay.follow("フォローするユーザーのID")
yay.unfollow("フォローけすユーザーのID")
yay.report(post_id="通報するポストのID",reason="理由、絶対いるらしい",category_id=0,opponent_id="通報するポスト主のユーザーID")
#↑カテゴリーIDは0～6までそれぞれ、不快なコンテンツ・煽り・暴言=0、スパム=1、他サイトへ誘導・ID交換=2、仕事・勧誘などの業者=3、出会い厨=4、なりすまし・権利侵害=5、その他=6
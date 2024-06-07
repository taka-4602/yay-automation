import requests
from uuid import uuid4

class YayError(Exception):
    pass
class Yay():
    def __init__(self,email:str=None,password:str=None,access_token:str=None,proxy:dict=None,uuid:str=str(uuid4())):
        self.proxy=proxy
        self.uuid=uuid
        if not access_token:
            if email:
                payload={
                "password":password,
                "uuid":uuid,
                "email":email,
                "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5"
                }
                login=requests.post("https://api.yay.space/v3/users/login_with_email",data=payload,proxies=self.proxy).json()
                if "error_code" in login:
                    raise YayError(login)
                self.access_token=login["access_token"]
        else:
            self.access_token=access_token
    
    def register(self,email:str):
        payload={
            "device_uuid":self.uuid,
            "locale":"ja",
            "intent":"sign_up",
            "email":email
            }
        verification_urls=requests.post("https://api.yay.space/v1/email_verification_urls",data=payload,proxies=self.proxy).json()
        if "error_code" in verification_urls:
            raise YayError(verification_urls)
        signatures=verification_urls["url"].replace("https://idcardcheck.com/apis/v1/apps/yay/","")
        payload={
            "locale":"ja",
            "email":email
            }
        verification_signature=requests.post(f"https://idcardcheck.com/apis/v1/apps/yay/{signatures}",data=payload,proxies=self.proxy).json()
        self.email=email

    def register_code(self,code:str,password:str,nickname:str,biography:str="",birth_date:str="2000-05-02",gender:int=-1,prefecture:str="",referral_code:str=""):
        payload={
            "email":self.email,
            "code":code
            }
        grant_tokens=requests.post("https://idcardcheck.com/apis/v1/apps/yay/email_grant_tokens",data=payload,proxies=self.proxy).json()
        payload={
            "uuid":self.uuid,
            "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5",
            "password":password,
            "email":self.email
            }
        login_with_email=requests.post("https://api.yay.space/v3/users/login_with_email",data=payload,proxies=self.proxy).json()
        if "error_code" in login_with_email:
            raise YayError(login_with_email)
        timestamp=requests.get("https://api.yay.space/v2/users/timestamp",proxies=self.proxy).json()
        payload={
            "prefecture":prefecture,
            "email_grant_token":grant_tokens["email_grant_token"],
            "timestamp":timestamp["time"],
            "uuid":self.uuid,
            #"signed_info":"4d59606254c5881c292308aa7f5d11be",
            "email":self.email,
            "referral_code":referral_code,
            "api_key":"92816834ea82099597f7285db999b4b74496eaf9b7e17007ebaaa8be4eb19ad5",
            #"signed_version":"8TqUP3F1DEj4dWqyYS5hG6WfYnAcj963i3IGmiYsGNI=",
            "profile_icon_filename":"s3\/user_avatar\/2024\/6\/1\/nHLnUTrAL70oaGOL_1717224764_0_size_241x240.jpg",
            #"app_version":"3.35",
            "gender":gender,#未設定-1,男0,女1
            "birth_date":birth_date,
            "password":password,
            "biography":biography,
            "country_code":timestamp["country"],
            "nickname":nickname
            }#コメントは必要なかった部分、なんでだろう
        register=requests.post("https://api.yay.space/v3/users/register",data=payload,proxies=self.proxy).json()
        if "error_code" in register:
            raise YayError(register)
        self.access_token=register["access_token"]
        return register["access_token"]
    
    def report(self,post_id:str,category_id:int,opponent_id:str,reason:str=""):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={
            "reason":reason,
            "category_id":category_id,
            "opponent_id":opponent_id
            }
        report=requests.post(f"https://api.yay.space/v3/posts/{post_id}/report",headers=token,data=payload,proxies=self.proxy).json()
        try:
            if report["result"]!="success":
                raise YayError(report)
        except:
            raise YayError(report)
        return report
    
    def like(self,post_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={
            "post_ids":[
                post_id
                ]
            }
        like=requests.post("https://api.yay.space/v2/posts/like",headers=token,data=payload,proxies=self.proxy).json()
        try:
            if like["result"]!="success":
                raise YayError(like)
        except:
            raise YayError(like)
        return like
    
    def unlike(self,post_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        unlike=requests.post(f"https://api.yay.space/v1/posts/{post_id}/unlike",headers=token,data={},proxies=self.proxy).json()
        try:
            if unlike["result"]!="success":
                raise YayError(unlike)
        except:
            raise YayError(unlike)
    
    def post(self,text:str,tags:list="[]",choices:list=None,font_size:str="0",color:str="0",post_id:str=None):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={
            "color": color,
            "font_size": font_size,
            "message_tags": tags,
            "post_type": "text",
            "text": text,
            "uuid": str(uuid4())
            }
        if choices:
            payload["post_type"]="survey"
            payload["choices"]=choices#["a", "b", "c", "d", "e", "f"] 5個まで
        if post_id:
            payload["in_reply_to"]=post_id
        post=requests.post(f"https://yay.space/api/posts",headers=token,data=payload,proxies=self.proxy).json()
        if post["result"]!="success":
            raise YayError(post)
        return post
    
    def repost(self,text:str,post_id:str,tags:list="[]",font_size:str="0",color:str="0"):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={
            "color": color,
            "font_size": font_size,
            "message_tags": str(tags),
            "post_type": "text",
            "text": text,
            "post_id": post_id
            }
        repost=requests.post(f"https://yay.space/api/posts",headers=token,data=payload,proxies=self.proxy).json()
        if repost["result"]!="success":
            raise YayError(repost)
        return repost
    
    def follow(self,user_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={"userId":user_id}
        follow=requests.post(f"https://api.yay.space/v2/users/{user_id}/follow",headers=token,data=payload,proxies=self.proxy).json()
        try:
            if follow["result"]!="success":
                raise YayError(follow)
        except:
            raise YayError(follow)
        return follow
    
    def unfollow(self,user_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={"userId":user_id}
        unfollow=requests.post(f"https://api.yay.space/v2/users/{user_id}/unfollow",headers=token,data=payload,proxies=self.proxy).json()
        try:
            if unfollow["result"]!="success":
                raise YayError(unfollow)
        except:
            raise YayError(unfollow)
        return unfollow
    
    def change_profile(self,nickname:str,biography:str="",prefecture:str=None):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        payload={
            "nickname": nickname,
            "biography": biography,
            }
        if prefecture:
            payload["prefecture"]=prefecture #都道府県
        cp=requests.post("https://api.yay.space/v3/users/edit",headers=token,data=payload,proxies=self.proxy).json()
        try:
            if cp["result"]!="success":
                raise YayError(cp)
        except:
            raise YayError(cp)
        return cp

    def add_to_bookmark(self,post_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        bookmark=requests.post(f"https://api.yay.space/v1/users/8926797/bookmarks/{post_id}",headers=token,proxies=self.proxy).json()
        return bookmark
    
    def remove_from_bookmark(self,post_id:str,user_id:str):
        token={
            "Authorization":f"Bearer {self.access_token}",
            "X-Device-Info":"Yay 3.39.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36)"
            }
        bookmark=requests.delete(f"https://api.yay.space/v1/users/{user_id}/bookmarks/{post_id}",headers=token,proxies=self.proxy)
        return bookmark.status_code
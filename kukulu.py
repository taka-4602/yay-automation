import requests
from bs4 import BeautifulSoup
import re

#-------------------------------------
#これはyay!アカウントジェネレーター用です
#-------------------------------------

class Kukulu():
    def __init__(self,csrf_token:str=None,sessionhash:str=None,proxy:dict=None):
        self.csrf_token=csrf_token
        self.sessionhash=sessionhash
        self.proxy=proxy
        self.session=requests.Session()
        if csrf_token!=None and sessionhash!=None:
            self.session.cookies.set("cookie_csrf_token",csrf_token)
            self.session.cookies.set("cookie_sessionhash",sessionhash)
            self.session.post("https://m.kuku.lu",proxies=proxy)
        else:
            self.session.post("https://m.kuku.lu",proxies=proxy)
    
    def new_account(self):
        return {"csrf_token":self.session.cookies["cookie_csrf_token"],"sessionhash":self.session.cookies["cookie_sessionhash"]}
    
    def create_mailaddress(self):
        return self.session.get("https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1",proxies=self.proxy).text[3:]
    
    def specify_address(self,address:str):
        return self.session.get(f"https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t=1716696234&csrf_token_check={self.csrf_token}&newdomain={address}",proxies=self.proxy).text[3:]
    
    def check_top_mail(self,mailaddress:str):
        mailaddress=mailaddress.replace("@","%40")
        mails=self.session.get(f"https://m.kuku.lu/recv._ajax.php?&q={mailaddress}&&nopost=1&csrf_token_check={self.csrf_token}",proxies=self.proxy)
        soup=BeautifulSoup(mails.text,"html.parser")
        script=soup.find_all("script")
        match = re.search("(openMailData[^ ]+)", str(script))
        openMailData=match.group()
        openMailData=openMailData.replace("openMailData(","")
        match2=re.findall(f"{openMailData} [^ ]+", str(script))
        maildata=match2[1].split("'")
        mail=self.session.post("https://m.kuku.lu/smphone.app.recv.view.php",data={"num":maildata[1],"key":maildata[3],"noscroll": "1"},proxies=self.proxy)
        soup=BeautifulSoup(mail.text,"html.parser")
        title=soup.find(class_="full").text

        #--------------------------------------------
        #ここの部分は届くメールによってよく変わるから注意
        text=soup.find(style=": 28.13px; margin-bottom: 24px; font-weight: 700; font-size: 24px; color: #212121").text
        #m.kuku.luは便利だけど自動化するにあたっては他のプラットフォームの方がいい可能性アリ
        #----------------------------------------------------------------------------

        text=text.replace(" ","")
        text=text.replace("\n","")
        return text
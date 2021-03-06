import base64
import time
 
import requests
requests.packages.urllib3.disable_warnings()
 
class tv:
    def __init__(self):
        self.root = 'http://39.108.64.125/WebRoot/superMaster/Server'
        self.memi1 = "9774d56d682e549c"
        self.rightkey = "376035775"
        self.key = "308202d5308201bda00302010202041669d9bf300d06092a864886f70d01010b0500301b310b3009060355040613023836310c300a06035504031303776569301e170d3136303731383038313935395a170d3431303731323038313935395a301b310b3009060355040613023836310c300a0603550403130377656930820122300d06092a864886f70d01010105000382010f003082010a028201010095f85892400aae03ca4ed9dcd838d162290ae8dd51939aac6ecfde8282f207c4cd9e507929a279e0a36f1e4847330cb53908c92915b2c6a93d7064be452d073a472093f7ca14f4ab68f827582fe0988e9e4bc8a6ea3b56001cbbbb760f9eec571b0bbc97392e65aaf08c686f0e2ba353896d48a37c36716239977bd0e4dd878025cab497d8164537aec9f6599eefb98577dce972a1b794e211226520e23497beec3fd8548bb5b4d263120d40115cca28116bac32378df5033f536a0d7367fef78c587fefed28c5c9b35ba684ed6e46d9369c40950cf7ad7236d10b7a51dfd2a8f218db72323bbd19f46947410b1191f263012ad4ba8f749223e37591254ee7f50203010001a321301f301d0603551d0e041604143d43284bd5e4b0d322c9962a5b70aad4dcbc3634300d06092a864886f70d01010b050003820101000f04c51ff763311aa011777ba2842b441b15c316373d1e1ed4116cf86e29d55c6ed3fa4c475251b1fb4fac57195dbca0166ebe565d9834552a3758b97c4528bab1f7ab82bb3a9faa932f5bc10943f3daf52e0fe5889ffb58a6be67ea1c9a2fb37dc8aa6f3af476039a467336991a4e52dccd520195cd473eb5b984e702ed9ff638a14c3abb575a7a80ae4062084d1138a06a20e173be9df32df631311b07352898706198ddebaaa011f0da8e5f288f7cfb77505bc943f6476d6cc1feef56b68137aad91f23c4bb772169539d05653a6f0d75f7192164e822b934322f3a975df677903b1667f5dc1e9ddb185da3281d31bfb8f67a84bd23bbcb398f8bb637dd72"
 
    def post(self, data=None):
        if data is None:
            data = {}
        return requests.post(url=self.root,data=data)
 
    def register(self, name, password):
        ret = self.post({'name': name, 'pass': password, 'memi1': self.memi1, 'key': self.key, 'rightkey': self.rightkey})
        print("Register response data: ")
        print(ret.content.decode('utf-8'))
 
 
    def login(self, name, password ):
        ret = self.post({'name': name, 'pass': password, 'memi1': self.memi1, 'key': self.key, 'rightkey': self.rightkey, 'login' : 'login'})
        print("Login response data: ")
        print(ret.content.decode('utf-8'))
 
    def updateSocre(self,name,password,jifen):
        t = int(round(time.time() * 1000))
        sign = base64.b64encode(str(5 * t).encode('utf-8')).decode('utf-8')
        ret = self.post({'name' : name, 'pass' : password, 'jifen' : jifen, 'time' : t, 'sign' : sign})
        print("UpdataScore response data: ")
        print(ret.content.decode('utf-8'))
 
if __name__ == "__main__":
    tv = tv()
    # 注册账号
    print(tv.register("mee4", "mee4"))
 
    # 登录账号
    print(tv.login("mee4","mee4"))
 
    # 更新积分
    print(tv.updateSocre("mee4","mee4","1000"))

import frida
import sys
import json

jscode = """
function log(){
    var Log = Java.use("android.util.Log");
    var Throwable = Java.use("java.lang.Throwable");
    console.log(Log.getStackTraceString(Throwable.$new()));
}


Java.perform(function(){

    /*
    * 模拟抓包
    */
    var client = Java.use("com.cz.babySister.c.a")
    client.a.overload("java.lang.String","java.lang.String").implementation = function(arg1,arg2){
        send("抓包**********************************************")
        send("request_url："+arg1+arg2);
        var response_data1 = this.a(arg1,arg2);
        send("response_data：");
        send(response_data1)
        return response_data1;
    }

    client.a.overload("java.lang.String").implementation = function(arg1){
        send("抓包**********************************************")
        send("request_url："+arg1);
        var response_data2 = this.a(arg1);
        send("response_data：");
        send(response_data2)
        return response_data2;
    }

     client.b.overload("java.lang.String").implementation = function(arg1){
        send("抓包**********************************************")
        send("request_url："+arg1);
        var response_data3 = this.b(arg1);
        send("response_data：");
        send(response_data3)
        return response_data3;
    }


    /*
    * hook UserInfo修改积分，积分修改之后消费一次积分会上传到服务器更新
    */
    var userinfo = Java.use("com.cz.babySister.javabean.UserInfo");
    userinfo.getJifen.implementation  = function(){
        return "100000";
    }


    /*
    * hook修改返回值，支付失败变成成功
    */
    var pay = Java.use("com.cz.babySister.alipay.q");
    pay.b.implementation = function(){
        return "9000"
    }


    /*
    * 修改vip会出现封号，服务器除了禁账号也会禁android_id，hook修改android_id
    */
    var sec = Java.use("android.provider.Settings$Secure")
    sec.getString.implementation = function(arg1,arg2){
        return "9774d56d682e549a"
    }

});
"""


def on_message(message, data):
    if message['type'] == 'send':
        try:
            print(json.dumps(json.loads(message['payload'].encode('utf8')), sort_keys=True, indent=4,
                             separators=(', ', ': '), ensure_ascii=False))
        except:
            print("[*] {0}".format(message['payload']))


    elif message['type'] == 'error':
        for i in message:
            if i == "type":
                print("[*] %s" % "error:")
                continue
            if type(message[i]) is str:
                print("[*] %s" %
                      i + ":\n    {0}".format(message[i].replace('\t', '    ')))
            else:
                print("[*] %s" %
                      i + ":\n    {0}".format(message[i]))
    else:
        print(message)


process = frida.get_usb_device().attach('com.cz.babySister')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()

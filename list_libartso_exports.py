import frida
import sys

jscode = """

  var exports = Module.enumerateExportsSync("libart.so");
    for(var i=0;i<exports.length;i++){
        send("name:"+exports[i].name+"  address:"+exports[i].address);
     }

"""

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))


process = frida.get_usb_device().attach("com.cz.babySister")
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()

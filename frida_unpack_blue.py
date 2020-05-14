#-*- coding:utf-8 -*-
# coding=utf-8
import frida
import sys

def on_message(message, data):
	if message['type'] == 'send':
		try:
			print(json.dumps(json.loads(message['payload'].encode('utf8')), sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
		except:
			print("[*] {0}".format(message['payload']))
			base = message['payload']['base']
			size = int(message['payload']['size'])
			print(hex(base), size)
		# print session
		# dex_bytes = session.read_bytes(base, size)
		# f = open("1.dex","wb")
		# f.write(dex_bytes)
		# f.close()
	elif message['type'] == 'error':
		for i in message:
			if i == "type":
				print("[*]%s" % "error:")
				continue
			if type(message[i]) is str:
				print("[*] %s" % i + ":\n	{0}".format(message[i].replace('\t', '	')))
			else:
				print("[*] %s" % i +":\n	{0}".format(message[i]))
	else:
		print(message)

	# MI6X 9.0	_ZN3art16ArtDexFileLoader10OpenCommonEPKhmS2_mRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPKNS_10OatDexFileEbbPS9_NS3_10unique_ptrINS_16DexFileContainerENS3_14default_deleteISH_EEEEPNS_13DexFileLoader12VerifyResultE
	# 9.0 arm 需要拦截　_ZN3art13DexFileLoader10OpenCommonEPKhjS2_jRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPKNS_10OatDexFileEbbPS9_NS3_10unique_ptrINS_16DexFileContainerENS3_14default_deleteISH_EEEEPNS0_12VerifyResultE
	# 7.0 arm：_ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_
	# 红米4A 6.0.1 arm: _ZN3art7DexFile10OpenMemoryEPKhmRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_	address:0x7f9ee7adf0
package = sys.argv[1]
print("dex 导出目录为: /data/data/%s"%(package))
device = frida.get_usb_device()
print("device:%s"%(device))
pid = device.spawn(package)
print("pid:%s"%(pid))
session = device.attach(pid)
print("session:%s"%(session))

src = """
var exports = Module.enumerateExportsSync("libart.so");
    for(var i=0;i<exports.length;i++){
        //if(exports[i].name == "_ZN3art7DexFile10OpenMemoryEPKhmRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_10OatDexFileEPS9_"){
        //if(exports[i].name == "_ZN3art16ArtDexFileLoader10OpenCommonEPKhmS2_mRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPKNS_10OatDexFileEbbPS9_NS3_10unique_ptrINS_16DexFileContainerENS3_14default_deleteISH_EEEEPNS_13DexFileLoader12VerifyResultE"){//MI6X
        if(exports[i].name == "_ZN3art7DexFile10OpenMemoryEPKhjRKNSt3__112basic_stringIcNS3_11char_traitsIcEENS3_9allocatorIcEEEEjPNS_6MemMapEPKNS_7OatFileEPS9_"){//夜神
            var openMemory = new NativePointer(exports[i].address);
            }
     }
console.log('openMemory 函数地址：' + openMemory)
Interceptor.attach(openMemory, {
    onEnter: function (args) {
		//dex起始位置	
        var begin = args[0]
		console.log('args[0]:' + args[0] + '	args[1]:' + args[1])
		
		//打印magic
        console.log("magic : " + Memory.readUtf8String(begin))

		//dex fileSize 地址
        var address = parseInt(begin,16) + 0x20
		console.log('address =  ' + address)
		
		//dex 大小
        var dex_size = Memory.readInt(ptr(address))
        console.log('dex_size = ' + dex_size)


		//dump dex 到/data/data/pkg/目录下  实测真机安卓9.0必须是这个目录 因为app只对他自己的这个目录有写入权限
        var file = new File("/data/data/com.cz.babySister/" + dex_size + ".dex", "wb")
        // var file = new File("/data/data/com.cz.babySister/" + dex_size + ".dex", "ab+")
        file.write(Memory.readByteArray(begin, dex_size))
        file.flush()
        file.close()

        var send_data = {}
        send_data.base = parseInt(begin,16)
        send_data.size = dex_size
        send(send_data)
    },
    onLeave: function (retval) {
        if (retval.toInt32() > 0) {
        }
    }
});
"""

script = session.create_script(src)

script.on("message" , on_message)

script.load()
device.resume(pid)
sys.stdin.read()

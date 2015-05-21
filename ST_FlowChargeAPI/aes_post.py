#coding:utf-8
import data, pycurl
#aes加密得到16进制串
def encrypt_mode_cbc(data, key = 'H5gOs1ZshKZ6WikN', iv = '8888159601152533'):
    from Crypto.Cipher import AES
    
    lenth = len(data)
    num = lenth % 16
    data = data.ljust(lenth + 16 - num,chr(16 - num))
    obj = AES.new(key, AES.MODE_CBC, iv)
    result = obj.encrypt(data)
    return result.encode('hex')


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

#aes加密得到16进制串转2进制
def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))
    
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
def dec2bin(string_num):
    global base
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])


#2进制按规则16进制加密   
def encodeBytes(bytelist):
    pieces = len(bytelist) / 8
    in_list = [int(bytelist[i*8:(i+1)*8],2) for i in range(pieces)]
    
    ret = []
    for byte in in_list:
        ret.append( chr(((byte >> 4) & 0xF) + 97) )
        ret.append( chr((byte & 0xF) + 97) )
    return ''.join(ret)
    
    
#post
def _postJson(json_str):
        c = pycurl.Curl()
        buf = cStringIO.StringIO()
        try:
           
            url = 'http://118.123.170.72:8888/fps/flowService.do'
            c.setopt(c.URL, url)
            #c.setopt(c.SSLVERSION, c.SSLVERSION_TLSv1)
            c.setopt(c.WRITEFUNCTION, buf.write)            
            #c.setopt(c.CONNECTTIMEOUT, 3)
            #c.setopt(c.TIMEOUT, 3)
            c.setopt(c.HTTPHEADER, ["Content-Type:application/json"]) 
            c.setopt(c.POSTFIELDS, json_str)
            c.perform()
            content = buf.getvalue()
            print content
            buf.close()
            c.close()
           
            return content
        except:
            c.close()
            buf.close()
            logging.error('api timeout')
            return None

#coding:utf-8

# For flow800 pack.
# 2015-05-15

import sys, data, binascii
from httpUtil import NetUtil as hu
from Crypto.Cipher import AES
from httpUtil import NetUtil as hu
import urllib



AES_KEY = data.aes_key #16-bytes password
AES_IV = data.aes_iv


def AES_encode(param_string):
    key = AES_KEY #16-bytes password
    iv = AES_IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # String must have a length of 16
    x = len(param_string) % 16
    if x != 0:
        fs_pad = param_string + '0'*(16 - x) 
    msg = cipher.encrypt(fs_pad)
    print 'File after AES is like...', binascii.b2a_hex(msg)
    return msg


def main():
	code_str = AES_encode(str(data.code_dic))
	code_str = binascii.b2a_hex(code_str)
	params_dic_800 = {
		'partner_no':data.partner_no,
		'code':code_str
	}
	#para_str = str(data.params_dic_800) % code_str
	#print para_str

	url = data.url_800
	m = hu()
	#print str(data.test_msg_dic1)
	test_msg = "{\"partner_no\":\"100054374\",\"code\":\"kdhgopclbjhfgkaceegofdkkhjpiilgakkbhllgjjomgfohclnaehcccaogbeikijceabpkcbbnaobmnbogifekhppomhopgiocofajbhofkikgmneibdhppnlhkddlmhjnmeildgfhppdclofpciainlhkhppbliihmhbdofplgblfoffepgnjgbebchaddkopkeifpjjjfonemigbbnejibcmkhellfhlcfocfjcecmdpmlgifheiihanckaaifcjaaaajkccnakjmdgkcaddbfifceknpmmdmkcgilgoclofmckcfjdcnaimccagffkplmoekclbelgkhbccomgamehkjhgnpoigikcgobolfpddcahcfpdagadljhpnhagamkeoahfdbkepbpcagdeeloppicfma\"}"
	print "*",test_msg
	resp = m.http_post(url, test_msg)#str(data.test_msg_dic1))
	print 'returned.'
	print resp

if __name__ == '__main__':
	main()
#coding:utf-8

# For flow800 pack.
# 2015-05-15

import sys, time, random, data
from Crypto.Cipher import AES
from httpUtil import NetUtil as hu
import aes_post as ap


AES_KEY = data.aes_key #16-bytes password
AES_IV = data.aes_iv


def AES_encode(param_string):
    key = AES_KEY #16-bytes password
    iv = AES_IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # String must have a length of 16
    x = len(param_string) % 16
    if x != 0:
        fs_pad = param_string + ' '*(16 - x) 
    msg = cipher.encrypt(fs_pad)
    #print 'File after AES is like...', binascii.b2a_hex(msg)
    return msg

def process_one():
	reqNO = str(int(time.time()*1000)) + str(random.randint(10000,99999)) # String 20

	codeString = data.get_post_params(reqNO, '18923090380')
	codeString = ap.encrypt_mode_cbc(codeString, data.aes_key, data.aes_iv)
	codeString = ap.hex2bin(codeString)
	codeString = ap.encodeBytes(codeString)
	params_dic_800 = {
		'partner_no':data.partner_no,
		'code':codeString
	}

	url = data.url_800
	m = hu()
	resp = m.http_post(url, str(params_dic_800))
	print resp


if __name__ == '__main__':
	process_one()

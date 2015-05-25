#coding:utf-8

# For flow800 pack.
# 2015-05-15

import sys, os, json, time, random, data
from Crypto.Cipher import AES
from httpUtil import NetUtil as hu
import aes_post as ap

_DEBUG_ = data._DEBUG_

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

def process_one(phone, prod_id):
	reqNO = time.strftime('%Y%m%d%H%M%S',time.localtime()) + str(random.randint(10000,99999)) # String 20

	codeString = data.get_post_params(reqNO, phone, prod_id)
	print codeString
	codeString = ap.encrypt_mode_cbc(codeString, data.aes_key, data.aes_iv)
	codeString = ap.hex2bin(codeString)
	codeString = ap.encodeBytes(codeString)
	params_dic_800 = {
		'partner_no':data.partner_no,
		'code':codeString
	}

	url = data.url_800
	m = hu()
	try:
		resp = m.http_post(url, str(params_dic_800))
	except Exception, e:
		return 'HTTP ERR|'+str(e)
	return resp

def get_all_files(_dir):
	print 'Load dir : %s' % _dir
	resList = []
	list_dirs = os.walk(_dir)
	for root, dirs, files in list_dirs:
		for f in files:
			if f.split('.')[-1]=='txt' and len(f.split('.'))>=2:
				resList.append(os.path.join(root,f))
	return resList

def parse_json(string):
	try:
		dic = json.loads(string)
		return dic['request_no'], dic['result_code']
		pass
	except Exception, e:
		#raise e
		print string
		return (-1, e)


def main():
	print "**Debuge:%d\n**" % _DEBUG_
	file_list = get_all_files(sys.argv[1])
	file_str = '\n'.join(file_list)
	if 'y' == raw_input(file_str+'\n?y/n '): # File should be named in '100.txt 200.txt 500.txt'
		print 'Start reading files ...'
	else:
		return

	wf = open(sys.argv[1]+'/res.txt', 'w')

	for f in file_list:
		request_no, result_code = (-1,-1)
		prod_id = f.split('/')[-1].split('.')[0]
		if prod_id not in ['10', '100', '200', '500']:
			continue

		print prod_id+'M', data.pack_dic[prod_id]
		i = 0

		with open(f, 'r') as fo:
			users = fo.readlines()
			print '\n==================================\nfile %s has %d numbers...' % (f, len(users))
			for usr in users:
				i += 1
				usr = usr.strip()
				res = process_one(usr, prod_id)
				request_no, result_code = parse_json(res)
				res_string = '%s,%s,%s,%s\n' % (usr, prod_id, request_no, result_code)
				if 0 == i%20 :
					print 'num %d: %s' % (i, res_string)
				print res_string
				wf.writelines(res_string)

	wf.close()

def test_cakk_bak():
	string = '{"request_no":"123test","result_code":"00000"}'
	m = hu()
	resp = m.http_post(data.url_cb, string)
	print resp

if __name__ == '__main__':
	#parse_json('{"request_no":"143252444834568482","result_code":"00000"}')
	main()
	#process_one()

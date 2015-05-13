#coding:utf-8

# 2015-05-13
# Test pack reject interface.

import httplib, urllib, json, sys
import data
from urlparse import urlparse

class NetUtil(object):
	"""A http query class."""
	def __init__(self):
		super(NetUtil, self).__init__()
		self.errcode = ''
		self.errmsg = ''

	def http_get(self, url, timeout=5, is_https=False):
		domain = port = query_string = data = ''
		o = urlparse(url)
		domain = o.hostname
		port = o.port if o.port else (443 if is_https else 80)
		if ''!=o.path or ''!=o.query:
			query_string = o.path + '?' + o.query

		if is_https:
			conn = httplib.HTTPSConnection(domain, port, timeout)
		else:
			conn = httplib.HTTPConnection(domain, port, timeout)
		conn.request('GET', query_string)

		resp = conn.getresponse()
		status = resp.status
		if 200 == status:
			data = resp.read()
		else:
			self.errcode = status
			self.errmsg = '%s' % resp.reason

		conn.close()
		return data

	def http_post(self):
		pass

class Pack(object):
	"""docstring for Pack"""
	def __init__(self, pack_id, is_available, priority):
		super(Pack, self).__init__()
		self.pack_id = pack_id
		self.pack_name = data.pack_code_name[pack_id]
		self.is_available = is_available
		self.priority = priority
	
	def print_pack_info(self):
		print '%s %s:%s, priority:%s' % ( self.pack_id, self.pack_name, self.is_available, self.priority)
		pass

def parse_flow_result(json_string):
	pack_list = []
	dc = json.loads(json_string)
	packs_string = json.dumps( dc['offers'] )
	packs =  json.loads(packs_string)

	for pack in packs:
		pk = Pack(pack['prodID'].encode('utf-8'), pack['sign'].encode('utf-8'), pack['priority'].encode('utf-8'))
		pk.print_pack_info()
		pack_list.append(pk)

		return pack_list

def main():
	url = data.url + ('18923090380' if len(sys.argv)<2 else sys.argv[1])
	print url
	m = NetUtil()
	resp = m.http_get(url)
	if '' == resp:
		print m.errcode, m.errmsg
	else:
		print resp[resp.find('<')+len('<br/>'):]
		packs = parse_flow_result(resp[:resp.find('<')].strip())
		for p in packs:

			pass


if __name__ == '__main__':
	main()

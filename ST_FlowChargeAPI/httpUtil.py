#coding:utf-8

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
		port = o.port if o.port else ('443' if is_https else '80')
		if ''!=o.path or ''!=o.query:
			query_string = o.path + '?' + o.query

		if is_https:
			conn = httplib.HTTPSConnection(domain, port) # ,timeout)
		else:
			conn = httplib.HTTPConnection(domain, port, timeout)

		print 'string',query_string
		conn.request(u'GET', query_string)

		resp = conn.getresponse()
		status = resp.status
		if 200 == status:
			data = resp.read()
		else:
			self.errcode = status
			self.errmsg = '%s' % resp.reason
			data = 'err:%d\t%s' % (self.errcode, self.errmsg)

		conn.close()
		return data

	def http_post(self, url, ps={}, timeout=5, is_https=False):
		headers = {"Content-type": "application/json","Accept": "text/plain"}
		domain = port = query_string = data = ''
		o = urlparse(url)
		domain = o.hostname
		port = o.port if o.port else (443 if is_https else 80)
		if ''!=o.path or ''!=o.query:
			query_string = o.path + '?' + o.query

		if is_https:
			conn = httplib.HTTPSConnection(domain, port) # ,timeout)
		else:
			conn = httplib.HTTPConnection(domain, port, timeout)

		#ps = urllib.quote(ps)
		print ps
		conn.request('POST', query_string, ps, headers)
		resp = conn.getresponse()
		status = resp.status
		if 200 == status:
			data = resp.read()
		else:
			self.errcode = status
			self.errmsg = '%s' % resp.reason
			data = 'err:%d\t%s' % (self.errcode, self.errmsg)
		conn.close()
		return data

def main():
	url = 'https://baidu.com'
	m = NetUtil()
	resp = m.http_get(url, is_https=True)
	print resp

if __name__ == '__main__':
	main()
#coding:utf-8

# 2015-05-10
# Parse the order error logs file during ordering flow pack from ST.
# There two type of error log files, .xls file and .txt files, which 
# have different data structure.
# Parse both types of the log files into a table.

import sys, xlrd

ERR_TYPE = {
	'4G' : '4G',
	'副卡':'副卡',
}

ERR_FLAG = 'BPSUBSCPTEX'
ERR_TYPE_LIST = [u'4G', u'副卡', u'依赖', u'互斥', u'III类客户', u'信息存储失败', u'没有定义', u'单位证件', u'App运行', u'派生了销售品退订', u'无效状态', u'欠费', u'SOAP']

class FailureMsg(object):
	"""docstring for FailureMsg"""
	def __init__(self, _orderPack, _msgString):
		super(FailureMsg, self).__init__()
		self.orderPack = _orderPack
		self.msgString = _msgString
		self.err_type = [
		0, #err_4g = 0
		0, #err_fk = 0
		0, #err_depd = 0
		0, #err_reject = 0
		0, #err_3 = 0
		0, #err_ccsb #信息存储失败，分为订单信息和申请信息
		0, #err_notdef
		0, #err_
		0, #err_app
		0, #err_pstd = 0
		0, #err_tcwx
		0, #err_qf
		0, #err_soap = 0
		]
		self.err_others = 0


	def RejectInfo(self):
		pass

	def GetErrCode(self):
		codePos = self.msgString.find('代码')
		if -1 != codePos:
			return self.msgString[codePos+3 : codePos+8]
		else:
			return ''

	def parseMsg(self):
		errTypeIndex = -1
		for i in range(len(ERR_TYPE_LIST)):
			errTypeIndex = self.msgString.find(ERR_TYPE_LIST[i])
			if -1 != errTypeIndex:
				self.err_type[i] = ERR_TYPE_LIST[i]
				return
		self.err_others = 1
		return

	def GetErrType(self):
		self.parseMsg()
		for errType in self.err_type:
			if errType != 0:
				return errType
		
	def PrintOtherErrMsg(self):
		self.parseMsg()
		if 1 == self.err_others:
			return self.msgString

class OrderFailure(object):
	"""A order OrderFailure."""
	def __init__(self, _platForm, _phone, _oper_code, _orderPack, _errCode, _errMsg, _errType, _errTime):
		super(OrderFailure, self).__init__()
		self.platForm = _platForm
		self.phone = str(_phone).strip(u'.0')
		self.operCode = str(_oper_code).strip(u'.0')
		self.orderPack = _orderPack
		self.errCode = _errCode
		self.errMsg = _errMsg.strip('\r\n')
		self.errType = _errType
		self.errTime = _errTime
		self.fm = FailureMsg(self.orderPack, self.errMsg)

	def PrintDetail(self):
		return u'%s|%s|%s|%s|%s|%s|EOL|\n' % (self.platForm, self.phone, self.operCode, self.orderPack, self.fm.GetErrType(), self.errMsg)

	def GetErrMsgTypeString(self):
		fm = FailureMsg(self.orderPack, self.errMsg)
		return fm.GetErrMsgTypeString()

	def GetOtherMsg(self):
		fm = FailureMsg(self.orderPack, self.errMsg)
		return fm.PrintOtherErrMsg()



def parse_xlsx_file( _xlsxFileName ):
	resList = []
	data = xlrd.open_workbook( _xlsxFileName )
	table = data.sheet_by_index(0)
	nrows = table.nrows
	print '****************************rows:', nrows

	count = 0
	for x in ERR_TYPE_LIST:
		#print x
		pass

	for i in range(1,nrows):
		rec = table.row_values(i)
		try:
			assert 9 == len(rec)
			# _platForm, _phone, _oper_code, _orderPack, _errCode, _errMsg, _errType, _errTime
			OdFl = OrderFailure(u'mb', rec[1], rec[2], rec[3], rec[4], rec[6], rec[7], rec[8]) # <type 'unicode'>
			resList.append((OdFl.PrintDetail()+'\n').encode('utf-8'))
		except Exception, e:
			raise e
	return resList

def parse_csv_file( _csvFileName ):
	resList = []
	with open(_csvFileName, 'r') as rf:
		recs = rf.readlines()
		print '****************************rows:', len(recs)

		for rec in recs:
			sections = rec.split('|')
			assert 9 == len(sections)
			# _paltForm, _phone, _oper_code, _orderPack, _errCode, _errMsg, _errType, _errTime
			OdFl = OrderFailure(u'st', sections[0], sections[2], '', '', sections[8].decode('utf-8'), '', sections[6])
			resList.append( (OdFl.PrintDetail()).encode('utf-8') )

	return resList


def main():
	# Print parseing file name.
	#'''
	wf = open('result.csv', 'w')
	csvf = ['./data/error_on_one_click_Mar.txt','./data/error_on_one_click_Apr.txt']
	xlsf = ['./data/3月明白消费页订购失败数据源error.xlsx', './data/4月明白消费页订购失败数据源.xlsx']
	for f in csvf:
		wf.writelines( parse_csv_file(f)) 

	try:
		tmpV = raw_input('解析文件\n\t%s\n，是否继续？ y/n ' % xlsf)
		if 'y' == tmpV:
			for f in xlsf:
				wf.writelines( parse_xlsx_file(f)) 
	except Exception, e:
		raise e
	wf.close()


if __name__ == '__main__':

	main()


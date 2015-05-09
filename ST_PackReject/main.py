#coding:utf-8

#建立数据类型，存储每个用户的号码和套餐资料

#读取用户数据，创建对象

#创建套餐表：ST流量包、5个4G流量包

#规范套餐互斥关系数据格式，读入后自动生成目标套餐表

#遍历号码与套餐，生成每个号码的输出格式

import sys, datetime

__DEBUG = False

TargetPackDir = './input/target_packs_lz.txt'
#TargetPackDir = './input/target_packs_lz.txt'

class Pack(object):
	"""docstring for Pack"""
	def __init__(self, _serial, _id, _name):
		super(Pack, self).__init__()
		self.serial = _serial
		self.id = _id
		self.name = _name

	def get_serial(self):
		return self.serial

	def get_pack_string(self):
		return "%s|%s|%s" % (self.serial, self.id, self.name)

	def get_name(self):
		return self.name


class TargetPack(Pack):
	"""docstring for TargetPack"""
	def __init__(self, _serial, _id, _name, _pay, _is4g):
		super(TargetPack, self).__init__(_serial, _id, _name)
		self.pay = _pay
		self.is4g = _is4g
		self.reject_packs = {}

	def add_rej_pack(self, _pack):
		self.reject_packs[_pack.get_serial()] = _pack

	def get_pay(self):
		if self.pay in ['1', '2']:
			return self.pay
		else:
			return ''

	def is_4g(self):
		if self.is4g in ['1', '0']:
			return self.is4g
		else:
			return ''

	def get_reject_packs(self):
		return self.reject_packs
		
	def print_detail(self):
		print 'Target Pack %s has %d reject packs:' % (self.get_serial(), len(self.reject_packs))
		for k in self.reject_packs:
			print self.reject_packs[k].get_serial()
		

class User(object):
	"""docstring for User"""
	def __init__(self, _phone, _pay):
		super(User, self).__init__()
		self.phone = _phone
		self.pay = _pay
		self.is4g = ''
		self.packs = {}
		self.how_many_ordered_packs = 0

	def add_pack(self, _pack):
		if self.packs.has_key(_pack.serial):
			#print '\t\t Pack %s has loaded for user %s' % (_pack.serial, self.phone)
			return -1, "self.phone|%s" % _pack.get_pack_string() # Return the pardon record in format 'serial|id|name'.
		else:
			self.packs[_pack.serial] = _pack
			self.how_many_ordered_packs += 1
			return self.how_many_ordered_packs,''

	def get_phone(self):
		return self.phone

	def get_pack_count(self):
		return self.how_many_ordered_packs

	def get_pay(self):
		if self.pay in ['1', '2']:
			return self.pay
		else:
			return ''

	def get_4g(self):
		if self.is_4g in ['1', '0']:
			return self.is4g
		else:
			return ''

	def is_4g(self):
		for pack in self.packs:
			if -1 != self.packs[pack].name.upper().find('4G'):
				return '1'
		return '0'


def main():
	startTime = datetime.datetime.now()
	users_g = {}	# Stores all users.

	# Clear pardon_files.
	with open("./pardon_lines.txt", 'w') as pf:
		pass



	if 2 <= len(sys.argv):
		# Load all users into variable users_g.
		with open(sys.argv[1], 'r') as rf:
			recs = rf.readlines()
			print len(recs), "lines read.\n"
			print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds

			for rec in recs:
				try:
					sections = rec.split("|")
					user = User(sections[0], sections[1])
					pack = Pack(sections[2], sections[3], sections[4])
					user.add_pack(pack)
					if users_g.has_key(user.get_phone()):
						add_res = users_g[user.get_phone()].add_pack(pack)
						'''
						if __DEBUG:
							# Write pardon files into file.
							if -1 == add_res[0]:
								with open('./pardon_lines.txt', 'a') as pf:
									pf.writelines(add_res[1])'''
					else:
						users_g[user.get_phone()] = user
				except Exception, e:
					raise e
				finally:
					pass

			print 'Loading users info done.'
			print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds
				
	else:
		print ('No file input.')
		return



	# Compare with target packs. Return '13399999999|1|0|1|1| ...' as result and write it into file.

	# Load target packs first.
	all_target_packs = {} # {target_pack_serial:Target_pack, ...}
	with open(TargetPackDir, 'r') as tpf:
		tpRecs = tpf.readlines()

	for tpRec in tpRecs:
		try:
			tpSections = tpRec.strip().split('|') # tar_pack: serial, id, name, pay, is_4g
			reject_pack = Pack(tpSections[5], tpSections[6], tpSections[7]) # An Pack object.
			targetPack = TargetPack(tpSections[0], tpSections[1], tpSections[2], tpSections[3], tpSections[4])
			if all_target_packs.has_key(targetPack.get_serial()):
				all_target_packs[targetPack.get_serial()].add_rej_pack(reject_pack)
			else:
				targetPack.add_rej_pack(Pack(tpSections[5], tpSections[6], tpSections[7]))
				all_target_packs[targetPack.get_serial()] = targetPack
			
			'''
			if all_target_packs.has_key(tpSections[0]):
				all_target_packs[tpSections[0]].append(tpSections[3])
			else:
				all_target_packs[tpSections[0]] = [tpSections[3]]'''
		except Exception, e:
			print tpRec
			raise e
		finally:
			pass
	print 'Loading target pack info done.'
	print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds
	'''  test code
	for p in  all_target_packs:
		print p
		print all_target_packs[p].print_detail()
			#print k, all_target_packs[p][k]
	#'''


	target_pack_file_flag = TargetPackDir.split('/')[-1].split('_')[-1] # 'lz.txt' or 'st.txt'
	wf_filename = './output/' + sys.argv[1].split('/')[-1].replace('.txt','_res_' + target_pack_file_flag)
	with open(wf_filename, 'w') as wf:

		result_tile_line = 'phone' # The first line for result file.
		for tp in all_target_packs:
			result_tile_line += '|%s' % all_target_packs[tp].get_serial()
		wf.writelines(result_tile_line+'\n')

		for user_phone in users_g:
			user_res = user_phone # result line:'13399999999'
			user_pay = users_g[user_phone].get_pay()
			user_4g = users_g[user_phone].is_4g()
			if user_phone=='18022581839':
				print 'packs:', users_g[user_phone].get_pack_count()
				print 'is_4g:', user_4g 

			for tp in all_target_packs: # Get 0 or 1 fro user_res
				is_avalible = '|11'
				tp_pay = all_target_packs[tp].get_pay()
				tp_4g = all_target_packs[tp].is_4g()

				if min(tp_pay, user_pay) != '' and tp_pay != user_pay: 
				# If both payment info of tp and user exists.
				# And if payment info not identical.
					is_avalible = '|0p'
				elif 1:
					for p in users_g[user_phone].packs:
						if all_target_packs[tp].get_reject_packs().has_key(p):
							is_avalible = '|0r'
							break
					if min(tp_4g, user_4g) != '' and tp_4g != user_4g:
						#test
						#print 'pay', tp_pay, user_pay
						#print 'prod:%s,4g:%s,%s,  %s,%s' % (tp,tp_4g, user_4g, type(tp_4g), type(user_4g))
						is_avalible = '|04'

				user_res += is_avalible
			wf.writelines(user_res+'\n')
	print 'Write result file %s done.' % wf_filename
	print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds



	#''' ========== test code section ============
	print len(users_g), "users read."

	lines = 0
	for user in users_g:
		lines += users_g[user].get_pack_count()
	print lines, "normal lines read."

	if __DEBUG:
		with open('pardon_lines.txt', 'r') as pf:
			print len(pf.readlines()), 'pardon lines fond.'
	#============ test code end =============='''

# For temprory use.
# Add payment type info (1 or 2) into source data.
def main_rewrite_file():
	startTime = datetime.datetime.now()

	file_lz = './input/users_lz.csv'
	file_st = './input/users_st.csv'

	user_pay = {}
	# Load payment type.
	for f in (file_lz, file_st):
		with open(f, 'r') as rf:
			recs = rf.readlines()
			print 'Read file %s done.' % f
			print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds

			for rec in recs:
				secs = rec.split(',')
				pay = secs[1].strip()
				if '1' == pay or '2' == pay:
					user_pay[secs[0]] = pay

			print 'Load file %s done.' % f
			print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds

	wf = open('./output/user.txt', 'w')
	with open(sys.argv[1], 'r') as rf:
		done = False
		count = 0
		try:
			while not done:
				count += 1
				if count%200000 == 0:
					print '%d recs read' % count
					print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds
					wf.flush()

				rec = rf.readline()
				if rec != '':
					secs = rec.strip().split('|')
					if user_pay.has_key(secs[0]):
						secs.insert(1, user_pay[secs[0]][0])
						wf.writelines('|'.join(secs) + '\n')
					else:
						continue
				else:
					print '\nRead file end', count
					done = True
					wf.flush()
		except Exception, e:
			print e
			#raise e
		finally:
			print 'Write file done.'
			print '== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds
	wf.close()

# Remove duplicate lines.
def main_remove_duplicate_lines():
	startTime = datetime.datetime.now()
	recs = ''.join(set([x for x in open(sys.argv[1]).readlines() if x.strip()!='']))
	print 'Reading end.\n== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds
	with open('./output/tcpp_rm_dup.txt', 'w') as wf:
		wf.writelines(recs)
	print 'Removing end.\n== Time cllapse:%d\n' % (datetime.datetime.now()-startTime).seconds




if __name__ == '__main__':
	main()
	#main_rewrite_file()
	#main_remove_duplicate_lines()		

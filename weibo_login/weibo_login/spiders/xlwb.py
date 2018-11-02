# -*- coding: utf-8 -*-
import scrapy
import base64
import time 
from urllib.parse import urlencode
import json
import rsa
import random
import binascii
import re



class XlwbSpider(scrapy.Spider):
	name = 'xlwb_login'
	#allowed_domains = ['weibo.com']

	headers = {
	# 'Host':	'login.sina.com.cn',
 # 'Connection':	'keep-alive',
# 'Content-Length':	'624',
#  'Cache-Control':	'max-age=0',
# 'Origin'	:'https://weibo.com',
# 'Upgrade-Insecure-Requests':	'1',
# 'DNT':	'1',
# 'Content-Type':	'application/x-www-form-urlencoded',
'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
# 'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Referer':	'https://weibo.com/',
# 'Accept-Encoding':	'gzip, deflate, br',
# 'Accept-Language':	'zh-CN,zh;q=0.9,en;q=0.8',
#'Cookie':	'login=13a0857768fc0c0abafd3d70c0f4538a; SINAGLOBAL=172.16.138.138_1541038556.17115; Apache=172.16.138.138_1541038556.17118; SCF=Ak293onlvowNUZWlI1oLUXcE0wArmO0a9MI21yqrI9z2WpS1ylInhlUjEN9Z4fJ97upo_ry9Qe6mtvO1pSY_jpM.; SUB=_2AkMshu0hdcPxrAZVmf4dzGrrZY5H-jyfU4TXAn7tJhMyAhh77gstqSVutBF-XKfjkkrL3alAhn_FrXpvN8SG_XDW; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Whh4h34Gi_jawDnV6vY-g4n5JpVF02ReoefShBpeK2p; ULOGIN_IMG=tc-f1d1b49c8fef60b0962feaeaac73a0090ada',

	}

	def start_requests(self):
		url = 'https://login.sina.com.cn/sso/prelogin.php?'
		su = base64.b64encode(b'weifanw_stu@163.com')
		ser_time = int(time.time()*1000)
		param = {'entry':"weibo",'callback':"sinaSSOController.preloginCallBack",'su':su,'rsakt':"mod",'checkpin':'1','client':'ssologin.js(v1.4.19)','_':ser_time}
		pre_url = url + urlencode(param)
		yield scrapy.Request(url=pre_url, callback=self.get_form,meta={'cookiejar':1})
    
	def get_form(self, response):
		res_text = response.text
		res_text = res_text.strip('sinaSSOController.preloginCallBack')
		res_text = res_text.strip('(')
		res_text = res_text.strip(')')
		res_text = json.loads(res_text)
		login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'

		nonce = res_text['nonce']
		pcid = res_text['pcid']
		servertime = res_text['servertime']
		rsakv = res_text['rsakv']
		pubkey = res_text['pubkey']
		su = base64.b64encode(b'weifanw_stu@163.com')
		password = 'wangqiang654321'
		sp = self.get_password(servertime,nonce,password,pubkey)

		FormData = {
'entry': 'weibo',
'gateway': '1',
'from':'', 
'savestate': '0',
'qrcode_flag': 'false',
'useticket': '1',
'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1',
'pcid': pcid,
'door': '',
'vsnf': '1',
'su': su,
'service': 'miniblog',
'servertime': str(servertime),
'nonce': nonce,
'pwencode': 'rsa2',
'rsakv': '1330428213',
'sp': sp,
'sr': '1440*900',
'encoding': 'UTF-8',
'prelt': str(random.randint(20,200)),
'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
'returntype': 'META',
			}

		#login_url = 'https://login.sina.com.cn/signup/signin.php?entry=ss'
		yield scrapy.http.FormRequest(login_url,headers=self.headers, formdata=FormData, callback=self.redir_login,meta={'cookiejar':response.meta['cookiejar']})
	
	#def pre_login(self,response):
		# print(response.url)
		# res_text = response.meta
		# nonce = res_text['res_text']['nonce']
		# picd = res_text['res_text']['pcid']
		# servertime = res_text['res_text']['servertime']
		# rsakv = res_text['res_text']['rsakv']
		# pubkey = res_text['res_text']['pubkey']
		# su = base64.b64encode(b'18235441111')
		# password = 'wangqiang654321'
		#sp = self.get_password(servertime,nonce,password,pubkey)
		#print(sp)

# 		FormData = {
# 'entry': 'weibo',
# 'gateway': '1',
# 'from':'', 
# 'savestate': '0',
# 'qrcode_flag': 'false',
# 'useticket': '1',
# 'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1',
# 'pcid': pcid,
# 'door': '',
# 'vsnf': '1',
# 'su': su,
# 'service': 'miniblog',
# 'servertime': servertime,
# 'nonce': nonce,
# 'pwencode': 'rsa2',
# 'rsakv': '1330428213',
# 'sp': sp,
# 'sr': '1440*900',
# 'encoding': 'UTF-8',
# 'prelt': str(random.randint(20,200)),
# 'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
# 'returntype': 'META',
# 			}
		
		# FormData = {
		# 'ag':'',
		# 'username': su,
		# 'password': sp,
		# 'vsncode':'',
		# 'remLoginName':'on',
		# 'entry': 'sso',
		# 'gateway': '1',
		# 'from': '',
		# 'savestate': '0',
		# #'qrcode_flag': 'false',
		# 'useticket': '0',
		# 'pagerefer': 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',
		# 'vsnf': '1',
		# 'su': su,
		# 'service': 'sso',
		# 'servertime': str(servertime),
		# 'nonce': nonce,
		# 'pwencode':'rsa2',
		# 'rsakv':'1330428213',
		# 'sp':sp,
		# 'sr':'1440*900',
		# 'encoding':'UTF-8',
		# 'cdult': '3',
		# 'domain':'sina.com.cn',
		# 'prelt':str(random.randint(20,200)),
		# #'url':'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
		# 'returntype':'TEXT',
		# 	}
		#login_url = 'https://login.sina.com.cn/signup/signin.php?entry=sso'

		
		#return scrapy.http.FormRequest(login_url,headers=self.headers, formdata=FormData, callback=self.after_pre_login,meta={'cookiejar':response.meta['cookiejar']})

	def get_password(self,servertime,nonce,password,pubkey):
		#print(password)
		rsaPublickey = int(pubkey, 16)
		para2 = int('10001',16)
		key = rsa.PublicKey(rsaPublickey, para2) #创建公钥
		message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)#拼接明文 js加密文件中得到
		#print(message)
		message = bytes(message,encoding = "utf-8")
		passwd = rsa.encrypt(message, key)#加密
		passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
		#print(passwd)
		return passwd

		

	def redir_login(self,response):
		#print(response.xpath('//body/script/text()')).extract()
		#print(type(response.text))
		#redir_url = 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&sudaref=weibo.com'
		redir_url = 'https://passport.weibo.com/wbsso/login?url=https%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent.sinaSSOController.feedBackUrlCallBack%26sudaref%3Dweibo.com&display=0&'
		w1 = 'isplay=0&ticket='
		w2 = '&retcode='
		buff = response.text
		pat = re.compile(w1+'(.*?)'+w2,re.S)
		result = pat.findall(buff)
		#print(result[0])
		param = {'ticket':result[0],'retcode':'0'}
		final_url = redir_url + urlencode(param)
		#print(final_url)
		yield scrapy.Request(url = final_url, meta = {'cookiejar':response.meta['cookiejar']},callback = self.login_tmp_1)


	def login_tmp_1(self,response):
		#print(response.text)
		tmp_url1 = 'https://weibo.com/nguide/interest' 
		yield scrapy.Request(tmp_url1, meta={'cookiejar':response.meta['cookiejar']},callback=self.login_success)

	def login_success(self,response):
		#my_name = response.xpath('//div[@class="WB_miniblog"]/div[@class="WB_main clearfix"]/div[@class="WB_frame"]/div[@class="plc_main"]/div[@class="WB_main_r"]/div[@id="v6_pl_rightmod_myinfo"]/div[@class="WB_cardwrap S_bg2"]/div[@class="W_person_info"]/div[@class="WB_innerwrap"]/div[@class="nameBox"]/a').extract()
		#my_name = response.xpath('//div[@class="WB_miniblog"]//div[@class="WB_main clearfix"]//div[@class="WB_frame"]//div[@class="plc_main"]//div[@class="WB_main_r"]//div[@id="v6_pl_rightmod_myinfo"]//div[@class="WB_cardwrap S_bg2"]').extract()
		my_name = response.xpath('//div[@class="WB_miniblog"]/div[@class="WB_miniblog_fb"]/div[@class="WB_main clearfix"]').extract_first()
		#title = response.xpath('//title/text()').extract()
		#print(response.text)
		print(my_name)
		#my_name = str(my_name)
		# if my_name != '' :
		# 	print("登录成功！您的昵称为:" + my_name)
		# else:
		# 	print("登录失败！")
		
		


		




		







		# test = response.xpath('//span[@class="tit"]//text()').extract()
		# img_url = response.xpath('//img[@node-type="verifycode_image"]/@src').extract()
		# user_name = get_user_name('18235441111'):
		# sp = get_password('1q2w3e4r')
		# data = {
		# 'entry': 'account',
		# 'gateway': '1',
		# 'su': user_name,
		# 'servertime':servertime,
		# 'sp': password,
		# 'nounce':nounce,
		# }


		#print(response.text)

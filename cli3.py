# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import urllib2
import sys
    
BOT_TOKEN = 'bot123456789:abcdefgh-ijklmnopqrstuvwxyzABCDEFGY'
CHAT_ID = '@clienjirum'

def send_url ( url ) :
	link  ='https://api.telegram.org/' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=https://www.clien.net' + url
	print link
	urllib2.urlopen(link)
	
def save_no( no ):
	filename = 'bbsno.ini'
	f = open(filename, 'w')
	f.write(no)
	f.close();
	
def pasing_url( link ):

	with open('bbsno.ini', 'r') as f:
		old_no = f.readline()
		f.close()

	user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)" 
	req = urllib2.Request(link) 
	req.add_header("User-agent", user_agent)

	response = urllib2.urlopen(req) 
	headers = response.info().headers
	html = response.read() 

	# BeautifulSoup 로 파싱
	soup = BeautifulSoup(html)
	elements=soup.findAll("div", {"class" : "item"})

	for el in reversed(elements) :
		# 공지사항 제외
		str = ''.join(el.encode('utf-8'))
		if str.find("<span>공지</span>")> -1 :
			continue
		
		tt = el.find("a").text
		tt = ' '.join(tt.split()) # 긴 공백 제거
		title = tt.split(' ', 1)[1] # 카테고리 부부 제외  (상품정보,해외구매정보,오프라인정보 ... )

		url = el.find('a')['href']
		url = url.strip()
		bbs_no = url.split('/')[4]

		# 게시판 번호를 저장해서, 높은번호이면 알람
		if int( bbs_no ) > int ( old_no ) :
			send_url (url)
			save_no ( bbs_no )
			old_no = bbs_no
			
			
		#print title
		#print url		
		#print bbs_no

reload(sys)
sys.setdefaultencoding('utf-8')		

pasing_url('https://www.clien.net/service/board/jirum')
			


			
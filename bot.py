# -*- coding: utf-8 -*- 
import sys
import threading
import traceback
import psutil
import requests
import json
import os
import random
import datetime
import untangle
import urllib.parse
token = os.environ.get('BOT_TOKEN')
bot_name = ['bot','elin','елин','бот']
def apisay(text,toho,torep):
	param = (('v', '5.68'), ('peer_id', toho),('access_token',token),('message',text),('forward_messages',torep))
	result = requests.post('https://api.vk.com/method/messages.send', data=param)
	return result.text
open('system/msgs','w').write('')
data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
data = json.loads(data)['response']
def sendpic(pic,mess,toho,torep):
	ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
	with open('tmp/'+pic, 'rb') as f:
		ret = requests.post(ret['response']['upload_url'],files={'file1': f}).text
	ret = json.loads(ret)
	ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
	ret = json.loads(ret)
	requests.get('https://api.vk.com/method/messages.send?attachment=photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])+'&message='+mess+'&v=5.68&forward_messages='+str(torep)+'&peer_id='+str(toho)+'&access_token='+str(token))
def evalcmds(directory,toho,torep,answ):
	dir = os.listdir(directory)
	#print(dir)
	for plugnum in range(len(dir)):
	  exec(open(directory+'/'+str(dir[plugnum]),'r').read())
print('Инициализация бота завершена')
while True:
	try:
		response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data['server'], key=data['key'], ts=data['ts'])).json() 
		try: 
			updates = response['updates'];
		except KeyError:
			data = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+str(token)+'&v=5.68&lp_version=2').text
			data = json.loads(data)['response']
			continue
		if updates: 
			for result in updates: 
				if result[0] == 4:
					if (result[3] < 2000000000):
						userid = result[3]
					else:
						userid = result[6]['from']
					toho = result[3]
					torep = result[1]
					###game
					open('system/msgs','a+').write(str(result)+'\n')
					#result[5] = result[5].lower()
					answ = result[5].split(' ')
					bot_cmd = json.loads(open('system/cmds','r').read())
					#print(bot_cmd['default'])
					if len(answ) > 1:
						answ[0] = answ[0].lower()
						answ[1] = answ[1].lower()
						if (str(userid) not in bot_cmd["default"]) or (answ[1] in bot_cmd["admin"]):
							print('[Упоминание Бота от пользователя '+str(toho)+']')
							answ_text = result[5].split(' ')
							if len(answ_text) >2:
								answ_text.remove(answ_text[0])
								answ_text.remove(answ_text[0])
							else:
								answ_text = ''
							answ_text = ' '.join(answ_text)
							try:
								thr = threading.Thread(target=evalcmds,args=('plugins/default',toho,torep,answ))
								thr.start()
							except KeyError:
								pass
							adminlist = json.loads(open('system/admin','r').read())
							if str(userid) in adminlist:
								try:
									thr1 = threading.Thread(target=evalcmds,args=('plugins/admin',toho,torep,answ))
									thr1.start()
								except KeyError:
									pass
							else:
								if answ[1] in bot_cmd['admin']:
									apisay('А ты что тут забыл? Эта команда доступна лиш для owner',toho,torep)
	except Exception as error:
		adminlist = json.loads(open('system/admin','r').read())
		print(error)
		apisay(error,adminlist[0],'')
	data['ts'] = response['ts'] 

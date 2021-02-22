import os
try:
	import requests
except:
	os.system('pip install requests')
try:
	from tqdm.auto import tqdm
except:
	os.system('pip install tqdm')
	os.system('clear')
	print('\nPlease re-open this script again!')
	input()

def save(url, name):
	if not os.path.exists('MP3'):
		os.makedirs('MP3')
	path = 'MP3/'+name+'.mp3'
	response = requests.get(url, stream=True)
	with tqdm.wrapattr(open(path, "wb"), "write", miniters=1,
	                   total=int(response.headers.get('content-length', 0)),
	                   desc=name) as fout:
	    for chunk in response.iter_content(chunk_size=4096):
	        fout.write(chunk)
	            
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def search(qry):
	headers = {
	    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; POCO F1 Build/PQ3A.190801.002)',
	    'Host': 'www.saavn.com',
	    'Connection': 'Keep-Alive',
	    'Accept-Encoding': 'gzip',
	}
	
	params = (
	    ('cc', ''),
	    ('session_device_id', ''),
	    ('app_version', '7.6.1'),
	    ('_marker', '0'),
	    ('ctx', 'android'),
	    ('tz', 'Asia/Kolkata'),
	    ('query', str(qry)),
	    ('params', '{"type":"songs"}'),
	    ('api_version', '4'),
	    ('n', '10'),
	    ('manufacturer', 'Xiaomi'),
	    ('p', '1'),
	    ('network_operator', ''),
	    ('readable_version', '7.6.1'),
	    ('build', 'PQ3A.110801.002'),
	    ('v', '263'),
	    ('_format', 'json'),
	    ('model', 'POCO+F1'),
	    ('__call', 'search.getMoreResults'),
	    ('network_subtype', ''),
	    ('state', 'login'),
	    ('network_type', 'WIFI'),
	)
	
	res = requests.get('https://www.saavn.com/api.php', headers=headers, params=params)
	js = []
	
	for x in res.json()['results']:
		bb = {}
		bb['title'] = x['title'].replace('amp;','').replace('&quot;','')
		bb['image'] = x['image']
		bb['subtitle'] = x['subtitle']
		bb['id'] = x['more_info']['encrypted_cache_url']
		js.append(bb)
	return js

def play(id):
	headers = {
	    'Host': 'www.jiosaavn.com',
	    'accept': 'application/json, text/plain, */*',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 9; POCO F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36',
	    'sec-fetch-site': 'same-origin',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-dest': 'empty',
	    'accept-encoding': 'gzip, deflate, br',
	    'accept-language': 'en-US,en;q=0.9'
	}
	
	params = (
	    ('__call', 'song.generateAuthToken'),
	    ('url', str(id)),
	    ('bitrate', '320'),
	    ('api_version', '4'),
	    ('_format', 'json'),
	    ('ctx', 'wap6dot0'),
	    ('_marker', '0'),
	)
	
	res = requests.get('https://www.jiosaavn.com/api.php', headers=headers, params=params)
	if res.status_code == 200:
		return res.json()['auth_url']
	else:
		msg = 'Uh Oh! An error occured'
		print(msg)
		return False
		#sendMessage with error telegram

while True:
	print('''
░░█ █ █▀█ █▀ ▄▀█ ▄▀█ █░█ █▄░█
█▄█ █ █▄█ ▄█ █▀█ █▀█ ▀▄▀ █░▀█\n''')
	print('JioSaavn DL by S1 (V1.0)\n')
	qry = "+".join(str(input('Search: ')).lower().split())
	os.system("clear")
	if not qry:
		continue
	
	data = search(qry)
	cnt = 0
	for j in data:
		cnt += 1
		print(bcolors.OKGREEN+'['+str(cnt)+'] '+bcolors.WARNING+j['title']+' | '+bcolors.FAIL+j['subtitle'])
		print(bcolors.OKBLUE+'--------------------------------------------')
	
	try:
		choose = int(input('Choose: ').strip())
	except:
		os.system('clear')
		continue
	try:
		url = play(data[choose-1]['id'])
		if url != False:
			os.system("clear")
			name = data[choose-1]['title']
			#print("Download: "+url)
			save(url,name)
	except Exception as e:
		print('Exception: '+str(e))
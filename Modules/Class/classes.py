import urllib.request, threading, re, os, socket
from ..Config import *
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
from datetime import datetime

class Validador:

	def __init__(self, lang=Rules['Language']):
		self.lang = lang
		self.hoje = datetime.now().strftime("%d-%m-%Y") if self.lang == 0 else datetime.now().strftime("%Y-%m-%d")
		self.path = f'Resultados/{self.hoje}' if self.lang == 0 else f'Results/{self.hoje}'
		self.servidores = Rules['Server']
		self.Val = Rules['Validation']

		open('./sites.txt', 'w', encoding='utf-8').close() if not os.path.isfile('./sites.txt') else None
		Path(f'./{self.path}').mkdir(parents=True, exist_ok=True)

	def clear(self):
		return lambda: os.system('cls')

	def Idioma(self, config=False):

		Sitemap = [
			'Fora do servidor',
			'Sitemap correto', 
			'Sitemap incorreto', 
			'Sitemap inexistente',
			'Sitemap não recuperado',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Sitemap correct', 
			'Sitemap invalid', 
			'Sitemap nonexistent',
			'Sitemap not recovered',
			'Not recovered'
		]

		Tag = [
			'Fora do servidor', 
			'Tag recuperada', 
			'Tag não recuperada',
			'Cerificado inválido',
			'Domínio congelado'
		] if self.lang == 0 else [
			'Off the server', 
			'Tag recovered', 
			'Tag not recovered',
			'Certificate invalid',
			'Not recovered'
		]

		Servidor = [
			'Fora do servidor', 
			'Domínio congelado'
			'Dentro do servidor', 
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Frozen domain',
			'Inside the server', 
			'Not recovered'
		]

		SSL = [
			'Fora do servidor', 
			'SSL ativo', 
			'Domínio inativo',
			'SSL não ativo',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'SSL active', 
			'Domain is inactive',
			'SSL not active', 
			'Not recovered'
		]

		Recaptcha = [
			'Fora do servidor', 
			'Erro de recaptcha', 
			'Recaptcha em funcionamento',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Recaptcha error', 
			'Recaptcha\'s working', 
			'Not recovered'
		]

		Email = [
			'Fora do servidor', 
			'Email @doutoresdaweb', 
			'Email correto',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Email @doutoresdaweb', 
			'Email correct', 
			'Not recovered'
		]

		Sitename = [
			'Fora do servidor', 
			'Contém Doutores da web', 
			'Nome correto',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Contains Doutores da web', 
			'Sitename is correct', 
			'Not recovered'
		]

		Status = [
			'Fora do servidor', 
			'Online', 
			'Offline'
			'Inativo',
		] if self.lang == 0 else [
			'Off the server', 
			'Online', 
			'Offline',
			'Inactive',
		]
		
		return {
			'sitemap'	: Sitemap,
			'tag'		: Tag,
			'server'	: Servidor,
			'ssl'		: SSL,
			'recaptcha' : Recaptcha,
			'email'		: Email,
			'sitename'	: Sitename,
			'status'	: Status
		}[config]

	def Create_Path(self, path):
		Path(f'./{self.path}/' + path).mkdir(parents=True, exist_ok=True)
		
	def Base(self, url, www=False):
		try:
			if not www:
				return url
			else:
				return 'www.' + url
		except:
			return url

	def Check_Suspended(self, url):
		Suspended = [
			'Website Suspended'.lower(), 
			'Coming Soon'.lower()
		]
		return True if BeautifulSoup(urlopen(f'http://www.{url}/').read(), "html5lib").find('title').text.lower() in Suspended else False

	def Saiu(self, url, test=False):
		try:
			Domains = {
				'tester': {
					'inside': [],
					'out': [],
				},
				'domains': [
					socket.gethostbyname(self.Base(url)),
					socket.gethostbyname(self.Base(url, www=True))
				]
			}
			for Domain in Domains['domains']:
				if Domain in self.servidores:
					Domains['tester']['inside'].append(Domain)
				else:
					Domains['tester']['out'].append(Domain)

			if len(Domains['tester']['inside']) < 2:
			 	return '{}, {}'.format(Domains['tester']['out'][0], Domains['tester']['inside'][0]) if len(Domains['tester']['inside']) > 0 else Domains['tester']['out'][0]
			else:
				return False if not test else Domains['tester']['inside'][0]
		except:
			return 'No response'

	def Check_Key(self, recaptcha, url):
		with open(f'./Modules/Data/{recaptcha}.txt', 'r', encoding='utf-8') as f:
			linha = f.readlines()
			for sites in linha:
				if url in sites: return url
		return False

	def Response_Code(self, url):
		r = urllib.request.urlopen(f'http://www.{url}/').getcode()
		if r == 200: return r
		return False

	def Servidor(self, url):
		Def = 'server'
		try:
			self.Create_Path(Def)
			if self.Saiu(url):
				if self.Saiu(url).lower() != 'No response'.lower():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
				else:
					with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				if self.Response_Code(url) == 200:
					if not self.Check_Suspended(url):
						with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as file:
							file.write(f'{url} => {self.Saiu(url, test=True)}\n')
					else:
						with open(self.path + f'/{Def}/Suspended.txt', "a", -1, encoding='utf-8') as file:
							file.write(f'{url} => {self.Saiu(url, test=True)}\n')
				else:
					with open(self.path + f'/{Def}/Frozen domain.txt', "a", -1, encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Tag(self, url):
		Def = 'tag'
		try:
			self.Create_Path(Def)
			if self.Saiu(url):
				if self.Saiu(url).lower() != 'No response'.lower():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
				else:
					with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:
					request = urlopen(f"https://{url}/").read()
					html = BeautifulSoup(request, "html5lib");
					try:
						script = re.search(r"ga\('(create)',\s+'(.*?)',(.*?)\s+'(.*?)'\);", str(html.body)).group(2)
						with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
							file.write(f'{url}: {script}\n')
					except:
						try:
							script = re.search(r"gtag\([\"\']config[\"\'].*?[\"\'](.*?)[\"\']\);", str(html.body)).group(1)
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
								file.write(f'{url}: {script}\n')
						except:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
								file.write(f'{url}\n')
				except:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[4] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Certificado_SSL(self, url):
		Def = 'ssl'
		try:
			self.Create_Path(Def)
			if self.Saiu(url):
				if self.Saiu(url).lower() != 'No response'.lower():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
				else:
					with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				if self.Response_Code(url) == 200:
					if not self.Check_Suspended(url):
						try:
							Url = url.replace('www.', '')
							request = urlopen(f"https://www.{Url}/").read()
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as file:
								file.write(f'{url}\n')
						except:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', "a", -1, encoding='utf-8') as file:
								file.write(f'{url}\n')
					else:
						with open(self.path + f'/{Def}/Suspended.txt', "a", -1, encoding='utf-8') as file:
							file.write(f'{url} => {self.Saiu(url, test=True)}\n')
				else:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as file:
							file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[4] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Sitemap(self, url):

		Def = 'sitemap'
		http = [ f'https://www.{url}/', f'https://{url}', f'http://{url}', f'http://www.{url}/' ]

		try:
			self.Create_Path(Def)
			if self.Saiu(url):
				if self.Saiu(url).lower() != 'No response'.lower():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
				else:
					with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
						file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:

					request = urlopen(f'{http[3]}sitemap.xml').read()
					html = BeautifulSoup(request, "html5lib")

					sitemap = [
						re.findall(http[0], str(html.body)),
						re.findall(http[1], str(html.body)),
						re.findall(http[2], str(html.body)),
						re.findall(http[3], str(html.body)),
					]

					if sitemap[0]:
						if len(sitemap[0]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => https://www\n')
						else:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
						
					elif sitemap[1]:
						if len(sitemap[1]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => https://\n')
						else:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
							
					elif sitemap[2]:
						if len(sitemap[2]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => http://\n')
						else:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
								
					elif sitemap[3]:
						if len(sitemap[3]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => http://www\n')
						else:
							with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
					else:
						with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
							file.write(f'{url}\n')

				except:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[4] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[5] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Recaptcha(self, url):			
		Def = 'recaptcha'
		self.Create_Path(Def)
		if self.Saiu(url):
			if self.Saiu(url).lower() != 'No response'.lower():
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
		else:
			try:
				request = urlopen(f'http://www.{url}/contato').read()
				html = BeautifulSoup(request, "html5lib")
				g_recaptcha = re.search(r'data-sitekey=[\"\'](.*?)[\"\']', str(html.select('.form .g-recaptcha'))).group(1)
				if not self.Check_Key(g_recaptcha, url):
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {g_recaptcha}\n')
				else:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {g_recaptcha}\n')
			except:
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
					file.write(f'{url}\n')
					
	def Sitename(self, url):
		Def = 'sitename'
		self.Create_Path(Def)
		if self.Saiu(url):
			if self.Saiu(url).lower() != 'No response'.lower():
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
		else:
			try:
				request = urlopen(f'http://www.{url}/').read()
				html = BeautifulSoup(request, "html5lib")
				meta = re.search(r'content=[\"\'](.*?)[\"\']', str(html.select('head meta[property="og:site_name"]'))).group(1)
				if 'doutores da web' in meta.lower().strip():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {meta}\n')
				else:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {meta}\n')
			except:
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
					file.write(f'{url}\n')

	def Email(self, url):
		Def = 'email'
		self.Create_Path(Def)
		if self.Saiu(url):
			if self.Saiu(url).lower() != 'No response'.lower():
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
		else:
			try:
				request = urlopen(f'http://www.{url}/').read()
				html = BeautifulSoup(request, "html5lib")
				script = re.search(r'[\w.-]+@[\w.-]+.\w+', str(html.body)).group(0)
				if 'doutoresdaweb.com.br' in script.lower().strip():
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {script}\n')
				else:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {script}\n')
			except:
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
					file.write(f'{url}\n')

	def Status(self, url):
		Def = 'status'
		self.Create_Path(Def)
		if self.Saiu(url):
			if self.Saiu(url).lower() != 'No response'.lower():
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/No response.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
		else:
			try:
				if self.Response_Code(url) == 200:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {self.Saiu(url, test=True)}\n')
				else:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url} => {self.Saiu(url, test=True)}\n')
			except:
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
					file.write(f'{url} => {self.Saiu(url, test=True)}\n')

	def Init(self, url, case=False, thread=True):
		try:
			if not case:
				if self.Val['Cerificado SSL']:
					threading.Thread(
					    target=Validador().Certificado_SSL,
					    args=(url,)).start() if thread else Validador().Certificado_SSL(url)
				if self.Val['Sitemap']:
					threading.Thread(
					    target=Validador().Sitemap,
					    args=(url,)).start() if thread else Validador().Sitemap(url)
				if self.Val['Tag']:
					threading.Thread(
					    target=Validador().Tag,
					    args=(url,)).start() if thread else Validador().Tag(url)
				if self.Val['Recaptcha']:
					threading.Thread(
					    target=Validador().Recaptcha,
					    args=(url,)).start() if thread else Validador().Recaptcha(url)
				if self.Val['Email']:
					threading.Thread(
					    target=Validador().Email,
					    args=(url,)).start() if thread else Validador().Email(url)
				if self.Val['Sitename']:
					threading.Thread(
					    target=Validador().Sitename,
					    args=(url,)).start() if thread else Validador().Sitename(url)
				if self.Val['Status']:
					threading.Thread(
					    target=Validador().Status,
					    args=(url,)).start() if thread else Validador().Status(url)
			else:
				itens = case.strip().split(',')
				try:
					for i in itens:
						if not thread:
							if 'certificado ssl' 	== i.lower().strip(): Validador().Certificado_SSL(url)
							if 'servidor' 			== i.lower().strip(): Validador().Servidor(url)
							if 'tag' 				== i.lower().strip(): Validador().Tag(url)
							if 'sitemap' 			== i.lower().strip(): Validador().Sitemap(url)
							if 'email' 				== i.lower().strip(): Validador().Email(url)
							if 'sitename' 			== i.lower().strip(): Validador().Sitename(url)
							if 'recaptcha' 			== i.lower().strip(): Validador().Recaptcha(url)
							if 'status' 			== i.lower().strip(): Validador().Status(url)
						else:
							if 'certificado ssl' 	== i.lower().strip(): threading.Thread(target=Validador().Certificado_SSL, args=(url,)).start()
							if 'servidor' 			== i.lower().strip(): threading.Thread(target=Validador().Servidor, args=(url,)).start()
							if 'tag' 				== i.lower().strip(): threading.Thread(target=Validador().Tag, args=(url,)).start()
							if 'sitemap' 			== i.lower().strip(): threading.Thread(target=Validador().Sitemap, args=(url,)).start()
							if 'email' 				== i.lower().strip(): threading.Thread(target=Validador().Email, args=(url,)).start()
							if 'sitename' 			== i.lower().strip(): threading.Thread(target=Validador().Sitename, args=(url,)).start()
							if 'recaptcha' 			== i.lower().strip(): threading.Thread(target=Validador().Recaptcha, args=(url,)).start()
							if 'status' 			== i.lower().strip(): threading.Thread(target=Validador().Status, args=(url,)).start()
					return True
				except:
					return 'Não foi possível iniciar os módulos indicados.' if self.lang == 0 else 'We couldn\'t start the methods given.'
		except:
			return 'Não foi possível iniciar os métodos.' if self.lang == 0 else 'Unable to start modules.'
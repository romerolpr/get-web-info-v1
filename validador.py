# Choice for yout preference language 
# pt-BR = 0 / en = 1

lang = 1

from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Fore, Style
from pathlib import Path
import threading
import re
import socket

class Validador:

	def __init__(self, lang=0):
		self.lang = lang
		self.path = 'Resultados' if self.lang == 0 else 'Results'
		self.servidores = [
			'XXX.XX.XXX.XX',
			'XXX.XX.XXX.XX',
			'XXX.XX.XXX.XX',
			'XXX.XX.XXX.XX',
		]
		self.Val = {
			'Cerificado SSL' : True,
			'Tag'			 : True,
			'Sitemap'		 : True,
			'Recaptcha'		 : True,
			'Sitename'		 : True,
			'Email'		 	 : True,
		}

		Path(f'./{self.path}').mkdir(parents=True, exist_ok=True)

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
			'Dentro do servidor', 
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'Inside the server', 
			'Not recovered'
		]

		SSL = [
			'Fora do servidor', 
			'SSL ativo', 
			'SSL não ativo',
			'Não recuperado'
		] if self.lang == 0 else [
			'Off the server', 
			'SSL active', 
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
		
		return {
			'sitemap'	: Sitemap,
			'tag'		: Tag,
			'servidor'	: Servidor,
			'ssl'		: SSL,
			'recaptcha' : Recaptcha,
			'email'		: Email,
			'sitename'	: Sitename
		}[config]

	def Base(self, url, www=True):
		try:
			url = url.split('//')
			url = url[1].split('/')
			if www:
				return url[0]
			else:
				return url[0].replace('www.', '')
		except:
			return url[0]

	def Saiu(self, url, test = False):
		IP = socket.gethostbyname(self.Base(url))
		if IP not in self.servidores:
			return IP
		else:
			return False if not test else IP

	def Check_Key(self, recaptcha, url):
		with open(f'Modules/data-recaptcha/{recaptcha}.txt', 'r', encoding='utf-8') as f:
			linha = f.readlines()
			for sites in linha:
				if url in sites: return url
		return False

	def Tag(self, url):
		Def = 'tag'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
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

	def Servidor(self, url):
		Def = 'servidor' if self.lang == 0 else 'server'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write(f'{url} => {self.Saiu(url, test=True)}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Certificado_SSL(self, url):
		Def = 'ssl'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:
					request = urlopen(f"https://www.{url}/").read()
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[1] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write(f'{url}\n')
				except:
					with open(self.path + f'/{Def}/' + self.Idioma(Def)[2] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Sitemap(self, url):

		Def = 'sitemap'
		http = [ f'https://www.{url}/', f'https://{url}', f'http://{url}', f'http://www.{url}/' ]

		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:

					request = urlopen('{}sitemap.xml'.format(http[0])).read()
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
		Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
		if self.Saiu(url):
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
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
		Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
		if self.Saiu(url):
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
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
		Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
		if self.Saiu(url):
			with open(self.path + f'/{Def}/' + self.Idioma(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
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

	def Inicializa(self, url, case=False, thread=True):

		try:
			if not case:
				if self.Val['Cerificado SSL']:
					threading.Thread(
					    target=validador.Certificado_SSL,
					    args=(url,)).start() if thread else validador.Certificado_SSL(url)
				if self.Val['Sitemap']:
					threading.Thread(
					    target=validador.Sitemap,
					    args=(url,)).start() if thread else validador.Sitemap(url)
				if self.Val['Tag']:
					threading.Thread(
					    target=validador.Tag,
					    args=(url,)).start() if thread else validador.Tag(url)
				if self.Val['Recaptcha']:
					threading.Thread(
					    target=validador.Recaptcha,
					    args=(url,)).start() if thread else validador.Recaptcha(url)
				if self.Val['Email']:
					threading.Thread(
					    target=validador.Email,
					    args=(url,)).start() if thread else validador.Email(url)
				if self.Val['Sitename']:
					threading.Thread(
					    target=validador.Sitename,
					    args=(url,)).start() if thread else validador.Sitename(url)
			else:
				itens = case.strip().split(',')
				try:
					for i in itens:
						if not thread:
							if 'certificado ssl' 	== i.lower().strip(): validador.Certificado_SSL(url)
							if 'servidor' 			== i.lower().strip(): validador.Servidor(url)
							if 'tag' 				== i.lower().strip(): validador.Tag(url)
							if 'sitemap' 			== i.lower().strip(): validador.Sitemap(url)
							if 'email' 				== i.lower().strip(): validador.Email(url)
							if 'sitename' 			== i.lower().strip(): validador.Sitename(url)
							if 'recaptcha' 			== i.lower().strip(): validador.Recaptcha(url)
						else:
							if 'certificado ssl' 	== i.lower().strip(): threading.Thread(target=validador.Certificado_SSL, args=(url,)).start()
							if 'servidor' 			== i.lower().strip(): threading.Thread(target=validador.Servidor, args=(url,)).start()
							if 'tag' 				== i.lower().strip(): threading.Thread(target=validador.Tag, args=(url,)).start()
							if 'sitemap' 			== i.lower().strip(): threading.Thread(target=validador.Sitemap, args=(url,)).start()
							if 'email' 				== i.lower().strip(): threading.Thread(target=validador.Email, args=(url,)).start()
							if 'sitename' 			== i.lower().strip(): threading.Thread(target=validador.Sitename, args=(url,)).start()
							if 'recaptcha' 			== i.lower().strip(): threading.Thread(target=validador.Recaptcha, args=(url,)).start()
				except:
					return 'Não foi possível iniciar os módulos indicados.' if self.lang == 0 else 'We couldn\'t start the methods given.'
		except:
			return 'Não foi possível iniciar os métodos.' if self.lang == 0 else 'Unable to start modules.'

validador = Validador(lang)

def Validador(arquivo):  
	try:
		with open(f"{arquivo}.txt", "r", encoding='utf-8') as sites:
			linha = sites.readlines()

			desc = 'Validando links' if lang == 0 else 'Checking the links'
			arrayUrl = {
				0: [], 1: [], 2: [], 3: [], 4: []
			}

			for i, line in enumerate(linha):
				
				divide = int(len(linha)) / int(len(arrayUrl))

				if len(linha) > 500:
					if i in range((int(divide) * 0) + 0, int(divide * 1)):
						arrayUrl[0].append(line.strip('\n').strip(' '))
					if i in range((int(divide) * 1) + 1, int(divide * 2) + 1):
						arrayUrl[1].append(line.strip('\n').strip(' '))
					if i in range((int(divide) * 2) + 1, int(divide * 3) + 1):
						arrayUrl[2].append(line.strip('\n').strip(' '))
					if i in range((int(divide) * 3) + 1, int(divide * 4) + 1):
						arrayUrl[3].append(line.strip('\n').strip(' '))
					if i in range((int(divide) * 4) + 1, int(divide * 5) + 1):
						arrayUrl[4].append(line.strip('\n').strip(' '))
				else:
					arrayUrl[0].append(line.strip('\n').strip(' '))

			for Array in arrayUrl.keys():
				if len(arrayUrl[Array]) > 0:
					for url in tqdm(arrayUrl[Array], desc=desc):
						validador.Inicializa(url, thread=False)

			return True
	except:
		return False

if Validador('sites'):
	print('\nEscrevendo dados...' if lang == 0 else '\nWriting data...')
else:
	input('\nFalha.' if lang == 0 else '\nFail.')
# PT = 0
# EN = 1

lang = 0

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
			'169.57.141.90',
			'169.57.141.88',
			'169.57.141.86',
			'169.57.169.70',
			'169.57.169.72',
			'169.57.141.85',
			'169.57.169.85',
			'169.57.169.91',
			'169.57.169.73',
			'169.57.141.94',
		]
		self.Val = {
			'Cerificado SSL' : True,
			'Tag'			 : True,
			'Sitemap'		 : True,
		}

		Path(f'./{self.path}').mkdir(parents=True, exist_ok=True)

	def Set_language(self, config=False):

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
		
		return {
			'sitemap'	: Sitemap,
			'tag'		: Tag,
			'servidor'	: Servidor,
			'ssl'		: SSL	
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

	def Tag(self, url):
		Def = 'tag'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Set_language(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:
					request = urlopen(f"https://{url}/").read()
					html = BeautifulSoup(request, "html5lib");
					try:
						script = re.search(r"ga\('(create)',\s+'(.*?)',(.*?)\s+'(.*?)'\);", str(html.body)).group(2)
						with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
							file.write(f'{url}: {script}\n')
					except:
						try:
							script = re.search(r"gtag\([\"\']config[\"\'].*?[\"\'](.*?)[\"\']\);", str(html.body)).group(1)
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', 'a', encoding='utf-8') as file:
								file.write(f'{url}: {script}\n')
						except:
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
								file.write(f'{url}\n')
				except:
					with open(self.path + f'/{Def}/' + self.Set_language(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Set_language(Def)[4] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Servidor(self, url):
		Def = 'servidor' if self.lang == 0 else 'server'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Set_language(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write(f'{url} => {self.Saiu(url, test=True)}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Certificado_SSL(self, url):
		Def = 'ssl'
		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Set_language(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
					file.write('{} => {}\n'.format(url, self.Saiu(url)))
			else:
				try:
					request = urlopen(f"https://www.{url}/").read()
					with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write(f'{url}\n')
				except:
					with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', "a", -1, encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Set_language(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Sitemap(self, url):

		Def = 'sitemap'
		http = [ f'https://www.{url}/', f'https://{url}', f'http://{url}', f'http://www.{url}/' ]

		try:
			Path(f'./{self.path}/' + Def).mkdir(parents=True, exist_ok=True)
			if self.Saiu(url):
				with open(self.path + f'/{Def}/' + self.Set_language(Def)[0] + '.txt', "a", -1, encoding='utf-8') as file:
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
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => https://www\n')
						else:
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
						
					elif sitemap[1]:
						if len(sitemap[1]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => https://\n')
						else:
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
							
					elif sitemap[2]:
						if len(sitemap[2]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => http://\n')
						else:
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
								
					elif sitemap[3]:
						if len(sitemap[3]) in range(20, 10001):
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[1] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url} => http://www\n')
						else:
							with open(self.path + f'/{Def}/' + self.Set_language(Def)[2] + '.txt', "a", -1, encoding='utf-8') as arquivo:
								arquivo.write(f'{url}\n')
					else:
						with open(self.path + f'/{Def}/' + self.Set_language(Def)[3] + '.txt', 'a', encoding='utf-8') as file:
							file.write(f'{url}\n')

				except:
					with open(self.path + f'/{Def}/' + self.Set_language(Def)[4] + '.txt', 'a', encoding='utf-8') as file:
						file.write(f'{url}\n')
		except:
			with open(self.path + f'/{Def}/' + self.Set_language(Def)[5] + '.txt', 'a', encoding='utf-8') as file:
				file.write(f'{url}\n')

	def Start(self, url, case=False):
		try:
			if not case:
				if self.Val['Cerificado SSL']:
					threading.Thread(
					    target=validador.Certificado_SSL,
					    args=(url,)).start()
				if self.Val['Tag']:
					threading.Thread(
					    target=validador.Tag,
					    args=(url,)).start()
				if self.Val['Sitemap']:
					threading.Thread(
					    target=validador.Sitemap,
					    args=(url,)).start()
			else:
				itens = case.split(',')
				try:
					for i in itens:
						if i.lower() == 'certificado ssl' or itens.lower() == 'certificado ssl':
							threading.Thread(
							    target=validador.Certificado_SSL,
							    args=(url,)).start()
						if i.lower() == 'servidor' or itens.lower() == 'servidor':
							threading.Thread(
							    target=validador.Servidor,
							    args=(url,)).start()
						if i.lower() == 'saiu' or itens.lower() == 'saiu':
							threading.Thread(
							    target=validador.Saiu,
							    args=(url,)).start()
						if i.lower() == 'tag' or itens.lower() == 'tag':
							threading.Thread(
							    target=validador.Saiu,
							    args=(url,)).start()
						if i.lower() == 'sitemap' or itens.lower() == 'sitemap':
							threading.Thread(
							    target=validador.Saiu,
							    args=(url,)).start()
				except:
					res = 'Não foi possível iniciar os módulos indicados.' if self.lang == 0 else 'We couldn\'t start the methods given.'
					res += '\nIniciando validação padrão...' if self.lang == 0 else 'Starting standard modules...'
					self.Start(url, False)
		except:
			res = 'Não foi possível iniciar os métodos.' if self.lang == 0 else 'Unable to start modules.'
			
		return res

validador = Validador(lang)

def crawler(arquivo):  
	try:
		with open(f"{arquivo}.txt", "r", encoding='utf-8') as sites:
			linha = sites.readlines()
			arrayUrl = []
			for i in linha:
				arrayUrl.append(i.strip("\n").strip(" "))
			desc = 'Validando links' if lang == 0 else 'Checking the links'
			for url in tqdm(arrayUrl, desc=desc):
				validador.Start(url)
				
		return True
	except:
		return False

if crawler('sites'):
	print('\nEscrevendo dados...' if lang == 0 else '\nWriting data...')
else:
	input('\nFalha.' if lang == 0 else '\nFail.')
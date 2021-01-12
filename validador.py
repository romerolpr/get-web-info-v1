# Choice for your preference language: pt-BR = 0; en = 1

import threading, os
from tqdm.auto import tqdm
from Modules.Class.classes import Validador
from Modules.Config import *

lang = Rules['Language']
validador = Validador(lang)

def Validador(arquivo, validar=False, thread=False):  
	try:
		validar = False if 'todos' == validar.lower() else validar
		with open(f"{arquivo}.txt", "r", encoding='utf-8') as sites:
			linha = sites.readlines()

			desc = 'Verificando sites' if lang == 0 else 'Checking the sites'
			arrayUrl = {
				0: [], 1: [], 2: [], 3: [], 4: []
			}
			total = 0

			for i, line in enumerate(linha):
				
				divide = int(len(linha)) / int(len(arrayUrl))

				if len(linha) > 500:
					count = 5
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
					count = 1
					arrayUrl[0].append(line.strip('\n').strip(' '))	


			for i, Array in enumerate(arrayUrl.keys()):
				step = f'Etapa {i + 1}/{str(count)}: {desc}' if lang == 0 else f'Step {i + 1}/{str(count)}: {desc}'
				if len(arrayUrl[Array]) > 0:
					total += len(arrayUrl[Array])
					for url in tqdm(arrayUrl[Array], unit=' sites', desc=step, leave=False):
						init = validador.Init(url, case=validar, thread=thread)
					print(f"{step.split("/")[0]} -> OK" if init else init)
			return f'Total de domínios verificados: {total}' if lang == 0 else f'Domains checked: {total}'
	except:
		return False

Crawler = Validador('sites', validar='certificado ssl')

# validador.clear() 

if Crawler:
	input(f'{Crawler}\nFinalizado.' if lang == 0 else f'{Crawler}\nFinished.')
else:
	input('Erro 500: Não foi possível inicializar o sistema.' if lang == 0 else 'Error 500: We couldn\'t start the system.')
from tqdm.auto import tqdm
from ..Modules.Config import *

response = []

def to_compare(old):
	for new in Fora:
		if old in new: 
			return old
	return False

for old in tqdm(Dentro, unit=' sites', desc='Comparando sites', leave=False):
	if to_compare(old): response.append(to_compare(old))

print(f"Foram encontrados ({len(response)}) sites com possíveis trocas de apontamentos.")
for sites in response: 
	print(f" - {sites}")

input()
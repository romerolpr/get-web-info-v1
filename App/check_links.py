import os, pyperclip, urllib.request, re
import requests as r
from tqdm.auto import tqdm
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

Type = {
	# Choice for your configurations on app
	"error_404": [],
	"no_response": [],
	"tester": [],
	# Redirect tester for any links
	"redirect": False,
}

status = 0
regex = r"https?(.*)\.com(\.br)?/"

def Status(url, redirect=False):
	try:
		req = r.get(url)
		if not redirect:
			if "404" in req.url and "404" not in url: return url
		else:
			if redirect not in req.url: return req.url
		return False
	except:
		Type["no_response"].append(url)
		return False

def Tester(tester):
	try:
		desc = "404 links" if not Type['redirect'] else f"{Type['redirect']} as redirect"
		for link in tqdm(tester["tester"], unit=" sites", desc=f"Checking for {desc}", leave=False): 
			if Status(link, Type["redirect"]): Type["error_404"].append(Status(link, Type["redirect"]))

	except Exception as error:
		print(error)

	finally:

		copy = ""

		print(f"We found ({len(tester['error_404'])}) links leading to 404" if not Type["redirect"] else f"We found ({len(tester['error_404'])}) links that's not leading to {Type['redirect']}")
		domain = re.search(regex, tester['error_404'][0]).group(0)

		for a in tester['error_404']:
			links = re.sub(regex, "/", a)
			copy += "\nRewriteCond %{} ^(.*){}$\nRewriteRule ^(.*) {} [L,R=301,QSD]\n".format("{REQUEST_URI}", links, domain)
		pyperclip.copy(copy)

		if str(input("Do you wanna see all the 404 links? (y/ n) ")).lower() == "y": print(pyperclip.paste())

		if len(tester["no_response"]) > 0:
			if str(input("Do you wanna show the server's responses about the links? (y/ n) ")).lower() == "y": 
				print("Found ({}) wrong links".format(len(tester["no_response"])))
				for no_response in tester["no_response"]: print(f" {no_response}")

		return "Finished. Links already copied to the clipboard."

try:
	while status in range(4):

		if status != 3:
			file = str(input("Give a file name for the links: "))
			if os.path.isfile(f"./{file}.txt"):
				with open(f"{file}.txt", "r", encoding="utf-8") as sites:
					lines = sites.readlines()
					for i in lines: Type["tester"].append(i.strip("\n").strip())
				if len(Type["tester"]) > 0: print(Tester(Type))
				break
			else:
				print("This file \"{}\" doesn't exists. Try again.".format(file if len(file) > 0 else "undefined") if status <= 2 else "This file \"{}\" doesn't exists. You have one more chance!".format(file if len(file) > 0 else "undefined"))
				status += 1
		else:
			print("You lose. Press \"Enter\" to close.")
			break

except Exception as error:
	print(error)

input()
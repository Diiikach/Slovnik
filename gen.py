import random


vowels = [
	"а",
	"о",
	"у",
	"ы",
	"э",
	"е",
	"ё",
	"и", 
	"и",
	"ю",
	"я"
]

def get_vars(s : str) -> list[str]: 
	word = [i for i in s.lower()]
	positions = []
	for num, i in enumerate(word):
		if (i in vowels):
			positions.append(num)

	vars = []

	for pos in positions:
		nvar = ""
		for i in range(0, len(word)):
			if i == pos:
				nvar += word[i].upper()
			else:
				nvar += word[i].lower()
		vars.append(nvar)
	return vars
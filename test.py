class myInt:
	def __init__(self, val : int):
		self.val = val
	def __lt__(self, other):
		return self.val > other.val

a = myInt(1)
b = myInt(2)

vals = set()
vals.add(a)
vals.add(b)

for i in vals:
	print(i.val)
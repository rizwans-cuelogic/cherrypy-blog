def myfun(num=None):
	if not num:
		return sum(range(101))
	return sum(num)

print myfun(range(1,5))
print myfun()

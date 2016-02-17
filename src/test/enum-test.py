def nums(arg):
	numbers = {
		"zero":0,
		1:"one"
	}
	return numbers.get(arg,"invalid")

print nums("zeros")

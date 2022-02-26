# test = True

# def decorateur(funct):
# 	if test:
# 		return funct
# 	else:
# 		print("Une erreur est survenue")

# @decorateur
# def my_function():
# 	test = False
# 	print("affiche ma fonction teste")


# @decorateur
# def other_function():
# 	print("Une autre function teste")


# my_function()
# print(test)
# other_function()

my_char = 'r'

def change_char():
	print(my_char)
	my_char = 'e'
	
print(my_char)

change_char()
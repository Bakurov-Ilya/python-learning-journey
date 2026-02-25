import math

def mathematica(n, stroka):
	vse_funkcii = {
		'квадрат': n ** 2,
		'куб': n ** 3,
		'корень': n ** 0.5,
		'модуль': abs(n),
		'синус': math.sin(n)
	}
	return vse_funkcii[stroka]

print(mathematica(int(input), input()))

n = input().split()

def summa_4isel(stroka):
	k = 0
	for i in stroka:
		k+=int(i)
	return k

print(*sorted(n, key = summa_4isel))
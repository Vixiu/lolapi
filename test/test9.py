lst = [i for i in range(10)]

for i in lst:
    print(i,i - 5 if i >= 5 else i)

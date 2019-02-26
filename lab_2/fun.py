upper_limit = 50

check_list = [False for i in range(upper_limit)]

check_list[0] = True
check_list[1] = True

for i in range(2, upper_limit):
    if check_list[i] == False:
        for j in range(i+i, upper_limit, i):
            check_list[j] = True

#print(check_list)
            
result = ""

for i in range(upper_limit):
    if check_list[i] == False:
        result += str(i) + " "

        
print(result)

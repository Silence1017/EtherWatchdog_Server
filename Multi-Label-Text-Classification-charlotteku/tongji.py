from matplotlib import pyplot as plt
i=0
count = 0
len_list = []
with open("./data/test.txt",'r',encoding='utf-8') as file:
    while True:
        line = file.readline()
        if not line:
            break
        count += 1
        if count % 1000 == 0:
            print(count)
            print("----------")
            #print(line)
            print("----------")
        len_list.append(len(line.split(" ")))
        if len(line.split(" "))<3000:
            i+=1
            print(len(line.split(" ")))
print(count)
print(len_list)
print(len(len_list))
print(i)
plt.hist(len_list,100)
plt.xlabel('Sequence Length')
plt.ylabel('Frequency')
plt.axis([0,4000,0,800])
#plt.axis([0,1000,0,500000])
#plt.axis([1000,7000,0,200])
#plt.axis([7000,12000,0,1500])
#plt.axis([12000,20000,0,2000])
#plt.axis([20000,60000,0,2000])
plt.show()

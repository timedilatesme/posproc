
import random 
l = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
#random.choices([0, 1], k=10)
print("Unshuffled: ",l)


mylist = random.choices([0,1],k=10)
random.shuffle(mylist)

print(mylist)
random.shuffle(mylist)
print(mylist)
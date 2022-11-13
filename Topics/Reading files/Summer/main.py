file = open('/home/sysadmin/PycharmProjects/Web Calendar1/Topics/Reading files/Summer/data/dataset/input.txt', 'r')
count = 0
for line in file:
    if line == 'summer\n':
        count += 1
print(count)



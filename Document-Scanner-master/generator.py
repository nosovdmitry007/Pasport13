import os

file = os.listdir('data/test')
print(file)
t = 0
lines = []
f = open('data/gt_test.txt', 'w', encoding='UTF-8')


for i in file:
    put = i.split('_')[0]
    t += 1
    new_f = str(t) + '.jpg'
    os.rename('data/test/' + i, 'data/test/' + new_f)
    line = str(t) + '.jpg;' + put+'\n'
    f.write(line)
    lines.append(line)
    print(line)
#
# f = open('gt.txt','w') /home/dima/PycharmProjects/Pasport13/Document-Scanner-master/all_data/ru_train_filtered
# f.write("\n".join(lines).join("\n"));
# print(lines)

#/home/dima/PycharmProjects/Pasport13/Document-Scanner-master/all_data/ru_train_filtered

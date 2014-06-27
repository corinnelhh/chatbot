pos_str = ""
with open('doctorow.txt', 'r') as f:
    pos_str = f.read()
pos_dict = eval(pos_str)

for k, v in pos_dict.items():
    pos = {}
    for i in v:
        if i not in pos:
            pos[i] = 1
        else:
            pos[i] += 1
    pos_dict[k] = pos

for k, v in pos_dict.items():
    pos_list = []
    for pos, count in v.items():
        pos_list.append((count, pos))
    pos_list.sort(reverse=True)
    pos_dict[k] = pos_list

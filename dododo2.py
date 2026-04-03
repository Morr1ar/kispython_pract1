# 2.4
print('№ 2.4')
i = 0
'muchcodewow'[i::3] # 19 символа




# 5.3
print('№ 5.3')
from functools import cache

@cache
def lev_dist(a, b):
    if not a or not b:
        return max(len(a), len(b))
    
    if a[0] == b[0]:
        return lev_dist(a[1:], b[1:])
    
    return 1 + min(
        lev_dist(a, b[1:]),
        lev_dist(a[1:], b),
        lev_dist(a[1:], b[1:])
    )

print(lev_dist('столб', 'слон'))



# 5.4
print('№ 5.4')
from functools import cache

@cache
def lev_dist_ops(a, b, i=None, j=None):
    if i is None:
        i = len(a)
    if j is None:
        j = len(b)
    
    if i == 0 and j == 0:
        return 0, []
    if i == 0:
        return j, ['вставка'] * j
    if j == 0:
        return i, ['удаление'] * i
    
    if a[i-1] == b[j-1]:
        dist, ops = lev_dist_ops(a, b, i-1, j-1)
        return dist, ops
    
    insert_dist, insert_ops = lev_dist_ops(a, b, i, j-1)
    delete_dist, delete_ops = lev_dist_ops(a, b, i-1, j)
    replace_dist, replace_ops = lev_dist_ops(a, b, i-1, j-1)
    
    min_dist = min(insert_dist, delete_dist, replace_dist)
    
    if replace_dist == min_dist:
        ops = replace_ops.copy()
        ops.append('замена')
        return replace_dist + 1, ops
    elif delete_dist == min_dist:
        ops = delete_ops.copy()
        ops.append('удаление')
        return delete_dist + 1, ops
    else:
        ops = insert_ops.copy()
        ops.append('вставка')
        return insert_dist + 1, ops

print(lev_dist_ops('столб', 'слон'))

def get_operations(a, b):
    _, ops = lev_dist_ops(a, b)
    return list(ops)

print(get_operations('столб', 'слон'))

# 5.5
print('№ 5.5')
def lev_dist_gen(source, target):
    ops = get_operations(source, target)
    
    source_list = list(source)
    target_list = list(target)
    
    commands = []
    pos = 0 # текущая позиция
    
    for op in ops:
        while source_list[pos] == target_list[pos]:
            pos += 1
        
        if op == 'удаление':
            commands.append(f"del x[{pos}]")
            del source_list[pos]
            
        elif op == 'вставка':
            val = target_list[pos]
            commands.append(f"x.insert({pos}, y[{pos}])")
            source_list.insert(pos, val)
            pos += 1
            
        elif op == 'замена':
            val = target_list[pos]
            commands.append(f"x[{pos}] = y[{pos}]")
            source_list[pos] = val
            pos += 1
    
    print(source_list)
    return commands
    
print(get_operations('достаток', 'остаточный'))
print('\n'.join(lev_dist_gen('достаток', 'остаточный')))

'''
# 5.6
print('№ 5.6')
def spell(s):
    result = []
    with open('words.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    with open('words.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for word in s.split():
        if word in content:
            result.append(word)
            continue
        
        isInLev = True
        max_pop = 0
        pred_dist = 3
        for line in lines:
            dist = lev_dist(word, line.split()[0])
            if dist in [1, 2]:
                if dist == 1:
                    if int(line.split()[1]) > max_pop:
                        pred_dist = 1
                        max_pop = int(line.split()[1])
                        lev_word = line.split()[0]
                    elif pred_dist >= 2:
                        pred_dist = 1
                        max_pop = int(line.split()[1])
                        lev_word = line.split()[0]
                        continue
                elif dist == 2:
                    if pred_dist >= 2 and int(line.split()[1]) > max_pop:
                        pred_dist = 2
                        max_pop = int(line.split()[1])
                        lev_word = line.split()[0]
                        continue
        if max_pop:
            result.append(lev_word)
            continue
        else:
            result.append(word)
            continue

    return ' '.join(result)

print(spell('помоему я напесал усё правильна'))
'''


# 2.5
print('№ 2.5')
lst = ['a', 'b', 'c']
lst += 'd'
print(lst)

lst = lst + ['d'] # Ошибка?!
print(lst)

lst += [42]
print(lst) # Ошибка?!







# 3.9
print('№ 3.9')
from itertools import groupby

rle_encode = lambda s: [(ch, sum(1 for _ in grp)) for ch, grp in groupby(s)]

print(rle_encode('ABBCCCDEF'))



print('№ 4.3')
MASK32 = 0xFFFFFFFF
DELTA = 0x9E3779B9


def tea_decrypt_block(v0, v1, k):
    k0, k1, k2, k3 = k
    s = 0xC6EF3720
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & MASK32
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & MASK32
        s = (s - DELTA) & MASK32
    return v0, v1


cipher_hex = '''
E3238557 6204A1F8 E6537611 174E5747
5D954DA8 8C2DFE97 2911CB4C 2CB7C66B
E7F185A0 C7E3FA40 42419867 374044DF
2519F07D 5A0C24D4 F4A960C5 31159418
F2768EC7 AEAF14CF 071B2C95 C9F22699
FFB06F41 2AC90051 A53F035D 830601A7
EB475702 183BAA6F 12626744 9B75A72F
8DBFBFEC 73C1A46E FFB06F41 2AC90051
97C5E4E9 B1C26A21 DD4A3463 6B71162F
8C075668 7975D565 6D95A700 7272E637
'''

key = [0, 4, 5, 1]
words = [int(x, 16) for x in cipher_hex.split()]

decoded_chars = []
for i in range(0, len(words), 2):
    a, b = tea_decrypt_block(words[i], words[i + 1], key)
    decoded_chars.extend([chr(a), chr(b)])

print(''.join(decoded_chars))


















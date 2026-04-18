from collections import defaultdict

from aioitertools import combinations


def get_1item_set(buy_list, min_count):
    counts = defaultdict(int)
    for item_set in buy_list:
        for item in item_set:
            counts[frozenset([item])]+=1
    return {k:v for k,v in counts.items() if v>=min_count}

def get_bigger_item_set( buy_list, min_count,k,temp):

    old_keys = list(temp.keys())
    candidates = set()
    counts = defaultdict(int)

    for i in range(len(old_keys)-1):
        for j in range(i+1, len(old_keys)):
            candidate = old_keys[i]|old_keys[j] #candidate = {1,2,3} 이런 애일테고
            if len(candidate)==k:
                flag=1
                for c in candidate:
                    valid_c = candidate-{c}
                    if valid_c not in old_keys:
                        flag=0
                if flag:
                    candidates.add(candidate)
    for item_set in buy_list:
        for c in candidates:
            if c.issubset(item_set):
                counts[c]+=1

    return {k:v for k,v in counts.items() if v>=min_count}


def get_all_item_set(buy_list, min_count):
    item_sets=[]
    temp=get_1item_set(buy_list,min_count)
    item_sets.append(temp)
    k=2
    while 1:
        temp=get_bigger_item_set(buy_list,min_count,k,temp)
        if temp:
            item_sets.append(temp)
            k+=1
        else:
            break

    return item_sets

item_sets = get_all_item_set([], 3)
tmp=dict()
for sets in item_sets:
    tmp.update(sets)

for k,v in tmp.items():
    if len(k)==1:
        print(f"frequent item set {k} support is {v}")
    else:
        for i in range(1,len(k)):
            combs = combinations(k,i)
            for c in combs:
                c = frozenset(list(c))
                print(f"frequent item set {k} support is {v} and confidence{c}->{k-c}  is {v/tmp[c] *100}")








                    

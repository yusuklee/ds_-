import math
import sys
from collections import Counter, defaultdict

def read_data(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    header = lines[0].split('\t')
    data = [line.split('\t') for line in lines[1:]]
    return header, data


def entropy(labels):
    total = len(labels)
    counter = Counter(labels) # [1:10, 0:2] 이렇게
    if len(counter)==1:
        return 0
    tmp=0
    for c in counter.values():
        p = c/total
        tmp-=p*math.log2(p)
    return tmp

def gini(labels):
    total = len(labels)
    counter=  Counter(labels)
    if len(counter)==1:
        return 0
    tmp=0
    for c in counter.values():
        p=c/total
        tmp+=p*p
    return 1-tmp


def majority(data, label_idx):
    datas = [a[label_idx] for a in data]
    counter = Counter(datas)
    return counter.most_common(1)[0][0]



def gini_info_gain(data,attr,label_idx):
    parent_labels = [row[label_idx] for row in data]  #[1,1,1,0,0]
    par_score = gini(parent_labels)
    attr_vals = set([row[attr] for row in data ])
    if len(attr_vals)==1:
        return 0
    tmp = defaultdict(list)
    total_len = len(parent_labels)
    child_score=0
    for row in data:
        tmp[row[attr]].append(row[label_idx])

    for val in tmp.values():
        if len(val)==0:
            continue
        가중치 = len(val)/total_len
        child_score+=가중치*gini(val)

    return par_score-child_score

def entropy_info_gain(data,attr, label_idx):
    parent_labels = [row[label_idx] for row in data]
    par_score = entropy(parent_labels)
    attr_vals = set([row[attr] for row in data])
    if len(attr_vals)==1:
        return 0
    tmp = defaultdict(list)
    total_len = len(parent_labels)
    child_score = 0
    for row in data:
        tmp[row[attr]].append(row[label_idx])

    for val in tmp.values():
        if len(val) == 0:
            continue
        가중치 = len(val) / total_len
        child_score += 가중치 * entropy(val)

    return par_score-child_score

def build_tree(data, label_idx, available_attrs):
    labels = set([i[label_idx] for i in data])
    if len(labels)==1:
        return data[0][label_idx]
    if len(available_attrs)<=0:
        return majority(data,label_idx)
    best_score = 0
    best_attr=None
    for att in available_attrs:
        score = gini_info_gain(data,att,label_idx)
        if score>best_score:
            best_score=score
            best_attr=att

    if best_score==0:
        return majority(data,label_idx)

    part = defaultdict(list)
    vals = set([i[best_attr] for i in data])
    children = {}

    if len(vals)==1:
        return majority(data,label_idx)
    for row in data:
        part[row[best_attr]].append(row) #part = {A:[data들], B:[data들]...}
    for i in list(vals):
        children[i] = build_tree(part[i], label_idx, available_attrs-{best_attr})

    return {
        "data":data,
        "split_attr":best_attr,
        "children":children

    }



def build_tree2(data, label_idx, available_attrs):
    labels = set([i[label_idx] for i in data])
    if len(labels)==1:
        return data[0][label_idx]
    if len(available_attrs)<=0:
        return majority(data,label_idx)
    best_score = 0
    best_attr=None
    for att in available_attrs:
        score = entropy_info_gain(data,att,label_idx)
        if score>best_score:
            best_score=score
            best_attr=att

    if best_score==0:
        return majority(data,label_idx)

    part = defaultdict(list)
    vals = set([i[best_attr] for i in data])
    children = {}

    if len(vals)==1:
        return majority(data,label_idx)
    for row in data:
        part[row[best_attr]].append(row) #part = {A:[data들], B:[data들]...}
    for i in list(vals):
        children[i] = build_tree2(part[i], label_idx, available_attrs-{best_attr})

    return {
        "data":data,
        "split_attr":best_attr,
        "children":children

    }

def pred_data(row,tree,label_idx):
    if isinstance(tree, str):  #
        return tree

    if row[tree['split_attr']] in tree['children']:
        return pred_data(row,tree['children'][row[tree['split_attr']]],label_idx)
    else:
        return majority(tree['data'],label_idx)


def main():
    if len(sys.argv) != 4:
        print("Usage: python dt.py <train_file> <test_file> <output_file>")
        sys.exit(1)

    train_file, test_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

    train_header, train_data = read_data(train_file)
    label_idx = len(train_header) - 1
    class_name = train_header[label_idx]
    attributes = set(range(label_idx))

    tree = build_tree(train_data, label_idx, attributes)  # gini 기준

    test_header, test_data = read_data(test_file)

    with open(output_file, 'w') as f:
        f.write('\t'.join(test_header + [class_name]) + '\n')
        for row in test_data:
            prediction = pred_data(row, tree, label_idx)
            f.write('\t'.join(row + [prediction]) + '\n')


if __name__ == '__main__':
    main()








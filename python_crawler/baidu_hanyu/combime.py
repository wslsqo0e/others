import sys

def read_cc(cc, dd):
    key = None
    value = []
    for i in open(cc, encoding='utf8'):
        ii = i.strip()
        if ii.startswith('+'):
            if key:
                if key in dd:
                    if len(value) > len(dd[key]):
                        dd[key] = value
                else:
                    dd[key] = value
            key = ii
            value = []
        else:
            value.append(ii)
    if key:
        if key in dd:
            if len(value) > len(dd[key]):
                dd[key] = value
        else:
            dd[key] = value

if __name__ == '__main__':
    total_dd = {}
    out = open("total_out.txt", 'w', encoding='utf8')
    for i in sys.argv[1:]:
        print(i)
        read_cc(i, total_dd)
    ll = sorted(total_dd.items())
    for i in ll:
        out.write(i[0]+'\n') 
        for w in i[1]:
            out.write('\t{}\n'.format(w))

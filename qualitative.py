import numpy as np 
import jamotools 


def qualitative(argtext, arguni):
    standards = np.genfromtxt('./data_qualitative/학생종합채점표.xlsx', delimiter=',')
    v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_1, max_length=None, prefix_padding_size=0)
    text = v.vectorize(argtext)
    category = ['학업역량', '전공적합성', '인성', '발전가능성']
    for c in category: 
        print(standards[c])



if __name__ == '__main__':
    text = np.loadtxt('./data_qualitative/서가연_양지고등학교_여.txt')
    qualitative(text, '서울대학교')
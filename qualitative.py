import numpy as np 
import pandas as pd 
import jamotools 
from scipy.spatial import distance as dis
import argparse

def qualitative(text, uni):
    f = open('./data_qualitative/standard.txt', 'r')
    dfstandard = pd.read_csv(f, delimiter='\t')
    v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_1, max_length=None, prefix_padding_size=0)
    vectext = v.vectorize(text)

    category = ['학업역량', '전공적합성', '인성', '발전가능성']
    scores = []
    for c in category: 
        question = ''
        df = dfstandard.loc[dfstandard.index[dfstandard.iloc[:,0]==c].tolist()].iloc[:,2]
        for i,value in df.iteritems():
            question += value+'\n'
        vecques = v.vectorize(question)
        ml = max(len(vectext), len(vecques))
        vectext = np.concatenate((vectext, np.zeros(ml-len(vectext))))
        vecques = np.concatenate((vecques, np.zeros(ml-len(vecques))))
      
        score = 1 - dis.cosine(vectext, vecques)
        score = score * 40
        if score >= 5.0: score = 5.0
        # score = dis.euclidean(vectext, vecques)
        scores.append(score)

    # TODO fetch evaluation from DB 
    evaluation = 'NULL'
    scores = dict(zip(category, scores))
    return scores, evaluation



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--text_path', type=str, default='./data_qualitative/sample_01.txt')
    parser.add_argument('--university', type=str, default='서울대학교')

    args = parser.parse_args()

    text = open(args.text_path, 'r').read()
    print(qualitative(text, args.university))
    

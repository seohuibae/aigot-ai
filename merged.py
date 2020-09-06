import numpy as np 
import pandas as pd 
import jamotools 
from scipy.spatial import distance as dis
from scipy.stats import norm
import argparse

import math


def qualitative(user_text, uni_eval_text):
    f = open('./data_qualitative/standard.txt', 'r')
    dfstandard = pd.read_csv(f, delimiter='\t')
    v = jamotools.Vectorizationer(rule=jamotools.rules.RULE_1, max_length=None, prefix_padding_size=0)
    vectext = v.vectorize(user_text)

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
    evaluation = uni_eval_text 
    scores = dict(zip(category, scores))
    return scores, evaluation

def retrieve_probability(uni_score_min, user_score):
    mu = uni_score_min
    std = abs(1-mu)/3
    probability = (1 - norm.cdf(user_score, mu, std)) * 100
    if probability > 95.0: probability = 95.0

    return probability

def merged_func(user_value, user_text, uni_score_min, uni_eval_text):

    probability = retrieve_probability(uni_score_min, user_score)  # 0-100
    scores, evaluation = qualitative(user_text, uni_eval_text) #0-5
    scores_copied = list(scores.values())

    c = np.mean(scores_copied)/5-probability/100

    if c > 0 and c > 0.05: # increase probabiilty if score is too high 
        probability += c*100 

    return probability, scores, evaluation




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--user_text_path', type=str, default='./data_qualitative/sample_01.txt')
    parser.add_argument('--university', type=str, default='서울대학교')
    parser.add_argument('--category', type=str, default='기회균등')
    parser.add_argument('--department', type=str, default='경영학부')
    parser.add_argument('--major', type=str, default='경영학과')
    parser.add_argument('--user_score', type=float, default=1.34)
    args = parser.parse_args()

    user_text = open(args.user_text_path, 'r').read()
    user_score = args.user_score

    # TODO retrieve uni_score_min and uni_eval_text from DB from users' input
    # [uni_score_min] input: university, category, department, major
    # [uni_eval_text] input: university, category 
    
    uni_score_min = 1.56
    uni_eval_text = 'NULL'

    probability, scores, evaluation = merged_func(user_score, user_text, uni_score_min, uni_eval_text)
    
    print(probability, scores, evaluation)
    
    

# encoding=utf8

"""
对复旦大学的文本语料库做实验
"""
import numpy as np
import os
from wordweight import WordWeightEvaluation
import cmpcluster
from CommunityBuilder import CommunityBuilder
def out_result_header():
    return 'NCluster \tARI \tANMI \tFM  \tVM\n'

def cmp_cluster(predicted, real_labels):
    ncluster = len(set(predicted))
    adjr = cmpcluster.cmp_doc_clusters(predicted,real_labels, 'rand')
    nmi = cmpcluster.cmp_doc_clusters(predicted,real_labels,'nmi')
    fm = cmpcluster.cmp_doc_clusters(predicted,real_labels,'f-measure')
    vm = cmpcluster.cmp_doc_clusters(predicted,real_labels, 'v-measure')
    return [ncluster, adjr,nmi,fm,vm]
    
def mean_std(metrics):
    A = np.array(metrics)
    mean = np.mean(A, axis=0).tolist()
    std = np.std(A,axis=0).tolist()
    return (mean,std)

def main():
    import pretext
    import extract_keyword2
    import worddf
    dbfile = '../data/sougou.db'
    logsteadyfile = '../result/sougou.log'
    
    steadyfile = open(logsteadyfile,'w')
    steadyfile.write(out_result_header())
    
    if not os.path.exists(dbfile):
        pretext.load_topiclist(dbfile,'/home/cs/download/cluster_data/sougou')
        eva = WordWeightEvaluation(30,'../data/worddf')
        ke = extract_keyword2.DBKeywordExtractor(dbfile,eva)
        ke.init_db()
        ke.content_keyword()
        ke.title_keyword()
        ke.topic_keyword()
        ke.close_db()


    cb = CommunityBuilder(dbfile)
    
    metrics = list()
    c = 1
    real = cmpcluster.load_doc_labels(dbfile)
    print 'fudan'
    for i in range(c):
        print 'Time %d' % (i+1)
        predicted = cb.build(max_depth=5, min_doc_num=20)
        metrics.append(cmp_cluster(predicted,real))
    
    mean,std = mean_std(metrics)
    meanstr = '%.1f \t%.3f \t%.3f \t%.3f \t%.3f\n' % tuple(mean)
    stdstr =  '%.1f \t%.3f \t%.3f \t%.3f \t%.3f\n' % tuple(std)
    steadyfile.write(meanstr)
    steadyfile.write(stdstr)
    steadyfile.close()
    os.system('emacs '+logsteadyfile)

if __name__ == '__main__':
    main()
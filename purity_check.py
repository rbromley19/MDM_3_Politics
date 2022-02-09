import pandas as pd
import numpy as np

def purity_check(labels,data):
    purity_check = pd.DataFrame({'Cluster Labels' : labels})
    purity_check['Vote'] = data['generalElectionVote']
    cluster_purity_list=[]
    for cluster in range(n_clusters):
    
        vote_list = []
        for x in range(purity_check.shape[0]):
            if purity_check.loc[x,'Cluster Labels'] == cluster:
                vote_list.append(data.loc[x,'generalElectionVote'])
        vote_list_data_frame = pd.DataFrame({'Assignment':vote_list})
        cluster_purity_list.append(max(vote_list_data_frame['Assignment'].value_counts(normalize=True)))

    mean_purity = np.mean(cluster_purity_list)
    return mean_purity
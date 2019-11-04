from sklearn.neighbors import DistanceMetric
import pandas as pd
import json
from dist_definition import my_dist


votes = pd.read_csv('data/votes.csv', index_col=0, dtype=str)
votes = votes.where(lambda x: x!='Nieobecny', 0).applymap(hash)

votes = votes.head(800)
names = votes.columns

dist = DistanceMetric.get_metric('pyfunc', func=my_dist)
dist_matrix = dist.pairwise(votes.T)
dist_matrix = pd.DataFrame(dist_matrix)

with open('data/deputies.json', 'r') as f:
    deputies = json.load(f)


def select_club(name):
    ## TODO: przejrzec nazwiska, pewnie jest tego wiecej.
    if not name == 'Szynkowski vel Sęk Szymon':
        name = name.split(' ')
        name = name[1] + ' ' + name[0]
    else:
        name = 'Szymon Szynkowski vel Sęk'
    return deputies.get(name, 'INNY')


clubs = names.to_series().apply(select_club)
rm = clubs[clubs == 'INNY'].index.tolist()

dist_matrix.columns = names
dist_matrix.index = names
dist_matrix.drop(rm, axis=1).drop(rm, axis=0).to_csv('data/dist.txt', index=False, header=False)

clubs.name = 'club'
pd.DataFrame(clubs).drop(rm).reset_index().to_csv('data/names_clubs.csv', index=False)
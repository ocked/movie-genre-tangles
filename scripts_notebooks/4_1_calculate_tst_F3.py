import pickle
from tangles.convenience import search_tangles
from tangles.search.progress import DefaultProgressCallback
from movie_genre_tangles.convenience import *

seps, _ = csv_to_setseperationsystem("../data/data_F3.csv")

with open("../orders/orders_O12_K3", "rb") as f:
    order_O12 = pickle.load(f)

sw = search_tangles(seps, 3, 140, np.argsort(order_O12), DefaultProgressCallback())
tm = sw.tree.tangle_matrix(3)
intersting_umbrella_tm_K3 = calc_interesting_umbrella_tm(tm)

with open("../results/interesting_umbrella_tm_K3.pkl", "wb") as f:
    pickle.dump(intersting_umbrella_tm_K3, f)
sw.tree.save("../results/tst_O12_K3")

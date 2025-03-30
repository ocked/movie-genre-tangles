import sys

sys.path.append("..")
import pickle
from tangles.convenience import search_tangles
from tangles.search.progress import DefaultProgressCallback
from tangles.movietangles.convenience import *

seps, _ = csv_to_setseperationsystem("../data/data_K10.csv")

with open("../orders/orders_O12_K10", "rb") as f:
    order_O12 = pickle.load(f)

sw = search_tangles(seps, 10, 650, np.argsort(order_O12), DefaultProgressCallback())
tm = sw.tree.tangle_matrix(10)
intersting_umbrella_tm_K10 = calc_interesting_umbrella_tm(tm)

with open("../results/interesting_umbrella_tm_K10.pkl", "wb") as f:
    pickle.dump(intersting_umbrella_tm_K10, f)
sw.tree.save("../results/tst_O12_K10")

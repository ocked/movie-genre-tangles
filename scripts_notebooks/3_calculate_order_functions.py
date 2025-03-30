import pickle

from movie_genre_tangles.entropy import O12
from movie_genre_tangles.convenience import csv_to_setseperationsystem

with open("../data/data_K3.csv", "r") as f:
    seps, _ = csv_to_setseperationsystem("../data/data_K3.csv")
orders_O12_K3 = O12(seps)
with open("../orders/orders_O12_K3", "wb") as f:
    pickle.dump(orders_O12_K3, f)
with open("../data/data_K10.csv", "r") as f:
    seps_K10, _ = csv_to_setseperationsystem("../data/data_K10.csv")
orders_O12_K10 = O12(seps_K10)
with open("../orders/orders_O12_K10", "wb") as f:
    pickle.dump(orders_O12_K10, f)
with open("../data/data_K24.csv", "r") as f:
    seps_K24, _ = csv_to_setseperationsystem("../data/data_K24.csv")
orders_O12_K24 = O12(seps_K24)
with open("../orders/orders_O12_K24", "wb") as f:
    pickle.dump(orders_O12_K24, f)

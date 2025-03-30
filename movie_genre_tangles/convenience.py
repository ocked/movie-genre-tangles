import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
from tangles.separations import SetSeparationSystem


def csv_to_setseperationsystem(filepath: str) -> Tuple[np.array, list]:
    """Generates a seperationsystem as a matrix from a csv file.

    Args:
        filepath (str): Path to the csv file. File has to have colomn "keywords"

    Returns:
        np.array: Matrix, where each row corresponts to a row of the file and each colomn corresponts to a (set of) keyword(s).
        list: list[i] contains the keywords corresponding to the i-th colomn of the matrix.
    """
    data = pd.read_csv(filepath)
    data["keywords"] = data["keywords"].apply(lambda x: ast.literal_eval(x))

    idtokeyword = data.explode("keywords")["keywords"].unique()
    keywordtoid = {keyword: np.where(idtokeyword == keyword) for keyword in idtokeyword}

    seps = -np.ones((len(data), len(idtokeyword)))
    for i in data.index:
        for keyword in data.loc[i, "keywords"]:
            seps[i, keywordtoid[keyword]] = 1

    sepsys = SetSeparationSystem(len(data))
    sepsys.add_seps(seps, metadata=idtokeyword)
    seps = sepsys.__getitem__(sepsys.all_sep_ids())

    sepidtokeyword = []
    for i in range(len(sepsys.sep_metadata)):
        eintrag = sepsys.sep_metadata[i]
        sepidtokeyword.append([eintrag.info])
        while eintrag.next != None:
            eintrag = eintrag.next
            sepidtokeyword[i].append(eintrag.info)
    return seps, sepidtokeyword


def calc_interesting_umbrella_tm(tangle_matrix: np.array) -> np.array:
    """returns a tangle matrix only containing interesting umbrella tangels"

    Args:
        tangle_matrix (np.array): original tangle matrix, is assumed to have agreement value at least 3.

    Returns:
        np.array: new tangle matrix containing only interesting umbrella tangles
    """
    tm = tangle_matrix.copy()
    interesting_tangles = [i for i in range(tm.shape[0]) if (tm[i] == 1).sum() >= 3]
    interesting_tm = tm[interesting_tangles]
    ones_positions = [set(np.where(row == 1)[0]) for row in interesting_tm]
    mask = np.ones(len(ones_positions), dtype=bool)
    for i in range(len(ones_positions)):
        for j in range(len(ones_positions)):
            if i != j and ones_positions[i].issubset(ones_positions[j]):
                mask[i] = False
    interesting_umbrella_tm = interesting_tm[mask]
    return interesting_umbrella_tm


def printkeywordsfromtm(
    tanglematrix: np.array, tangleid: int, metadata_lvls: list
) -> None:
    """Prints metadata of positive sides of the tangle in row tangleid of tanglematrix.

    Args:
        tanglematrix (np.array): tanglematrix containing the tangle. It's rows are tangles and it's columns seperations.
        tangleid (int): Row of the tangle in question
        metadata_lvls (list): metadata of seperations. metadata_lvls[i] is assumed to contian metadata of seperation at level i.
    """
    print("tangle: ", tangleid)
    for t in np.where(tanglematrix[tangleid] == 1)[0]:
        print(metadata_lvls[t])


# --- needed below?


def treetotangles(tree, agreement, metadata):
    print("Es wurden ", len(tree._sep_ids), " Schlagwörter betrachtet")
    tangle_mat = tree.tangle_matrix(agreement)
    positive = np.count_nonzero(tangle_mat == 1, axis=1)
    print("Präinteresannte Tangle sind: ")
    i = 0
    for n in np.where(positive == 2)[0]:
        print("Tangle ", n, ": ")
        printkeywordsformtangle(tree, tangle_mat, n, metadata)
        i += 1
    print("Es gibt ", i, " präinteresante Tangles")
    i = 0
    print("Interesannte Tangle sind: ")
    for n in np.where(positive >= 3)[0]:
        print("Tangle ", n, ": ")
        printkeywordsformtangle(tree, tangle_mat, n, metadata)
        i += 1
    print("Es gibt ", i, " interesante Tangles")


def show_interesting_tangle(tree, agreement):
    mat = tree.tangle_matrix(agreement)
    plt.matshow(mat[np.sum(mat == 1, axis=1) >= 3])
    plt.show


def corpus_to_genrecounter(
    movies: pd.DataFrame, corpora: np.ndarray, tangleid: int
) -> pd.Series:
    return (
        movies["genres"][corpora[:, tangleid] == 1].explode().value_counts()
        / (corpora[:, tangleid] == 1).sum()
    )


def plot_genre_mat(movies, corpora, tangles):
    df = pd.DataFrame({t: corpus_to_genrecounter(movies, corpora, t) for t in tangles})
    fig = plt.matshow(df, cmap="YlGnBu")
    plt.yticks(ticks=range(len(df.index)), labels=df.index)
    plt.xticks(ticks=range(len(tangles)), labels=tangles, rotation=90)
    return fig

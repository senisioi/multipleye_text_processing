import sys
import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import RobustScaler

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, cophenet, dendrogram
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

from language_constants import LANG_COLORS


in_file = sys.argv[1] if len(sys.argv) > 1 else "stats_page.csv"
out_dir = os.path.join('trees', in_file.replace(".csv", "_results"))
print("Saving results to:", out_dir)
os.makedirs(out_dir, exist_ok=True)

df = pd.read_csv(in_file)

# remove empty trailing rows
df = df.dropna(subset=["Language"]).copy()

langs = df["Language"].tolist()
languages_to_remove = ["Swiss German", "Romansh"]# "Kallalisutit", "Cantonese"]
df = df[~df["Language"].isin(languages_to_remove)].copy()
langs = df["Language"].tolist()

# Only the requested features
feature_cols = [
    "Page@num. types",              # average number of unique words per page
    "Page@function words ratio",    # percentage of function words
    "Page@word length",             # average word length
    #"Page@type token ratio"
]

# ==========================
# REFERENCE TAXONOMY
# ==========================

taxonomy = {
    "English":("IE","Germanic","West","Anglo-Frisian"),
    "German":("IE","Germanic","West","High German"),
    #"Swiss German":("IE","Germanic","West","High German"),
    "Dutch":("IE","Germanic","West","Low Franconian"),
    "Danish":("IE","Germanic","North","Scandinavian"),
    "Swedish":("IE","Germanic","North","Scandinavian"),
    "Norwegian":("IE","Germanic","North","Scandinavian"),

    "Catalan":("IE","Romance","Western","Occitano-Romance"),
    "Spanish":("IE","Romance","Western","Ibero-Romance"),
    "Portuguese":("IE","Romance","Western","Ibero-Romance"),
    "Galician":("IE","Romance","Western","Ibero-Romance"),
    "Italian":("IE","Romance","Italo-Dalmatian",None),
    "Romansh":("IE","Romance","Rhaeto-Romance",None),
    "Romanian":("IE","Romance","Eastern","Balkan"),

    "Slovenian":("IE","Slavic","South","West"),
    "Croatian":("IE","Slavic","South","West"),
    "Serbian":("IE","Slavic","South","West"),
    "Macedonian":("IE","Slavic","South","East"),
    "Polish":("IE","Slavic","West",None),
    "Czech":("IE","Slavic","West",None),
    "Russian":("IE","Slavic","East",None),
    "Ukrainian":("IE","Slavic","East",None),

    "Lithuanian":("IE","Baltic",None,None),
    "Latvian":("IE","Baltic",None,None),

    "Finnish":("Uralic","Finnic",None,None),
    "Estonian":("Uralic","Finnic",None,None),

    "Greek":("IE","Hellenic",None,None),
    "Albanian":("IE","Albanian",None,None),

    "Hindi":("IE","Indo-Iranian","Indo-Aryan",None),
    "Urdu":("IE","Indo-Iranian","Indo-Aryan",None),
    "Farsi":("IE","Indo-Iranian","Iranian",None),

    "Turkish":("Turkic","Oghuz",None,None),

    "Arabic":("Afroasiatic","Semitic",None,None),
    "Hebrew":("Afroasiatic","Semitic",None,None),
    "Hausa":("Afroasiatic","Chadic",None,None),

    "Mandarin":("Sino-Tibetan","Sinitic",None,None),
    "Cantonese":("Sino-Tibetan","Sinitic",None,None),

    "Basque":("Basque",None,None,None),
    "Kalaallisut":("Eskaleut","Inuit",None,None)
}


# ==========================
# GOLD DISTANCE MATRIX
# ==========================

def shared_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x is None or y is None or x != y:
            break
        n += 1
    return n

gold_dist = []

for i in range(len(langs)):
    for j in range(i + 1, len(langs)):
        a = taxonomy.get(langs[i], (None, None, None, None))
        b = taxonomy.get(langs[j], (None, None, None, None))
        gold_dist.append(4 - shared_prefix(a, b))

gold_dist = np.array(gold_dist, dtype=float)


# ==========================
# PREPROCESS FEATURES
# ==========================

df[feature_cols].to_csv(out_dir + "/selected_features_raw.csv", index=False)
X = df[feature_cols].astype(float)
#X = SimpleImputer(strategy="median").fit_transform(X)
X = RobustScaler().fit_transform(X)
#X = StandardScaler().fit_transform(X)


# ==========================
# BUILD TREE AND SCORE
# ==========================

euclid = pdist(X)
Z = linkage(X, method="ward")
_, coph = cophenet(Z, euclid)
score = spearmanr(coph, gold_dist).correlation


# ==========================
# SAVE RESULTS
# ==========================

with open(out_dir + "/selected_features.txt", "w") as f:
    f.write("Selected features:\n")
    for col in feature_cols:
        f.write(col + "\n")
    f.write(f"\nScore: {score}\n")

pd.DataFrame({
    "feature": feature_cols
}).to_csv(out_dir + "/selected_features.csv", index=False)

Z_plot = Z.copy()
Z_plot[:, 2] = np.log1p(Z_plot[:, 2])

plt.figure(figsize=(12, 8))
dendrogram(
    Z_plot,
    labels=langs,
    leaf_rotation=75,
    leaf_font_size=13.5,
    color_threshold=0,
    above_threshold_color="black"
)


ax = plt.gca()

for label in ax.get_xticklabels():
    lang = label.get_text()
    code = df.loc[df["Language"] == lang, "lang_code"].values[0]

    if code in LANG_COLORS:
        label.set_color(LANG_COLORS[code])

#plt.title("Ward Dendrogram")
plt.ylabel("log(1 + distance)")
plt.tight_layout()
plt.savefig(out_dir + "/selected_features_tree.png", dpi=300)
plt.savefig(out_dir + "/selected_features_tree.pdf")
plt.show()




'''
plt.figure(figsize=(10, 14))

dendrogram(
    Z_plot,
    labels=langs,
    orientation="left",
    leaf_font_size=12
)

ax = plt.gca()

for label in ax.get_yticklabels():
    lang = label.get_text()
    code = df.loc[df["Language"] == lang, "lang_code"].values[0]

    if code in LANG_COLORS:
        label.set_color(LANG_COLORS[code])

plt.title("Ward Dendrogram")
plt.ylabel("log(1 + distance)")
plt.tight_layout()
plt.savefig(out_dir + "/selected_features_tree_h.png", dpi=300)
plt.show()
'''
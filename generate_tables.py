import os
import sys
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

from language_constants import (LANG_ORDER,
                                LANGUAGES,
                                CODE2LANG,
                                LANG_COLORS
                                )
from features import featurize


LEVEL = 'all' # page, stimulus, language
IN_DIR = sys.argv[1] if len(sys.argv) > 1 else 'multipleye_annotations/'
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else 'tables/'
os.makedirs(OUT_DIR, exist_ok=True)

col_mapping = {
    "stimulus_name": "Language",
    "num. words": "#Words",
    "num. types": None,
    "type token ratio": "Type-Token Ratio",
    "num. punct.": None,
    "punct. ratio": None,
    "num. function words": None,
    "function words ratio": None,
    "num. sentences": "#Sents.",
    "word length": "Word Length",
    "mean Zipf freq.": None,
    "median Zipf freq.": None,
    "std Zipf freq.": None,
    "num. PRON": None,
    "PRON ratio": None,
    "num. NOUN": None,
    "NOUN ratio": None,
    "num. VERB": None,
    "VERB ratio": None,
}


language_data = {}
for lang_dir in os.listdir(IN_DIR):
    dir_path = os.path.join(IN_DIR, lang_dir)
    lang_code = lang_dir.replace('multipleye_annotations_', '')
    if os.path.isdir(dir_path):
        language_csvs = []
        for csv_file in os.listdir(dir_path):
            if csv_file.endswith('.csv'):
                current_df = pd.read_csv(os.path.join(dir_path, csv_file),
                                         keep_default_na=False)
                language_csvs.append(current_df)
        if language_csvs:
            language_data[lang_code] = pd.concat(language_csvs, axis=0)


if LEVEL in {'all', 'language'}:
    out = {}
    limit = 100
    for lang_code, _ in tqdm(language_data.items()):
        out[lang_code] = featurize(language_data[lang_code], 'language')
        if limit <= 0:
            break
        limit -= 1
    
    elems = []
    for k,o in out.items():
        o['lang_code'] = k
        o['Language'] = CODE2LANG[k]
        elems.append(o.values[0])
        
    df = pd.DataFrame(elems, columns=o.columns)
    df.set_index(['Language'], inplace=True)
    for col in df.columns:
        if 'num.' in col:
            df[col] = df[col].astype(int)
        if 'ratio' in col:
            df[col] = (df[col] * 100).round(2)

    df['word length'] = df['word length'].round(2)
    rename = {}
    for col in df.columns:
        if 'lang_' not in col:
            rename[col] = 'Lang@' + col
    df.rename(columns=rename, inplace=True)

    languages = [CODE2LANG[l] for l in LANG_ORDER if CODE2LANG[l] in df.index]
    df = df.loc[languages]
    lang_df = df.copy()
    lang_df.to_csv(os.path.join(OUT_DIR, 'stats_language.csv'))

if LEVEL in {'all', 'page'}:
    out = {}
    limit = 100
    for lang_code, _ in tqdm(language_data.items()):
        out[lang_code] = featurize(language_data[lang_code], 'page')
        if limit <= 0:
            break
        limit -= 1

    elems = []
    for k,o in out.items():
        o = o.mean()
        o['lang_code'] = k
        o['Language'] = CODE2LANG[k]
        elems.append(o)
    df = pd.concat(elems, axis=1).T

    df.set_index(['Language'], inplace=True)
    for col in df.columns:
        if 'num.' in col:
            df[col] = df[col].astype(int)
        if 'ratio' in col:

            df[col] = (df[col].astype(float) * 100).round(2)

    languages = [CODE2LANG[l] for l in LANG_ORDER if CODE2LANG[l] in df.index]
    df = df.loc[languages]
    rename = {}
    for col in df.columns:
        if 'lang_' not in col:
            rename[col] = 'Page@' + col
    df.rename(columns=rename, inplace=True)
    page_df = df.copy()
    page_df.to_csv(os.path.join(OUT_DIR, 'stats_page.csv'))


lang_cols = ['Lang@num. words', 'Lang@type token ratio', 'Lang@num. sentences', 'Lang@word length']
page_cols = ['Page@num. words', 'Page@function words ratio', 'Page@word length']

rename = {
    'Lang@num. words': '#Words',
    'Lang@type token ratio': 'Type-Token Ratio',
    'Lang@num. sentences': '#Sents.',
    'Lang@word length': 'Word Length',
    'Page@num. words': '#Words (pp)',
    'Page@function words ratio': 'Function Words Ratio (pp)',
    'Page@word length': 'Word Length (pp)',
}

final_df = pd.concat([lang_df[lang_cols], page_df[page_cols]], axis=1)
for col in final_df.columns:
    if 'ratio' in col:
        final_df[col] = final_df[col].apply(lambda x: f'{x:.0f}%')

final_df['color'] = page_df['lang_code'].apply(lambda x: LANG_COLORS[x])

final_df.rename(columns=rename, inplace=True)
final_df.to_csv(os.path.join(OUT_DIR, 'stats_final.csv'))




print('Done!')

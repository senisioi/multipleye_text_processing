# run_turkish_tr_core_news_lg.py
# Env suggestion:
#   pip install pandas openpyxl tqdm spacy
#   pip install "tr_core_news_lg @ https://huggingface.co/turkish-nlp-suite/tr_core_news_lg/resolve/main/tr_core_news_lg-1.0-py3-none-any.whl"
import os
import re
import argparse
import pandas as pd
import spacy

from language_constants import CODE2LANG
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       find_stimulus_files,
                       find_extension)
from tokenization_common import isalpha_inclusive, eos_row

TARGET_RE = re.compile(r"^multipleye_stimuli_experiment_tr\.xlsx$", re.I)

def load_tr():
    nlp = spacy.load("tr_core_news_lg")
    if "sentencizer" not in nlp.pipe_names and "senter" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")
    return nlp


def stimuli_to_df(stimuli, nlp):
    rows = []
    lang_code = "tr"
    lang_name = CODE2LANG.get(lang_code, lang_code)

    for _, sname, page, text in iter_pages(stimuli):
        doc = nlp(text)
        for sent in doc.sents:
            for tok in sent:
                tok_id = (tok.i - sent.start) + 1
                rows.append({
                    "id": tok_id,
                    "language": lang_name,
                    "language_code": lang_code,
                    "stimulus_name": sname,
                    "page": page,
                    "token": anonymize(tok.text, sname),
                    "is_alpha": isalpha_inclusive(tok.text.strip()),
                    "is_stop": bool(tok.is_stop),
                    "is_punct": bool(tok.is_punct),
                    "lemma": anonymize(tok.lemma_, sname),
                    "upos": tok.pos_ or "",
                    "xpos": tok.tag_ or "",
                    "feats": "_",
                    "head": "0",
                    "deprel": "root",
                    "deps": "_",
                    "misc": "SpaceAfter=No" if not tok.whitespace_ else "_",
                })
            rows.append(eos_row(lang_name, lang_code, sname, page))

    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_xlsx")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="multipleye_annotations")
    args = ap.parse_args()

    
    os.makedirs(args.out_dir, exist_ok=True)

    lang_code = "tr"
    xlsx_path = find_stimulus_files(args.in_dir, lang_code)
    ext = find_extension(args.in_dir)
    stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)
    nlp = load_tr()
    df = stimuli_to_df(stimuli, nlp)
    save_per_stimulus_csv(df, args.out_dir, "tr")

if __name__ == "__main__":
    main()
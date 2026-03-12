import os
import re
import argparse
import pandas as pd
import pycantonese  # type: ignore
from pycantonese import stop_words

from language_constants import CODE2LANG
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       find_stimulus_files,
                       find_extension)
from tokenization_common import isalpha_inclusive, eos_row, is_punct

TARGET_RE = re.compile(r"^multipleye_stimuli_experiment_yu\.xlsx$", re.I)
STOP_WORDS = set(stop_words())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_xlsx")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="csv_d_yue")
    args = ap.parse_args()

    
    os.makedirs(args.out_dir, exist_ok=True)

    lang_code = "yu"
    lang_name = CODE2LANG.get(lang_code, lang_code)
    xlsx_path = find_stimulus_files(args.in_dir, lang_code)
    ext = find_extension(args.in_dir)
    stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)

    rows = []

    for _, sname, page, text in iter_pages(stimuli):
        # PyCantonese word segmentation via segment() :contentReference[oaicite:6]{index=6}
        tok_id = 0
        for tok in pycantonese.segment(text):
            tok = tok.strip()
            if not tok:
                continue
            tok_id += 1
            rows.append({
                "id": tok_id,
                "language": lang_name,
                "language_code": lang_code,
                "stimulus_name": sname,
                "page": page,
                "token": anonymize(tok, sname),
                "is_alpha": isalpha_inclusive(tok),
                "is_stop": tok in STOP_WORDS,
                "is_punct": is_punct(tok),
                "lemma": "",
                "upos": "",
                "xpos": "",
                "feats": "_",
                "head": "0",
                "deprel": "root",
                "deps": "_",
                "misc": "_",
            })
        rows.append(eos_row(lang_name, lang_code, sname, page))

    df = pd.DataFrame(rows)
    save_per_stimulus_csv(df, args.out_dir, lang_code)

if __name__ == "__main__":
    main()
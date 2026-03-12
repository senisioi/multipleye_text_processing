'''Script to process Urdu stimuli using Urduhack.
The current version of the library does not work and this code is not used. 
Instead we use a blank spacy model.
'''
import os
import re
import argparse
import pandas as pd
from urduhack.normalization import normalize  
from urduhack.tokenization import word_tokenizer

from language_constants import CODE2LANG
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       find_stimulus_files,
                       find_extension)
from tokenization_common import isalpha_inclusive, eos_row, is_punct

TARGET_RE = re.compile(r"^multipleye_stimuli_experiment_ur\.xlsx$", re.I)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_xlsx")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="multipleye_annotations")
    args = ap.parse_args()

    
    os.makedirs(args.out_dir, exist_ok=True)

    lang_code = "ut"
    xlsx_path = find_stimulus_files(args.in_dir, lang_code)
    ext = find_extension(args.in_dir)
    stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)

    lang_code = "ur"
    lang_name = CODE2LANG.get(lang_code, lang_code)
    rows = []

    for _, sname, page, text in iter_pages(stimuli):
        # Urduhack recommends normalization before tokenization :contentReference[oaicite:5]{index=5}
        norm = normalize(text)
        toks = word_tokenizer(norm)
        for tok in toks:
            tok = tok.strip()
            if not tok:
                continue
            rows.append({
                "language": lang_name,
                "language_code": lang_code,
                "stimulus_name": sname,
                "page": page,
                "token": anonymize(tok),
                "is_alpha": isalpha_inclusive(tok),
                "is_stop": False, #TODO
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
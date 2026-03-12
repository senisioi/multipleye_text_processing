import os
import re
import argparse
import pandas as pd
from indicnlp.tokenize import indic_tokenize  # type: ignore

from language_constants import CODE2LANG
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       find_stimulus_files,
                       find_extension)
from tokenization_common import isalpha_inclusive, eos_row, is_punct

HINDI_STOPWORDS = set(["अंदर", "अत", "अदि", "अप", "अपना", "अपनि", "अपनी", "अपने", "अभि", "अभी", "अंदर", "आदि", "आप", "अगर", "इंहिं", "इंहें", "इंहों", "इतयादि", "इत्यादि", "इन", "इनका", "इन्हीं", "इन्हें", "इन्हों", "इस", "इसका", "इसकि", "इसकी", "इसके", "इसमें", "इसि", "इसी", "इसे", "उंहिं", "उंहें", "उंहों", "उन", "उनका", "उनकि", "उनकी", "उनके", "उनको", "उन्हीं", "उन्हें", "उन्हों", "उस", "उसके", "उसि", "उसी", "उसे", "एक", "एवं", "एस", "एसे", "ऐसे", "ओर", "और", "कइ", "कई", "कर", "करता", "करते", "करना", "करने", "करें", "कहते", "कहा", "का", "काफि", "काफ़ी", "कि", "किंहें", "किंहों", "कितना", "किन्हें", "किन्हों", "किया", "किर", "किस", "किसि", "किसी", "किसे", "की", "कुछ", "कुल", "के", "को", "कोइ", "कोई", "कोन", "कोनसा", "कौन", "कौनसा", "गया", "घर", "जब", "जहाँ", "जहां", "जा", "जिंहें", "जिंहों", "जितना", "जिधर", "जिन", "जिन्हें", "जिन्हों", "जिस", "जिसे", "जीधर", "जेसा", "जेसे", "जैसा", "जैसे", "जो", "तक", "तब", "तरह", "तिंहें", "तिंहों", "तिन", "तिन्हें", "तिन्हों", "तिस", "तिसे", "तो", "था", "थि", "थी", "थे", "दबारा", "दवारा", "दिया", "दुसरा", "दुसरे", "दूसरे", "दो", "द्वारा", "न", "नहिं", "नहीं", "ना", "निचे", "निहायत", "नीचे", "ने", "पर", "पहले", "पुरा", "पूरा", "पे", "फिर", "बनि", "बनी", "बहि", "बही", "बहुत", "बाद", "बाला", "बिलकुल", "भि", "भितर", "भी", "भीतर", "मगर", "मानो", "मे", "में", "मैं", "मुझको", "मेरा", "यदि", "यह", "यहाँ", "यहां", "यहि", "यही", "या", "यिह", "ये", "रखें", "रवासा", "रहा", "रहे", "ऱ्वासा", "लिए", "लिये", "लेकिन", "व", "वगेरह", "वग़ैरह", "वरग", "वर्ग", "वह", "वहाँ", "वहां", "वहिं", "वहीं", "वाले", "वुह", "वे", "वग़ैरह", "संग", "सकता", "सकते", "सबसे", "सभि", "सभी", "साथ", "साबुत", "साभ", "सारा", "से", "सो", "संग", "हि", "ही", "हुअ", "हुआ", "हुइ", "हुई", "हुए", "हे", "हें", "है", "हैं", "हो", "हूँ", "होता", "होति", "होती", "होते", "होना", "होने"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_xlsx")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="multipleye_annotations")
    args = ap.parse_args()

    
    os.makedirs(args.out_dir, exist_ok=True)

    lang_code = "hi"
    xlsx_path = find_stimulus_files(args.in_dir, lang_code)
    ext = find_extension(args.in_dir)
    stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)

    lang_name = CODE2LANG.get(lang_code, lang_code)
    rows = []

    for _, sname, page, text in iter_pages(stimuli):
        # trivial_tokenize: punctuation-aware baseline for Indic scripts :contentReference[oaicite:4]{index=4}
        tok_id = 0
        for tok in indic_tokenize.trivial_tokenize(text, lang="hi"):
            tok = tok.strip()
            tok_id += 1
            if not tok:
                continue
            rows.append({
                "id": tok_id,
                "language": lang_name,
                "language_code": lang_code,
                "stimulus_name": sname,
                "page": page,
                "token": anonymize(tok, sname),
                "is_alpha": isalpha_inclusive(tok),
                "is_stop": tok in HINDI_STOPWORDS,
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
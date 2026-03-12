import os
import sys
import argparse
import pandas as pd
import spacy
import subprocess
from spacy.util import is_package, get_lang_class

from language_constants import CODE2LANG, SPACY_LANGUAGES
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       file_to_lang_code,
                       find_extension)
from tokenization_common import isalpha_inclusive, HAUSA_STOP, GALLICIAN_STOP, eos_row

LANG_UNIVERSE = {
    "ar","fa","lt","sl","ca","fi","lv","sq","cs","fr","mk","sr","da","gl","nl","sv",
    "de","ha","no","tr","el","he","pl","uk","en","hi","pt","ur","es","hr","rm","yu",
    "et","it","ro","zd","eu","kl","ru","zh"
}

# we don't have a functioning urdu pipeline
# 'ur',
SPECIAL_PIPELINES = set(['tr', 'fa', 'he', 'hi',  'yu']) 
# some languages do not have data:
SKIP_LANGS = {"fr", 'ja', 'bg', 'sk'} | SPECIAL_PIPELINES


def ensure_spacy_model(model_name: str):
    """
    Ensure a spaCy model is installed.
    If missing, download it via `spacy download`.
    """
    if is_package(model_name):
        return

    try:
        __import__(model_name)
        return
    except ImportError:
        pass

    print(f"Downloading spaCy model: {model_name}")
    subprocess.check_call(
        [sys.executable, "-m", "spacy", "download", model_name]
    )


def exists_spacy_blank(lang_code):
    try:
        get_lang_class(lang_code)
        return True
    except:
        return False


def load_spacy_model(lang_code, small=False):
    model = None
    if lang_code in SPACY_LANGUAGES:
        genre = 'news'
        if lang_code in {'zh', 'en'}:
            genre = 'web'
        model_name = f'{lang_code}_core_{genre}_{"sm" if small else "lg"}'
        print(f"Loading model {model_name} for {lang_code}")
        try:
            model = spacy.load(model_name)
        except:
            print(f"Model {model_name} not found. Attempting to download...")
            ensure_spacy_model(model_name)
            model = spacy.load(model_name)
        model.add_pipe("sentencizer")
    elif lang_code == "rm":
        model = spacy.load("it_core_news_lg")
        # keep 'morphologizer' ?
        model.disable_pipes('tok2vec', 'tagger', 'parser', 'lemmatizer', 'attribute_ruler', 'ner')
        model.add_pipe("sentencizer")
    elif lang_code == 'no':
        # assume Bokmal
        model_name = 'nb_core_news_lg'
        try:
            model = spacy.load(model_name)
        except:
            print(f"Model {model_name} not found. Attempting to download...")
            ensure_spacy_model(model_name)
            model = spacy.load(model_name)
    elif lang_code == 'gsw' or lang_code == 'zd':
        model = spacy.load('de_core_news_lg')
    elif exists_spacy_blank(lang_code):
        print(f"Loading model blank model for {lang_code}")
        model = spacy.blank(lang_code)
        model.add_pipe("sentencizer")
    else:
        model_name = f'xx_sent_ud_sm'
        print(f"Loading model {model_name} for {lang_code}")
        model = spacy.load(model_name)
        model.add_pipe("sentencizer")
    #special_cases = {"eye-tracking": [{ORTH: "eye-tracking"},
    #                                  {ORTH: "Eye-tracking"},
    #                                  {ORTH: "Eye-Tracking"}]}
    #for token, special_case in special_cases.items():
    #    model.tokenizer.add_special_case(token, special_case)
    return model


NLP_MODEL = None
CURRENT_LANG = ''


def load_nlp(lang_code, small=False):
    """To avoid loading all models at the same time
    """
    global NLP_MODEL, CURRENT_LANG
    if lang_code != CURRENT_LANG:
        try:
            print(f"Deleting model for {CURRENT_LANG}")
            del NLP_MODEL
        except:
            print("No model to delete")
        print(f"Loading model for {lang_code}")
        NLP_MODEL = load_spacy_model(lang_code, small=small)
        CURRENT_LANG = lang_code
    return NLP_MODEL


def feats_str(token):
    if not token.morph:
        return "_"
    md = token.morph.to_dict()
    if not md:
        return "_"
    parts = []
    for k in sorted(md):
        v = md[k]
        if isinstance(v, (list, tuple)):
            parts.append(f"{k}={','.join(v)}")
        else:
            parts.append(f"{k}={v}")
    return "|".join(parts) if parts else "_"


def head_deprel(token, sent):
    if token.head == token or token.dep_ == "ROOT":
        return 0, "root"
    return (token.head.i - sent.start) + 1, (token.dep_.lower() if token.dep_ else "_")


def misc(token, include_ner=True):
    parts = []
    if not token.whitespace_:
        parts.append("SpaceAfter=No")
    if include_ner and token.ent_iob_ != "O":
        parts.append(f"NER={token.ent_iob_}-{token.ent_type_}")
    return "|".join(parts) if parts else "_"


def stimuli_to_df(stimuli, lang_code: str, nlp):
    rows = []
    lang_name = CODE2LANG.get(lang_code, lang_code)

    for _, sname, page, text in iter_pages(stimuli):
        doc = nlp(text)
        for sent in doc.sents:
            for tok in sent:
                tok_id = (tok.i - sent.start) + 1
                # Romansh: keep “minimal” rows like your original
                if lang_code == "rm":
                    row = {
                        "id": tok_id,
                        "language": lang_name,
                        "language_code": lang_code,
                        "stimulus_name": sname,
                        "page": page,
                        "token": anonymize(tok.text, sname),
                        "is_alpha": isalpha_inclusive(tok.text.strip()),
                        "is_stop": False,
                        "is_punct": bool(tok.is_punct),
                        "lemma": "",
                        "upos": "",
                        "xpos": "",
                        "feats": "_",
                        "head": "0",
                        "deprel": "root",
                        "deps": "_",
                        "misc": misc(tok, include_ner=False),
                    }
                else:
                    head, dep = head_deprel(tok, sent)
                    row = {
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
                        "feats": feats_str(tok),
                        "head": head,
                        "deprel": dep,
                        "deps": "_",
                        "misc": misc(tok, include_ner=True),
                    }

                if lang_code == "ha" and row["token"].lower() in HAUSA_STOP:
                    row["is_stop"] = True
                if lang_code == "gl" and row["token"].lower() in GALLICIAN_STOP:
                    row["is_stop"] = True

                rows.append(row)

            rows.append(eos_row(lang_name, lang_code, sname, page))
    df = pd.DataFrame(rows).sort_values(by=["stimulus_name", "page"])
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_data")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="multipleye_annotations")
    args = ap.parse_args()

    ext = find_extension(args.in_dir)
    os.makedirs(args.out_dir, exist_ok=True)

    for fn in sorted(os.listdir(args.in_dir)):
        print(f"Processing {fn}...")
        lang = file_to_lang_code(fn)
        if lang not in LANG_UNIVERSE:
            print(f"Skipping {fn} since language code {lang} not in {LANG_UNIVERSE}")
            continue
        if lang in SKIP_LANGS:
            print(f"Skipping {fn} since language code {lang} is in skip list")
            continue
        xlsx_path = os.path.join(args.in_dir, fn)
        
        print(f"\n=== {lang} ===")
        try:
            stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)
        except Exception as e:
            print(f"[SKIPPING]: Error processing {xlsx_path}: {e}")
            continue
        nlp = load_nlp(lang)
        df = stimuli_to_df(stimuli, lang, nlp)
        save_per_stimulus_csv(df, args.out_dir, lang)


if __name__ == "__main__":
    main()
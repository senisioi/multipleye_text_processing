# run_fa_hazm.py
# Env:
#   pip install pandas openpyxl hazm huggingface-hub

import os
import re
import argparse
import pandas as pd

from hazm import (
    Normalizer,
    SentenceTokenizer,
    WordTokenizer,
    Lemmatizer,
    POSTagger,
    DependencyParser,
)  # type: ignore
from hazm.utils import stopwords_list  # type: ignore

from language_constants import CODE2LANG
from common_io import (input_file_to_stimuli,
                       iter_pages,
                       save_per_stimulus_csv,
                       anonymize,
                       find_stimulus_files,
                       find_extension)
from tokenization_common import isalpha_inclusive, eos_row, is_punct


TARGET_RE = re.compile(r"^multipleye_stimuli_experiment_fa\.xlsx$", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-dir", default="languages_xlsx")
    ap.add_argument("--write-json", action="store_true", default=False)
    ap.add_argument("--out-dir", default="multipleye_annotations")
    ap.add_argument("--with-pos", action="store_true", default=True)
    ap.add_argument("--with-dep", action="store_true", default=True)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    lang_code = "fa"
    lang_name = CODE2LANG.get(lang_code, lang_code)

    ext = find_extension(args.in_dir)
    xlsx_path = find_stimulus_files(args.in_dir, lang_code)
    stimuli = input_file_to_stimuli(xlsx_path, ext=ext, write_json=args.write_json)

    rows = []

    normalizer = Normalizer()
    sent_tokenizer = SentenceTokenizer()
    word_tokenizer = WordTokenizer()
    lemmatizer = Lemmatizer()
    stops = set(stopwords_list())

    tagger = None
    parser = None

    if args.with_pos or args.with_dep:
        tagger = POSTagger(
            repo_id="roshan-research/hazm-postagger",
            model_filename="pos_tagger.model",
        )

    if args.with_dep:
        parser = DependencyParser(
            tagger=tagger,
            lemmatizer=lemmatizer,
            repo_id="roshan-research/hazm-dependency-parser",
            model_filename="langModel.mco",
        )

    for _, sname, page, text in iter_pages(stimuli):
        tok_id = 0
        text = normalizer.normalize(text)
        sentences = sent_tokenizer.tokenize(text)

        for sent in sentences:
            word_tokens = [t for t in word_tokenizer.tokenize(sent)]
            if not word_tokens:
                print(f"Warning: no word tokens found for sentence: {sent}")
                continue
            tagged_words = []
            if tagger is not None:
                tagged_words = tagger.tag(word_tokens)

            dep_nodes = {}
            if parser is not None:
                dependency_graph = parser.parse(word_tokens)
                dep_nodes = getattr(dependency_graph, "nodes", {}) or {}

            for i, tok in enumerate(word_tokens, start=1):
                tok_id += 1

                node = dep_nodes.get(i, {})

                lemma = ""
                if node.get("lemma") not in (None, ""):
                    lemma = str(node["lemma"])
                else:
                    try:
                        lemma = lemmatizer.lemmatize(tok)
                    except Exception:
                        lemma = ""

                upos = ""
                xpos = ""
                feats = "_"
                head = "0"
                deprel = "root"
                deps = "_"

                if node:
                    upos = "" if node.get("ctag") is None else str(node.get("ctag"))
                    xpos = "" if node.get("tag") is None else str(node.get("tag"))
                    feats = "_" if node.get("feats") in (None, "") else str(node.get("feats"))
                    head = "0" if node.get("head") in (None, "") else str(node.get("head"))
                    deprel = "root" if node.get("rel") in (None, "") else str(node.get("rel"))

                    node_deps = node.get("deps")
                    if node_deps:
                        try:
                            parts = []
                            for rel, heads in node_deps.items():
                                for h in heads:
                                    parts.append(f"{h}:{rel}")
                            deps = "|".join(parts) if parts else "_"
                        except Exception:
                            deps = "_"

                elif i <= len(tagged_words):
                    # fallback to POS tagger output when dependency parser is not used
                    xpos = tagged_words[i - 1][1]
                    upos = tagged_words[i - 1][1]

                rows.append({
                    "id": tok_id,
                    "language": lang_name,
                    "language_code": lang_code,
                    "stimulus_name": sname,
                    "page": page,
                    "token": anonymize(tok, sname),
                    "is_alpha": isalpha_inclusive(tok),
                    "is_stop": tok in stops,
                    "is_punct": is_punct(tok),
                    "lemma": anonymize(lemma, sname),
                    "upos": upos,
                    "xpos": xpos,
                    "feats": feats,
                    "head": head,
                    "deprel": deprel,
                    "deps": deps,
                    "misc": "_",
                })

        rows.append(eos_row(lang_name, lang_code, sname, page))

    df = pd.DataFrame(rows)
    save_per_stimulus_csv(df, args.out_dir, lang_code)


if __name__ == "__main__":
    main()
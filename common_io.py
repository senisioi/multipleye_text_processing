import os
import json
import pandas as pd

ID2NAME = {
    1: "PopSci_MultiplEYE",
    2: "Ins_HumanRights",
    3: "Ins_LearningMobility",
    4: "Lit_Alchemist",
    5: "Lit_EmperorClothes",
    6: "Lit_MagicMountain",
    7: "Lit_NorthWind",
    8: "Lit_Solaris",
    9: "Lit_BrokenApril",
    10: "Arg_PISACowsMilk",
    11: "Arg_PISARapaNui",
    12: "PopSci_Caveman",
    13: "Enc_WikiMoon",
    14: "Lit_HarryPotter"
}
NAME2ID = {v: k for k, v in ID2NAME.items()}
SKIPPED_STIMULI = set(["Lit_EmperorClothes", "Lit_HarryPotter"])

# default is true unless explicitly set to false via environment variable (e.g. for Danish)
ANONYMIZE = False
if 'ANONYMIZE' in os.environ:
    print("Setting ANONYMIZE to", os.environ['ANONYMIZE'])
    ANONYMIZE = os.environ['ANONYMIZE'].lower() == 'true'
 

def anonymize(text, stimulus_name):
    if not text:
        return ""
    if 'Lit_' in stimulus_name and ANONYMIZE:
        return ""
    return text

def file_to_lang_code(filename):
    fis = os.path.basename(filename)
    fis = fis.replace("multipleye_stimuli_experiment_", "")
    fis = fis.replace(".xlsx", "")
    fis = fis.replace(".csv", "")
    return fis.lower()

def find_extension(in_dir: str):
    for fn in sorted(os.listdir(in_dir)):
        current = fn.replace('multipleye_stimuli_experiment_', '').lower()
        if current.endswith(".xlsx"):
            return ".xlsx"
        elif current.endswith(".csv"):
            return ".csv"
    raise FileNotFoundError("No .xlsx or .csv files found in the input directory")

def find_stimulus_files(in_dir: str, lang_code: str):
    found = False
    for fn in sorted(os.listdir(in_dir)):
        lang = file_to_lang_code(fn)
        if lang == lang_code:
            found = True 
            break
    if not found:
        raise FileNotFoundError(f"multipleye_stimuli_experiment_{lang_code}.xlsx / .csv not found")
    return os.path.join(in_dir, fn)

def input_file_to_stimuli(in_xlsx: str, ext:str = ".xlsx",  write_json:bool = False,):
    """
    Read xlsx / csv file  build stimuli list  write JSON to disk.
    Returns stimuli list (pipeline uses this directly; does NOT read JSON).
    """
    if ext.lower() == ".xlsx":
        df = pd.read_excel(in_xlsx)
    elif ext.lower() == ".csv":
        df = pd.read_csv(in_xlsx)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    stimuli = []

    for ridx, row in df.iterrows():
        pages = []
        for col in df.columns:
            if isinstance(col, str) and col.startswith("page_") and pd.notna(row[col]):
                pages.append(str(row[col]).strip())
        sname = row["stimulus_name"]
        if sname not in NAME2ID or sname in SKIPPED_STIMULI:
            continue
        stimuli.append({
            "stimulus_id": NAME2ID[sname],
            "stimulus_name": sname,
            "stimulus_type": row.get("stimulus_type", ""),
            "pages": pages
        })
    if write_json:
        out_dir = os.path.join(os.path.dirname(in_xlsx), 'languages_json')
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        out_json = os.path.join(out_dir, os.path.basename(in_xlsx).replace(".xlsx", ".json"))
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(stimuli, f, indent=2, ensure_ascii=False)

    return stimuli

def iter_pages(stimuli):
    for stim in stimuli:
        sid = stim["stimulus_id"]
        sname = stim["stimulus_name"]
        for pnum, page_text in enumerate(stim["pages"], start=1):
            yield sid, sname, pnum, page_text

def save_per_stimulus_csv(df, out_dir: str, lang_code: str):
    lang_out = os.path.join(out_dir, f'multipleye_annotations_{lang_code}')
    os.makedirs(lang_out, exist_ok=True)

    for stim_name, group in df.groupby("stimulus_name"):
        out_path = os.path.join(lang_out, f"{stim_name}_{lang_code}.csv")
        tmpdf = group.copy()
        tmpdf.index = range(1, len(tmpdf) + 1)
        tmpdf.to_csv(out_path, index=True, index_label='index')
        print(out_path)
import os
try:
    import re2 as re
except ImportError:
    import re
import io
import time
import zipfile
import sys
from tqdm import tqdm
from config import CSGO_FOLDER

start_time = time.time()

languages = ['brazilian', 'bulgarian', 'czech', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'greek', 'hungarian', 'italian', 'japanese', 'korean', 'koreana', 'latam', 'norwegian', 'pirate', 'polish', 'portuguese', 'romanian', 'russian', 'schinese', 'schinese_pw', 'spanish', 'swedish', 'tchinese', 'thai', 'turkish', 'ukrainian', 'vietnamese']
ITEMS_GAME = os.path.join(CSGO_FOLDER, "scripts/items/items_game.txt")


if sys.platform == 'linux' or sys.platform == 'darwin': # Linux or Mac
    zip_filename = os.path.join(os.environ['HOME'] + "/Desktop/weapons.zip")
else: # Windows
    zip_filename = os.path.join(os.environ['USERPROFILE'] + "/Desktop/weapons.zip")

with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for LANG in tqdm(languages, desc='Processing files'):
        LANGFILE = os.path.join(CSGO_FOLDER, "resource/csgo_" + LANG + ".txt")
        ENGLISH_LANGFILE = os.path.join(CSGO_FOLDER, "resource/csgo_english.txt")
        if sys.platform == 'linux' or sys.platform == 'darwin':
            OUTPUT_FILE = os.path.join(os.environ['HOME'] + "/Desktop/weapons_" + LANG + ".cfg")
        else:
            OUTPUT_FILE = os.path.join(os.environ['USERPROFILE'] + "/Desktop/weapons_" + LANG + ".cfg")

        with io.open(LANGFILE, 'r', encoding='utf_16_le') as f:
            translations = f.read()

        with io.open(ITEMS_GAME, 'r') as f:
            items_game = f.read()

        english_translations = ""

        def load_translations(langfile):
            with io.open(langfile, 'r', encoding='utf_16_le') as f:
                return f.read()

        translations = load_translations(LANGFILE)
        english_translations = load_translations(ENGLISH_LANGFILE)

        list_of_skins = []

        pattern = re.compile(r"\"(\d+?)\"[\r\n]{1,2}\s*?\{[\r\n]{1,2}\s*?\"name\"\s*?\"([^\"]*?)\"[\r\n]{1,2}[^\r\n]*?[\r\n]{1,2}\s*?\"description_tag\"\s*?\"#(Paint[Kk]it_[^\"]*?)\"")
        matcher = pattern.finditer(items_game)
        for m in matcher:
            skin = {}
            skin['id'] = int(m.group(1))
            skin['name'] = m.group(2)
            skin['tag'] = m.group(3)
            weapons_pattern = re.compile("\\s*?\"icon_path\"\\s*?\"econ/default_generated/(weapon_[^\"]*?)_" + skin['name'] + "_medium\"")
            weapons_matcher = weapons_pattern.finditer(items_game)
            skin['weapons'] = []
            for wm in weapons_matcher:
                skin['weapons'].append(wm.group(1))

            lang_pattern = re.compile("\"" + skin['tag'] + "\"\\s*?\"([^\"]*?)\"", re.IGNORECASE)
            lang_matcher = re.search("\"" + skin['tag'] + "\"\\s*?\"([^\"]*?)\"", translations, re.IGNORECASE)
            if lang_matcher:
                skin['lang'] = lang_matcher.group(1)

            list_of_skins.append(skin)

        def getLang(skin):
            phase = ""
            marbleized = ""

            if "phase" in skin['name'].lower():
                phase = " (Phase " + re.search("\d+", skin['name'][skin['name'].lower().index("phase"):]).group(0) + ")"
            if "marbleized" in skin['name'].lower():
                pattern = re.search("\w+(?=_marbleized)", skin['name']).group(0)
                if pattern == "am_blackpearl":
                    pattern = "black pearl"
                pattern = pattern.replace("am_", "")
                marbleized = " (" + pattern.title() + ")"
            if 'lang' in skin:
                lang = skin['lang']
            else:
                lang_matcher = re.search("\"" + skin['tag'] + "\"\\s*?\"([^\"]*?)\"", english_translations, re.IGNORECASE)
                if lang_matcher:
                    lang = lang_matcher.group(1)
                else:
                    lang = skin['tag']

            return lang + phase + marbleized

        if os.path.isfile(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)

        with io.open(OUTPUT_FILE, 'w', encoding='utf_8') as output_file:
            output_file.write("\"Skins\"\n")
            output_file.write("{\n")
            for skin in list_of_skins[::-1]:
                if len(skin['weapons']) > 0:
                    output_file.write("\t\""+ getLang(skin) + "\"\n")
                    output_file.write("\t{\n")
                    output_file.write("\t\t\"index\"\t\t\"" + str(skin['id']) + "\"\n")
                    output_file.write("\t\t\"classes\"\t\"" + ';'.join(skin['weapons']) + "\"\n")
                    output_file.write("\t}\n")
            output_file.write("}\n")

        zipf.write(OUTPUT_FILE, f"weapons_{LANG}.cfg")

        output_file.close()

        os.remove(OUTPUT_FILE)

        sys.stdout.flush()


end_time = time.time()
print(f"It took {end_time-start_time:.2f} seconds to finish")
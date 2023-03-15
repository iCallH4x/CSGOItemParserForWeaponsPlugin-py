# CSGOItemParserForWeaponsPlugin-py

This is essentially a re-write of https://github.com/kgns/CSGOItemParserForWeaponsPlugin written in Python. It uses re2 to speed up regex, and is about 10x faster per file than the original java program. Unlike the original program, you aren't meant to run this directly on your server, but on your computer to generate a zip file with all the necessary files on your Desktop, then upload to the server the way you would usually update. 

I have not yet tested this on Linux or Mac, however it *should* work as expected. If not, feel free to make a pull request!

# Usage

1. Install the requirements:
```py
pip install -r requirements.txt
```

2. Change all necessary information in the `config.py` file

3. Run `csgo.py` and wait for it to finish!
import os
import random
import urllib.parse
import requests
import streamlit as st
from io import BytesIO
from PIL import Image
import base64

# Make sure images folder exists
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

# --- UTILITY FUNCTIONS ---
def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name).lower()

def get_ext_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        return ext
    return ".png"

@st.cache_data(show_spinner=False)
def ensure_image(name: str, url: str):
    """
    Ensure the image is available locally.
    Returns a local path if possible; otherwise returns the URL.
    """
    if not url:
        return None
    local_filename = sanitize_filename(name) + get_ext_from_url(url)
    local_path = os.path.join(IMG_DIR, local_filename)

    if os.path.exists(local_path):
        return local_path

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://bloons.fandom.com/"
    }

    try:
        resp = requests.get(url, headers=headers, stream=True, timeout=15)
        if resp.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            return local_path
        else:
            return url
    except Exception:
        return url

def img_to_base64(path_or_url):
    """
    Convert a local file or URL to a base64 string for HTML embedding.
    """
    try:
        if path_or_url.startswith("http"):
            response = requests.get(path_or_url)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(path_or_url)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print("Error loading image:", e)
        return None

# --- Your existing data (maps/ heroes / towers) ---
modes = [
    "Standard (Easy)", "Primary Only", "Deflation", "Standard (Medium)", "Reverse",
    "Military Only", "Apopalypse", "Standard (Hard)", "Alternate Bloons Round",
    "Impoppable", "CHIMPS", "Magic Only", "Double HP Moabs", "Half Cash"
]

maps = [
    {"name": "Monkey Meadow", "water": False},
    {"name": "Tree Stump", "water": False},
    {"name": "Town Center", "water": True},
    {"name": "In the Loop", "water": True},
    {"name": "Logs", "water": True},
    {"name": "Cubism", "water": True},
    {"name": "End of the Road", "water": True},
    {"name": "Frozen Over", "water": True},
    {"name": "Carved", "water": True},
    {"name": "Water Park", "water": True},
    {"name": "Spa Pits", "water": True},
    {"name": "Flooded Valley", "water": True},
    {"name": "Mesa", "water": False},
    {"name": "Middle of the Road", "water": True},
    {"name": "Midnight Mansion", "water": False},
    {"name": "Moon Landing", "water": False},
    {"name": "Muddy Puddles", "water": True},
    {"name": "X Factor", "water": False},
    {"name": "Spice Islands", "water": True},
    {"name": "Dark Castle", "water": True},
    {"name": "High Finance", "water": True},
    {"name": "Geared", "water": False},
    {"name": "Cargo", "water": True},
    {"name": "Peninsula", "water": True},
    {"name": "#Ouch", "water": True},
    {"name": "Sulfur Springs", "water": True},
    {"name": "Off the Coast", "water": True},
    {"name": "Adora's Temple", "water": True},
    {"name": "Alpine Run", "water": False},
    {"name": "Ancient Portal", "water": True},
    {"name": "Another Brick", "water": True},
    {"name": "Balance", "water": True},
    {"name": "Bazaar", "water": True},
    {"name": "Bloody Puddles", "water": True},
    {"name": "Bloonarius Prime", "water": True},
    {"name": "Candy Falls", "water": True},
    {"name": "Castle Revenge", "water": True},
    {"name": "Chutes", "water": True},
    {"name": "Cornfield", "water": False},
    {"name": "Covered Garden", "water": True},
    {"name": "Cracked", "water": True},
    {"name": "Dark Dungeons", "water": True},
    {"name": "Dark Path", "water": False},
    {"name": "Downstream", "water": True},
    {"name": "Enchanted Glade", "water": True},
    {"name": "Encrypted", "water": True},
    {"name": "Erosion", "water": True},
    {"name": "Firing Range", "water": False},
    {"name": "Four Circles", "water": True},
    {"name": "Glacial Trail", "water": True},
    {"name": "Haunted", "water": True},
    {"name": "Hedge", "water": False},
    {"name": "Infernal", "water": True},
    {"name": "KartsNDarts", "water": False},
    {"name": "Last Resort", "water": True},
    {"name": "Lost Crevasse", "water": True},
    {"name": "Lotus Island", "water": True},
    {"name": "Luminous Cove", "water": True},
    {"name": "One Two Tree", "water": True},
    {"name": "Park Path", "water": True},
    {"name": "Pat's Pond", "water": True},
    {"name": "Polyphemus", "water": True},
    {"name": "Quad", "water": True},
    {"name": "Quarry", "water": True},
    {"name": "Quiet Street", "water": True},
    {"name": "Rake", "water": True},
    {"name": "Ravine", "water": True},
    {"name": "Resort", "water": True},
    {"name": "Sanctuary", "water": True},
    {"name": "Scrapyard", "water": True},
    {"name": "Skates", "water": True},
    {"name": "Spillway", "water": True},
    {"name": "Spring Spring", "water": True},
    {"name": "Streambed", "water": True},
    {"name": "Sunken Columns", "water": True},
    {"name": "Sunset Gulch", "water": False},
    {"name": "The Cabin", "water": True},
    {"name": "Tinkerton", "water": True},
    {"name": "Underground", "water": False},
    {"name": "Winter Park", "water": True},
    {"name": "Workshop", "water": False},
]

heroes = [
    "Gwendolin", "Quincy", "Obyn Greenfoot", "Admiral Brickell", "Silas", "Striker Jones"
]

maps_images = {
    "Monkey Meadow": "https://static.wikia.nocookie.net/b__/images/e/e2/MonkeyMeadow_No_UI.png/revision/latest?cb=20200519013103&path-prefix=bloons",
    "Tree Stump": "https://static.wikia.nocookie.net/b__/images/b/b4/TreeStump_No_UI.png/revision/latest?cb=20200519013110&path-prefix=bloons",
    "Town Center": "https://static.wikia.nocookie.net/b__/images/8/89/TownCenter_No_UI.png/revision/latest?cb=20200519013110&path-prefix=bloons",
    "In the Loop": "https://static.wikia.nocookie.net/b__/images/d/d3/InTheLoop_No_UI.png/revision/latest?cb=20200519013102&path-prefix=bloons",
    "Logs": "https://static.wikia.nocookie.net/b__/images/5/5d/Logs_No_UI.png/revision/latest?cb=20200519013103&path-prefix=bloons",
    "Cubism": "https://static.wikia.nocookie.net/b__/images/e/e6/Cubism_No_UI.png/revision/latest?cb=20200519012910&path-prefix=bloons",
    "End of the Road": "https://static.wikia.nocookie.net/b__/images/e/e1/EndoftheRoad_No_UI.png/revision/latest?cb=20200519012912&path-prefix=bloons",
    "Frozen Over": "https://static.wikia.nocookie.net/b__/images/0/00/FrozenOver_No_UI.png/revision/latest?cb=20200519012914&path-prefix=bloons",
    "Carved": "https://static.wikia.nocookie.net/b__/images/e/e9/Carved_No_UI.png/revision/latest?cb=20200519012908&path-prefix=bloons",
    "Water Park": "https://static.wikia.nocookie.net/b__/images/4/46/WaterPark_No_UI.png/revision/latest?cb=20230726125928&path-prefix=bloons",
    "Spa Pits": "https://static.wikia.nocookie.net/b__/images/0/00/SpaPits_No_UI.png/revision/latest?cb=20250402071846&path-prefix=bloons",
    "Flooded Valley": "https://static.wikia.nocookie.net/b__/images/9/96/Flooded_Valley_No_UI.png/revision/latest?cb=20200908030039&path-prefix=bloons",
    "Mesa": "https://static.wikia.nocookie.net/b__/images/d/d5/Mesa_No_UI.png/revision/latest?cb=20200903103358&path-prefix=bloons",
    "Middle of the Road": "https://static.wikia.nocookie.net/b__/images/f/f0/MiddleOfTheRoad_No_UI.png/revision/latest?cb=20230216084927&path-prefix=bloons",
    "Midnight Mansion": "https://static.wikia.nocookie.net/b__/images/e/e0/Midnight_Mansion_No_UI.png/revision/latest?cb=20221012204419&path-prefix=bloons",
    "Moon Landing": "https://static.wikia.nocookie.net/b__/images/f/f8/MoonLanding_No_UI.png/revision/latest?cb=20200519013104&path-prefix=bloons",
    "Muddy Puddles": "https://static.wikia.nocookie.net/b__/images/4/4c/MuddyPuddles_No_UI.png/revision/latest?cb=20200519013104&path-prefix=bloons",
    "X Factor": "https://static.wikia.nocookie.net/b__/images/7/7c/MapSelectXFactorButton.png/revision/latest?cb=20201203040004&path-prefix=bloons",
    "Spice Islands": "https://static.wikia.nocookie.net/b__/images/4/45/SpiceIslands_No_UI.png/revision/latest?cb=20200519013108&path-prefix=bloons",
    "Dark Castle": "https://static.wikia.nocookie.net/b__/images/1/1f/DarkCastle_No_UI.png/revision/latest?cb=20200519012911&path-prefix=bloons",
    "High Finance": "https://static.wikia.nocookie.net/b__/images/4/4e/HighFinance_No_UI.png/revision/latest?cb=20200519013101&path-prefix=bloons",
    "Geared": "https://static.wikia.nocookie.net/b__/images/d/df/Geared_No_UI.png/revision/latest?cb=20200519012914&path-prefix=bloons",
    "Cargo": "https://static.wikia.nocookie.net/b__/images/d/df/Cargo_No_UI.png/revision/latest?cb=20200519012907&path-prefix=bloons",
    "Peninsula": "https://static.wikia.nocookie.net/b__/images/b/b7/Peninsula_No_UI.png/revision/latest?cb=20200518232444&path-prefix=bloons",
    "#Ouch": "https://static.wikia.nocookie.net/b__/images/0/09/Ouch_No_UI.png/revision/latest?cb=20200519013105&path-prefix=bloons",
    "Sulfur Springs": "https://static.wikia.nocookie.net/b__/images/1/1c/Sulfur_Springs_No_UI.png/revision/latest?cb=20240207064930&path-prefix=bloons",
    "Off the Coast": "https://static.wikia.nocookie.net/b__/images/6/61/OffTheCoast_No_UI.png/revision/latest?cb=20200519013104&path-prefix=bloons",
    "Adora's Temple": "https://static.wikia.nocookie.net/b__/images/0/0a/AdorasTemple_No_UI.png/revision/latest?cb=20200519012904&path-prefix=bloons",
    "Alpine Run": "https://static.wikia.nocookie.net/b__/images/0/07/AlpineRun_No_UI.png/revision/latest?cb=20200519012905&path-prefix=bloons",
    "Ancient Portal": "https://static.wikia.nocookie.net/b__/images/b/bc/AncientPortal_No_UI.png/revision/latest?cb=20241009065716&path-prefix=bloons",
    "Another Brick": "https://static.wikia.nocookie.net/b__/images/f/f4/AnotherBrick_No_UI.png/revision/latest?cb=20200519012906&path-prefix=bloons",
    "Balance": "https://static.wikia.nocookie.net/b__/images/5/5a/Balance_No_UI.png/revision/latest?cb=20211112153122&path-prefix=bloons",
    "Bazaar": "https://static.wikia.nocookie.net/b__/images/a/a4/Bazaar_No_UI.PNG/revision/latest?cb=20201113035009&path-prefix=bloons",
    "Bloody Puddles": "https://static.wikia.nocookie.net/b__/images/3/31/BloodyPuddles_No_UI.png/revision/latest?cb=20200519012906&path-prefix=bloons",
    "Bloonarius Prime": "https://static.wikia.nocookie.net/b__/images/9/97/BloonariusPrime_No_UI.png/revision/latest?cb=20210816054741&path-prefix=bloons",
    "Candy Falls": "https://static.wikia.nocookie.net/b__/images/8/8e/CandyFalls_No_UI.png/revision/latest?cb=20200519012907&path-prefix=bloons",
    "Castle Revenge": "https://static.wikia.nocookie.net/b__/images/d/d7/CastleRevenge_No_UI.png/revision/latest?cb=20240408135401&path-prefix=bloons",
    "Chutes": "https://static.wikia.nocookie.net/b__/images/d/d3/Chutes_No_UI.png/revision/latest?cb=20200519012908&path-prefix=bloons",
    "Cornfield": "https://static.wikia.nocookie.net/b__/images/5/54/Cornfield_No_UI.png/revision/latest?cb=20200519012909&path-prefix=bloons",
    "Covered Garden": "https://static.wikia.nocookie.net/b__/images/d/d0/CoveredGarden_No_UI.png/revision/latest?cb=20221012204437&path-prefix=bloons",
    "Cracked": "https://static.wikia.nocookie.net/b__/images/3/3e/Cracked_No_UI.png/revision/latest?cb=20200519012909&path-prefix=bloons",
    "Dark Dungeons": "https://static.wikia.nocookie.net/b__/images/8/8b/DarkDungeons_No_UI.png/revision/latest?cb=20230216084928&path-prefix=bloons",
    "Dark Path": "https://static.wikia.nocookie.net/b__/images/6/6b/DarkPath_No_UI.png/revision/latest?cb=20231010074904&path-prefix=bloons",
    "Downstream": "https://static.wikia.nocookie.net/b__/images/1/18/Downstream_No_UI.png/revision/latest?cb=20200519012911&path-prefix=bloons",
    "Enchanted Glade": "https://static.wikia.nocookie.net/b__/images/b/b8/EnchantedGlade_No_UI.png/revision/latest?cb=20250205084253&path-prefix=bloons",
    "Encrypted": "https://static.wikia.nocookie.net/b__/images/e/e5/MapSelectEncryptedButton.png/revision/latest?cb=20201016000424&path-prefix=bloons",
    "Erosion": "https://static.wikia.nocookie.net/b__/images/1/12/Erosion_No_UI.png/revision/latest?cb=20230607074521&path-prefix=bloons",
    "Firing Range": "https://static.wikia.nocookie.net/b__/images/4/42/FiringRange_No_UI.png/revision/latest?cb=20240701035311&path-prefix=bloons",
    "Four Circles": "https://static.wikia.nocookie.net/b__/images/f/ff/FourCircles_No_UI.png/revision/latest?cb=20200519012913&path-prefix=bloons",
    "Glacial Trail": "https://static.wikia.nocookie.net/b__/images/b/bf/GlacialTrail_No_UI.png/revision/latest?cb=20231206090901&path-prefix=bloons",
    "Haunted": "https://static.wikia.nocookie.net/b__/images/e/e8/Haunted_No_UI.png/revision/latest?cb=20200519012915&path-prefix=bloons",
    "Hedge": "https://static.wikia.nocookie.net/b__/images/c/cd/Hedge_No_UI.png/revision/latest?cb=20200519012916&path-prefix=bloons",
    "Infernal": "https://static.wikia.nocookie.net/b__/images/d/d9/Infernal_No_UI.png/revision/latest?cb=20200519013101&path-prefix=bloons",
    "KartsNDarts": "https://static.wikia.nocookie.net/b__/images/e/e6/KartsNDarts_No_UI.png/revision/latest?cb=20200519013102&path-prefix=bloons",
    "Last Resort": "https://static.wikia.nocookie.net/b__/images/0/0f/Last_Resort_No_UI.png/revision/latest?cb=20241210132925&path-prefix=bloons",
    "Lost Crevasse": "https://static.wikia.nocookie.net/b__/images/0/07/LostCrevasse_No_UI.png/revision/latest?cb=20250827072050&path-prefix=bloons",
    "Lotus Island": "https://static.wikia.nocookie.net/b__/images/9/9e/LotusIsland_No_UI.png/revision/latest?cb=20211008000755&path-prefix=bloons",
    "Luminous Cove": "https://static.wikia.nocookie.net/b__/images/0/01/LuminousCove_No_UI.png/revision/latest?cb=20240801065346&path-prefix=bloons",
    "One Two Tree": "https://static.wikia.nocookie.net/b__/images/0/0b/OneTwoTree_No_UI.png/revision/latest?cb=20221208131615&path-prefix=bloons",
    "Park Path": "https://static.wikia.nocookie.net/b__/images/d/d8/ParkPath_No_UI.png/revision/latest?cb=20200519013106&path-prefix=bloons",
    "Pat's Pond": "https://static.wikia.nocookie.net/b__/images/9/96/PatsPond_No_UI.png/revision/latest?cb=20200519013106&path-prefix=bloons",
    "Polyphemus": "https://static.wikia.nocookie.net/b__/images/2/2c/Polyphemus_No_UI.png/revision/latest?cb=20230404070617&path-prefix=bloons",
    "Quad": "https://static.wikia.nocookie.net/b__/images/6/69/Quad_No_UI.png/revision/latest?cb=20200519013107&path-prefix=bloons",
    "Quarry": "https://static.wikia.nocookie.net/b__/images/5/53/Quarry_No_UI.png/revision/latest?cb=20221008184912&path-prefix=bloons",
    "Quiet Street": "https://static.wikia.nocookie.net/b__/images/4/4e/QuietStreet_No_UI.png/revision/latest?cb=20211209004434&path-prefix=bloons",
    "Rake": "https://static.wikia.nocookie.net/b__/images/2/23/Rake_No_UI.png/revision/latest?cb=20200519013107&path-prefix=bloons",
    "Ravine": "https://static.wikia.nocookie.net/b__/images/3/38/Ravine_No_UI.png/revision/latest?cb=20211117040536&path-prefix=bloons",
    "Resort": "https://static.wikia.nocookie.net/b__/images/3/38/Resort_No_UI.png/revision/latest?cb=20210930053044&path-prefix=bloons",
    "Sanctuary": "https://static.wikia.nocookie.net/b__/images/6/60/Sanctuary_No_UI.png/revision/latest?cb=20210818052711&path-prefix=bloons",
    "Scrapyard": "https://static.wikia.nocookie.net/b__/images/c/c4/Scrapyard_No_UI.png/revision/latest?cb=20220413173158&path-prefix=bloons",
    "Skates": "https://static.wikia.nocookie.net/b__/images/5/58/MapSelectSkatesButton.png/revision/latest?cb=20201203035953&path-prefix=bloons",
    "Spillway": "https://static.wikia.nocookie.net/b__/images/d/dd/Spillway_No_UI.png/revision/latest?cb=20200519013108&path-prefix=bloons",
    "Spring Spring": "https://static.wikia.nocookie.net/b__/images/1/1c/SpringSpring_No_UI.png/revision/latest?cb=20200519013109&path-prefix=bloons",
    "Streambed": "https://static.wikia.nocookie.net/b__/images/e/e7/Streambed_No_UI.png/revision/latest?cb=20200519013109&path-prefix=bloons",
    "Sunken Columns": "https://static.wikia.nocookie.net/b__/images/3/38/Sunken_Columns_No_UI.png/revision/latest?cb=20220217181915&path-prefix=bloons",
    "Sunset Gulch": "https://static.wikia.nocookie.net/b__/images/f/fb/Sunset_Gulch_No_UI.png/revision/latest?cb=20250618071944&path-prefix=bloons",
    "The Cabin": "https://static.wikia.nocookie.net/b__/images/b/b3/TheCabin_No_UI.png/revision/latest?cb=20211022045656&path-prefix=bloons",
    "Tinkerton": "https://static.wikia.nocookie.net/b__/images/a/af/Tinkerton_No_UI.png/revision/latest?cb=20240529062923&path-prefix=bloons",
    "Underground": "https://static.wikia.nocookie.net/b__/images/5/59/Underground_No_UI.png/revision/latest?cb=20200519013124&path-prefix=bloons",
    "Winter Park": "https://static.wikia.nocookie.net/b__/images/6/69/WinterPark_No_UI.png/revision/latest?cb=20200519013125&path-prefix=bloons",
    "Workshop": "https://static.wikia.nocookie.net/b__/images/b/ba/Workshop_No_UI.png/revision/latest?cb=20200519013125&path-prefix=bloons",
}

mode_images = {
    "Standard (Easy)": "https://static.wikia.nocookie.net/b__/images/6/63/ModeSelectEasyBtn.png/revision/latest?cb=20200613080341&path-prefix=bloons",
    "Primary Only": "https://static.wikia.nocookie.net/b__/images/9/9f/PrimaryBtn.png/revision/latest?cb=20200615232439&path-prefix=bloons",
    "Deflation": "https://static.wikia.nocookie.net/b__/images/5/5a/DeflationBtn.png/revision/latest?cb=20230512114310&path-prefix=bloons",
    "Standard (Medium)": "https://static.wikia.nocookie.net/b__/images/4/48/ModeSelectMediumBtn.png/revision/latest?cb=20200613080342&path-prefix=bloons",
    "Reverse": "https://static.wikia.nocookie.net/b__/images/c/cf/ReverseBtn.png/revision/latest?cb=20200620043846&path-prefix=bloons",
    "Military Only": "https://static.wikia.nocookie.net/b__/images/1/1c/MilitaryBtn.png/revision/latest?cb=20220905150044&path-prefix=bloons",
    "Apopalypse": "https://static.wikia.nocookie.net/b__/images/8/83/ApopalypseIconBTD6.png/revision/latest?cb=20190815203831&path-prefix=bloons",
    "Standard (Hard)": "https://static.wikia.nocookie.net/b__/images/3/31/ModeSelectHardBtn.png/revision/latest?cb=20200613080342&path-prefix=bloons",
    "Alternate Bloons Round": "https://static.wikia.nocookie.net/b__/images/1/17/AlternateBloonsBtn.png/revision/latest?cb=20230119032602&path-prefix=bloons",
    "Impoppable": "https://static.wikia.nocookie.net/b__/images/0/0f/ImpoppableBtn.png/revision/latest?cb=20230512114313&path-prefix=bloons",
    "CHIMPS": "https://static.wikia.nocookie.net/b__/images/f/f3/CHIMPSIconBTD6.png/revision/latest?cb=20230509072408&path-prefix=bloons",
    "Magic Only": "https://static.wikia.nocookie.net/b__/images/f/fc/MagicBtn.png/revision/latest?cb=20200615103706&path-prefix=bloons",
    "Double HP Moabs": "https://static.wikia.nocookie.net/b__/images/c/ca/DoubleHpMoabsBtn.png/revision/latest?cb=20200624234326&path-prefix=bloons",
    "Half Cash": "https://static.wikia.nocookie.net/b__/images/0/07/HalfMoneyBtn.png/revision/latest?cb=20230512114448&path-prefix=bloons",
}

# --- HERO IMAGES ---
hero_images = {
    "Quincy": "https://static.wikia.nocookie.net/b__/images/a/a8/QuincyPortrait.png/revision/latest?cb=20190612021048&path-prefix=bloons",
    "Gwendolin": "https://static.wikia.nocookie.net/b__/images/b/b9/GwendolinPortrait.png/revision/latest?cb=20190612022457&path-prefix=bloons",
    "Obyn Greenfoot": "https://static.wikia.nocookie.net/b__/images/7/72/ObynGreenFootPortrait.png/revision/latest?cb=20190612023839&path-prefix=bloons",
    "Admiral Brickell": "https://static.wikia.nocookie.net/b__/images/4/4d/AdmiralBrickellPortrait.png/revision/latest?cb=20200602105905&path-prefix=bloons",
    "Silas": "https://static.wikia.nocookie.net/b__/images/a/a2/SilasPortrait.png/revision/latest?cb=20250827063052&path-prefix=bloons",
    "Striker Jones": "https://static.wikia.nocookie.net/b__/images/b/b4/StrikerJonesPortrait.png/revision/latest?cb=20190612023137&path-prefix=bloons"
}

# --- TOWER IMAGES ---
tower_images = {
    "Dart Monkey": "https://static.wikia.nocookie.net/b__/images/b/b2/000-DartMonkey.png/revision/latest?cb=20190522014750&path-prefix=bloons",
    "Boomerang Monkey": "https://static.wikia.nocookie.net/b__/images/5/51/BTD6_Boomerang_Monkey.png/revision/latest?cb=20180616145853&path-prefix=bloons",
    "Bomb Shooter": "https://static.wikia.nocookie.net/b__/images/e/e1/Bomb_Shooter.png/revision/latest?cb=20180616145810&path-prefix=bloons",
    "Tack Shooter": "https://static.wikia.nocookie.net/b__/images/1/15/BTD6_Tack_Shooter.png/revision/latest?cb=20180616150423&path-prefix=bloons",
    "Ice Monkey": "https://static.wikia.nocookie.net/b__/images/f/fb/Ice_Monkey.png/revision/latest?cb=20180616145956&path-prefix=bloons",
    "Glue Gunner": "https://static.wikia.nocookie.net/b__/images/3/37/000-GlueGunner.png/revision/latest?cb=20190522014752&path-prefix=bloons",
    "Desperado": "https://static.wikia.nocookie.net/b__/images/6/64/000-Desperado.png/revision/latest?cb=20250618065544&path-prefix=bloons",
    "Sniper Monkey": "https://static.wikia.nocookie.net/b__/images/f/ff/BTD6_Sniper_Monkey.png/revision/latest?cb=20180616150336&path-prefix=bloons",
    "Monkey Sub": "https://static.wikia.nocookie.net/b__/images/e/e9/BTD6_Monkey_Sub.png/revision/latest?cb=20180616150211&path-prefix=bloons",
    "Monkey Buccaneer": "https://static.wikia.nocookie.net/b__/images/8/87/BTD6_Monkey_Buccaneer.png/revision/latest?cb=20180616150146&path-prefix=bloons",
    "Monkey Ace": "https://static.wikia.nocookie.net/b__/images/0/04/BTD6_Monkey_Ace.png/revision/latest?cb=20180616150015&path-prefix=bloons",
    "Heli Pilot": "https://static.wikia.nocookie.net/b__/images/e/e7/BTD6_Heli_Pilot.png/revision/latest?cb=20180616145943&path-prefix=bloons",
    "Mortar Monkey": "https://static.wikia.nocookie.net/b__/images/8/8d/000-MortarMonkey.png/revision/latest?cb=20190522015009&path-prefix=bloons",
    "Dartling Gunner": "https://static.wikia.nocookie.net/b__/images/f/f3/000-DartlingGunner.png/revision/latest?cb=20201203034034&path-prefix=bloons",
    "Wizard Monkey": "https://static.wikia.nocookie.net/b__/images/9/99/000-WizardMonkey.png/revision/latest?cb=20190522015102&path-prefix=bloons",
    "Super Monkey": "https://static.wikia.nocookie.net/b__/images/3/3d/000-SuperMonkey.png/revision/latest?cb=20190522015101&path-prefix=bloons",
    "Ninja Monkey": "https://static.wikia.nocookie.net/b__/images/2/28/000-NinjaMonkey.png/revision/latest?cb=20190522015010&path-prefix=bloons",
    "Alchemist": "https://static.wikia.nocookie.net/b__/images/6/65/Monkey_Alchemist.png/revision/latest?cb=20220804022938&path-prefix=bloons",
    "Druid": "https://static.wikia.nocookie.net/b__/images/7/79/Druid_Monkey.png/revision/latest?cb=20180616151044&path-prefix=bloons",
    "Mermonkey": "https://static.wikia.nocookie.net/b__/images/f/f4/000-Mermonkey.png/revision/latest?cb=20240801065305&path-prefix=bloons",
    "Banana Farm": "https://static.wikia.nocookie.net/b__/images/c/cb/000-BananaFarm.png/revision/latest?cb=20190522014608&path-prefix=bloons",
    "Spike Factory": "https://static.wikia.nocookie.net/b__/images/f/f6/000-SpikeFactory.png/revision/latest?cb=20190522015011&path-prefix=bloons",
    "Monkey Village": "https://static.wikia.nocookie.net/b__/images/8/8b/000-MonkeyVillage.png/revision/latest?cb=20190522015009&path-prefix=bloons",
    "Engineer Monkey": "https://static.wikia.nocookie.net/b__/images/9/98/000-EngineerMonkey.png/revision/latest?cb=20190921173225&path-prefix=bloons",
    "Beast Handler": "https://static.wikia.nocookie.net/b__/images/5/54/000-BeastHandler.png/revision/latest?cb=20230404070911&path-prefix=bloons",
}

# --- Tower groups & randomizer logic (your rules) ---
primary_towers = [
    "Dart Monkey", "Boomerang Monkey", "Bomb Shooter", "Tack Shooter",
    "Ice Monkey", "Glue Gunner", "Desperado"
]

military_towers = [
    "Sniper Monkey", "Monkey Sub", "Monkey Buccaneer", "Monkey Ace",
    "Heli Pilot", "Mortar Monkey", "Dartling Gunner"
]

magic_towers = [
    "Wizard Monkey", "Super Monkey", "Ninja Monkey",
    "Alchemist", "Druid", "Mermonkey"
]

support_towers = [
    "Banana Farm", "Spike Factory", "Monkey Village", "Engineer Monkey", "Beast Handler"
]

all_towers = primary_towers + military_towers + magic_towers + support_towers

tower_order = primary_towers + military_towers + magic_towers + support_towers

def randomize_btd6_setup():
    mode = random.choice(modes)
    map_choice = random.choice(maps)
    has_water = map_choice["water"]

    valid_heroes = [h for h in heroes if has_water or h != "Admiral Brickell"]
    hero = random.choice(valid_heroes)

    if mode == "Primary Only":
        valid_towers = primary_towers[:]
    elif mode == "Military Only":
        valid_towers = military_towers[:]
    elif mode == "Magic Only":
        valid_towers = magic_towers[:]
    elif mode == "CHIMPS":
        valid_towers = [t for t in all_towers if t != "Banana Farm"]
    else:
        valid_towers = all_towers[:]

    if not has_water:
        invalid = ("Monkey Sub", "Monkey Buccaneer", "Beast Handler")
        valid_towers = [t for t in valid_towers if t not in invalid]

    tower_selection = []
    while len(tower_selection) < 5:
        tower = random.choice(valid_towers)
        if tower_selection.count(tower) < 3:
            tower_selection.append(tower)

    # Sort towers in BTD6 order
    tower_selection.sort(key=lambda t: tower_order.index(t))


    return mode, map_choice, hero, tower_selection

# --- PAGE CONFIG & CSS ---
st.set_page_config(page_title="BTD6 Randomizer", page_icon="🎯")
st.markdown("""
<style>
.btd6-box { background-color: #1e1e1e; border-radius: 12px; padding: 16px; margin-top: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4); text-align: center; }
.btd6-map { border: 2px solid #3498db; }
.btd6-mode { border: 2px solid #e74c3c; }
.btd6-hero { border: 2px solid #9b59b6; }
.btd6-towers { border: 2px solid #2ecc71; display: flex; justify-content: space-around; flex-wrap: wrap; }
.btd6-box img { display: block; margin: 10px auto; max-width: 100%; height: auto; }
h1,h2,h3 { color: #f1c40f !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 BTD6 Randomizer")
st.write("Randomly generate a game setup with mode, map, hero, and 5 towers.")

# --- RANDOMIZE BUTTON ---
if st.button("🎲 Randomize Setup"):
    mode, map_choice, hero, towers = randomize_btd6_setup()

    col1, col2 = st.columns([2,1])

    # --- MAP ---
    with col1:
        maps_url = maps_images.get(map_choice['name'])
        maps_src = ensure_image(map_choice['name'], maps_url) if maps_url else None
        maps_b64 = img_to_base64(maps_src) if maps_src else None
        st.markdown(f"""
        <div class="btd6-box btd6-map">
            <h3>Map</h3>
            <p><b>{map_choice['name']}</b></p>
            {f'<img src="{maps_b64}" width="300">' if maps_b64 else ''}
        </div>
        """, unsafe_allow_html=True)

    # --- MODE ---
    with col2:
        mode_url = mode_images.get(mode)
        mode_src = ensure_image(mode, mode_url) if mode_url else None
        mode_b64 = img_to_base64(mode_src) if mode_src else None
        st.markdown(f"""
        <div class="btd6-box btd6-mode">
            <h3>Mode</h3>
            <p><b>{mode}</b></p>
            {f'<img src="{mode_b64}" width="150">' if mode_b64 else ''}
        </div>
        """, unsafe_allow_html=True)

    # --- HERO ---
    hero_url = hero_images.get(hero)
    hero_src = ensure_image(hero, hero_url) if hero_url else None
    hero_b64 = img_to_base64(hero_src) if hero_src else None
    st.markdown(f"""
    <div class="btd6-box btd6-hero">
        <h3>Hero</h3>
        <p><b>{hero}</b></p>
        {f'<img src="{hero_b64}" width="200">' if hero_b64 else ''}
    </div>
    """, unsafe_allow_html=True)

    # --- TOWERS ---
    tower_html = ""
    for t in towers:
        t_url = tower_images.get(t)
        t_src = ensure_image(t, t_url) if t_url else None
        t_b64 = img_to_base64(t_src) if t_src else None
        tower_html += f'<div><b>{t}</b><br>{f"<img src=\"{t_b64}\" width=\"100\">" if t_b64 else ""}</div>'

    st.markdown(f"""
    <div class="btd6-box btd6-towers">
        <h3>Towers</h3>
        {tower_html}
    </div>
    """, unsafe_allow_html=True)
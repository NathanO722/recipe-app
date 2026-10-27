"""
World Recipe App — Editorial Culinary Studio (Single-File Edition)

Design Highlights:
- Warm Alabaster & Pure White minimal palette (#F8F9FA background, #FFFFFF cards, #E8EAED borders)
- Single refined terracotta culinary accent (#D94E28) and deep charcoal typography (#18181B)
- Full-bleed Real Food Photo Hero Banner embedded at the top of the landing page
- Proportionally aligned, rounded-corner Real Food Photographs inside every button
- Self-installing dependencies (customtkinter, requests, Pillow) in a single runnable Python file

Run with: python "recipe app.py"
"""

import base64
import json
import os
import re
import subprocess
import sys
import threading
import webbrowser
from io import BytesIO
from urllib.parse import quote_plus


def _ensure_dependencies():
    """Automatically install required third-party packages if missing."""
    required = {
        "customtkinter": "customtkinter",
        "requests": "requests",
        "PIL": "Pillow",
    }
    missing = []
    for mod_name, pip_name in required.items():
        try:
            __import__(mod_name)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print(f"Installing required packages ({', '.join(missing)})... Please wait.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


_ensure_dependencies()

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

APP_DIR = os.path.dirname(os.path.abspath(__file__))
FAVOURITES_FILE = os.path.join(APP_DIR, "favourites.json")
API_BASE = "https://www.themealdb.com/api/json/v1/1"
HTTP_HEADERS = {
    "User-Agent": "WorldRecipeAppBot/1.0 (https://example.org; contact@example.org) python-requests/2.31"
}

# Proportional, uniform image dimensions
HERO_BANNER_SIZE = (980, 145)
SPOTLIGHT_IMG_SIZE = (216, 118)
CARD_THUMB_SIZE = (76, 58)
NAV_THUMB_SIZE = (36, 28)
CAT_THUMB_SIZE = (28, 22)
DETAIL_BANNER_SIZE = (500, 240)

# Clean, bright light editorial mode by default
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

# Cohesive 3-tone Professional Design Tokens
COLOR_APP_BG = ("#F6F7F9", "#121316")
COLOR_SURFACE = ("#FFFFFF", "#1B1D22")
COLOR_SURFACE_ALT = ("#F1F3F6", "#24272E")
COLOR_BORDER = ("#E2E6EC", "#2E323B")
COLOR_TEXT_PRIMARY = ("#14171A", "#F3F4F6")
COLOR_TEXT_MUTED = ("#656D78", "#9CA3AF")
COLOR_ACCENT = ("#D94E28", "#E05A34")
COLOR_ACCENT_HOVER = ("#B83D1B", "#C44825")
COLOR_ACCENT_SOFT = ("#FFF1ED", "#331D17")

# ---------------------------------------------------------------------------
# Embedded Real Food Photographs (JPEG Base64)
# ---------------------------------------------------------------------------
EMBEDDED_REAL_PHOTOS_B64 = {
    "local_jollof": (
        "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"
    ),
    "local_eba": (
        "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"
    ),
    "local_egusi": (
        "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"
        "LHqzMhwjXPXbyEeWavTvzqCO8LHK9MXONDiR7Q6k1WhhsIlUVH3xDADOVj0KZ9E4Lr1tRQ7YHqZdc6FyEYHHoZ844PqzVYFJ2m50"
        "FiNWOQAZ9JphITJFkDOJg87T3MamAeNOkWM6WUF0dFek0tOnoXlqqQIo9AIbMgG9J6TvtCbvspKkes0gTPC0G7QWwqPLWG8R1FoR"
        "ST0EPa2xmb+odcKqSitvFylSCSso/qDiJttZVOwmadskw2ps53JJizmYZys0xjRBjFdRaK0JJhbGwJQ8Y1WFcHICnA94icqQ2MbE"
        "eL63Jx94+vpM7a2XLjJY+sYusNrFm6dYm2HzkmBCPsczxypKlsFu28jcSc+GhPrjsZ5VV4LrYRkjflYQtBZ7HCZyd9t4zrYCdkdK"
        "bMLgDKnIJhbCQ5D5JHvtPHY0thT5s4M5vPk5BzsRAbsND1PEak0rU6mtmQnJwPvDbb9IGu/Q2Nd4VVikjyqx2Xb5/rBclTFPH8tX"
        "8xHU7Hb8TgZ9532eusq1RLoQG3x+WxlJJKypW2GXTvdpQ5swiqPKT1PpHdLqdBpVD6qp31CHmQL8d8xbiHEmtcCtFqGAAiDA6Ql1"
        "VlelWyoOb3wWGx37fAgd9hddHalqbqbrjXThkA8IMVNbHOcA+/ptKzhfDm12tXTqy1M2d2yQMDPb4lnZpLUtGnZCbSA7Cwqd+vX0"
        "lyvD2oZbKtZWmpAKs1bAZJzkDsBiE8nFaB4cuxSm66ix0qdBaSUUVKVUdRsBGtVYanTTWMiGvlQ+UnAUDfBwd8794Gniw02l8Kms"
        "C0HzMR1PQ/nK3Va6/UW1eMpdKjkKdgR6D8IlXJ7GuktF5w7T/a7LV0qJlkB83TPr87zzWcMp0z2HUW+NqSpZiBjlPv67A7esphxG"
        "yusUadGQdu8d4Rbp7ltPES7v0+/jl2OPnfEqpR2XaZ2jpD6qpjpQ1ZGeUt9447/j2guI6GoXPy04QnPlywT2z+ca4dq3e1KVsCgc"
        "yqCdiegx+Eb1DazRNdYbKjWoCitQGVycd9sY2+O0u3YLdGTvoahmUDoSMGKgsxw65xviX2rPjVorFfEO9vlxv6D2lfqK6SU8FXU4"
        "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"
    ),
    "local_moimoi": (
        "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"
    ),
    "local_akara": (
        "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"
    ),
    "local_suya": (
        "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"
    ),
    "cat_pasta": (
        "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"
    ),
    "cat_chicken": (
        "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"
        "/jZ/pWVlZXnLJuy//9k="
    ),
    "cat_seafood": (
        "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"
    ),
    "cat_dessert": (
        "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"
        "a7Xa7RJkz//Z"
    ),
    "cat_beef": (
        "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"
    ),
}


def load_embedded_real_photo(photo_key):
    """Decode one of the embedded real JPEG food photographs into a PIL Image."""
    b64_data = EMBEDDED_REAL_PHOTOS_B64.get(photo_key) or EMBEDDED_REAL_PHOTOS_B64["local_jollof"]
    raw_bytes = base64.b64decode(b64_data)
    return Image.open(BytesIO(raw_bytes)).convert("RGB")


def make_rounded_photo(pil_image, size, radius=10):
    """
    Center-crop a real food photograph to exact `size` proportions and apply
    smooth anti-aliased rounded corners so every button image aligns cleanly.
    """
    target_w, target_h = size
    img = pil_image.convert("RGB")
    src_w, src_h = img.size
    target_ratio = target_w / max(1, target_h)
    src_ratio = src_w / max(1, src_h)

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = ImageEnhance.Color(img).enhance(1.05)

    if radius <= 0:
        return img

    # Super-sampled alpha mask for crisp rounded corners
    scale = 2
    mask = Image.new("L", (target_w * scale, target_h * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [0, 0, target_w * scale - 1, target_h * scale - 1],
        radius=radius * scale,
        fill=255,
    )
    mask = mask.resize((target_w, target_h), Image.Resampling.LANCZOS)

    rgba = img.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def create_editorial_hero_banner(photos_dict, size=(980, 145)):
    """
    Create a wide, magazine-style culinary hero banner with real food photography
    embedded in the background and a warm dark gradient on the left for crisp typography.
    """
    w, h = size
    banner = Image.new("RGB", (w, h), (24, 22, 20))

    # Stitch 4 vibrant real food photos seamlessly across the right 72% of the banner
    keys = ["local_jollof", "cat_pasta", "local_suya", "cat_seafood"]
    tile_w = int(w * 0.22)
    start_x = w - (tile_w * len(keys))
    for i, k in enumerate(keys):
        raw = photos_dict.get((k, "raw"))
        if raw:
            tile = make_rounded_photo(raw, (tile_w, h), radius=0).convert("RGB")
            banner.paste(tile, (start_x + i * tile_w, 0))

    # Apply a smooth horizontal dark editorial gradient overlay so text on the left is 100% legible
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for x in range(w):
        if x < int(w * 0.34):
            alpha = 238
        elif x < int(w * 0.82):
            progress = (x - int(w * 0.34)) / max(1, int(w * 0.48))
            alpha = int(238 * (1 - progress * 0.72))
        else:
            alpha = 65
        odraw.line([(x, 0), (x, h)], fill=(20, 20, 22, alpha))

    combined = Image.alpha_composite(banner.convert("RGBA"), overlay)

    # Render clean editorial title text onto the banner
    tdraw = ImageDraw.Draw(combined)
    try:
        font_tag = ImageFont.truetype("segoeui.ttf", 12)
        font_title = ImageFont.truetype("segoeuib.ttf", 26)
        font_sub = ImageFont.truetype("segoeui.ttf", 14)
    except OSError:
        font_tag = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Accent pill badge
    tdraw.rounded_rectangle([28, 22, 198, 44], radius=6, fill=(217, 78, 40, 255))
    tdraw.text((38, 25), "WORLD CULINARY STUDIO", fill=(255, 255, 255), font=font_tag)

    tdraw.text(
        (28, 54),
        "Authentic Nigerian & Global Recipes",
        fill=(255, 255, 255),
        font=font_title,
    )
    tdraw.text(
        (28, 94),
        "Click any real dish photograph below to view ingredients, prep times, and step-by-step guides.",
        fill=(225, 228, 232),
        font=font_sub,
    )

    return make_rounded_photo(combined.convert("RGB"), size, radius=14)


def choose_fallback_photo_key(recipe_or_hint):
    """Pick the closest embedded real food photograph key for any recipe or category."""
    if isinstance(recipe_or_hint, dict):
        rid = recipe_or_hint.get("id", "")
        if rid in EMBEDDED_REAL_PHOTOS_B64:
            return rid
        text = f"{recipe_or_hint.get('name', '')} {recipe_or_hint.get('category', '')}".lower()
    else:
        text = str(recipe_or_hint).lower()
        if text in EMBEDDED_REAL_PHOTOS_B64:
            return text

    if "jollof" in text or "rice" in text:
        return "local_jollof"
    if "egusi" in text or "soup" in text or "stew" in text:
        return "local_egusi"
    if "eba" in text or "swallow" in text or "garri" in text:
        return "local_eba"
    if "moi" in text:
        return "local_moimoi"
    if "akara" in text or "bean" in text:
        return "local_akara"
    if "suya" in text or "kebab" in text or "skewer" in text:
        return "local_suya"
    if "pasta" in text or "italian" in text or "noodle" in text:
        return "cat_pasta"
    if "seafood" in text or "fish" in text or "prawn" in text or "salmon" in text:
        return "cat_seafood"
    if "dessert" in text or "cake" in text or "sweet" in text or "tart" in text:
        return "cat_dessert"
    if "beef" in text or "steak" in text or "pie" in text or "meat" in text:
        return "cat_beef"
    if "chicken" in text or "curry" in text or "grill" in text:
        return "cat_chicken"
    return "local_jollof"


def make_recipe(recipe_id, name, country, category, ingredients, instructions,
                video_query=None, image="", prep_time="35 mins"):
    """Create one recipe dictionary in the same format used by API recipes."""
    return {
        "id": recipe_id,
        "name": name,
        "country": country,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions,
        "image": image,
        "video": "",
        "video_query": video_query or f"how to cook {name}",
        "source": "Built-in recipe",
        "prep_time": prep_time,
    }


NIGERIAN_RECIPES = [
    make_recipe(
        "local_jollof", "Nigerian Jollof Rice", "Nigeria", "Rice",
        ["2 cups long-grain parboiled rice", "3 plum tomatoes, blended",
         "1 large red bell pepper (tatashe), blended", "1 medium red onion, chopped",
         "2 tablespoons rich tomato paste", "2 cups seasoned chicken or beef stock",
         "3 tablespoons vegetable oil", "1 teaspoon curry powder & 1 teaspoon dried thyme",
         "2 bay leaves, salt, and scotch bonnet pepper to taste"],
        ["Wash the parboiled rice in cool water until the water runs clear, then drain.",
         "Blend the plum tomatoes, red bell pepper, and half an onion into a smooth crimson puree.",
         "Heat vegetable oil in a heavy pot over medium heat and sauté the sliced onions until fragrant.",
         "Stir in the tomato paste and fry for 3 minutes, then pour in the blended pepper mixture and simmer until reduced and thick.",
         "Add the stock, curry powder, thyme, bay leaves, and salt, bringing the base to a lively boil.",
         "Stir in the washed rice, cover tightly with foil and a lid, and steam on low heat until the grains are tender and smoky.",
         "Fluff gently with a wooden spoon and serve with fried plantains or grilled chicken."],
        "Nigerian jollof rice recipe",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/6/67/Nigerian_jollof_rice.jpg/960px-Nigerian_jollof_rice.jpg",
        prep_time="45 mins",
    ),
    make_recipe(
        "local_egusi", "Egusi Soup", "Nigeria", "Soup",
        ["1½ cups ground egusi (melon seeds)", "3 tablespoons red palm oil",
         "1 medium onion, finely chopped", "2 cups rich meat or fish stock",
         "2 cups fresh fluted pumpkin leaves (ugu) or spinach, shredded",
         "2 tablespoons ground crayfish", "Assorted cooked meat, stockfish, or smoked fish",
         "Scotch bonnet pepper and seasoning cubes to taste"],
        ["Whisk the ground egusi with ½ cup of warm water in a bowl to form a thick, lumpy paste.",
         "Warm the palm oil in a pot over medium heat and sauté the chopped onion for 1 minute.",
         "Spoon the egusi paste into the oil in small mounds and fry gently for 5 minutes until nutty and golden.",
         "Pour in the meat stock, ground crayfish, pepper, and cooked meats; cover and simmer for 12 minutes.",
         "Fold in the shredded green leaves and simmer uncovered for 3 minutes so the greens stay vibrant.",
         "Taste for seasoning and serve piping hot alongside Eba or pounded yam."],
        "Nigerian egusi soup recipe",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2c/Egusi_soup_and_Eba.jpg/960px-Egusi_soup_and_Eba.jpg",
        prep_time="40 mins",
    ),
    make_recipe(
        "local_suya", "Suya Grilled Skewers", "Nigeria", "Grilled",
        ["500 g thinly sliced beef sirloin or chicken breast",
         "3 tablespoons yaji (roasted peanut & spice powder)",
         "1 teaspoon smoked paprika & 1 teaspoon ginger powder",
         "1 teaspoon garlic powder & ½ teaspoon cayenne pepper",
         "2 tablespoons peanut or vegetable oil", "1 red onion & 1 fresh tomato, sliced for serving"],
        ["Combine the roasted peanut powder, paprika, ginger, garlic, salt, and cayenne in a wide tray.",
         "Brush the thinly sliced beef strips with oil, then press firmly into the suya spice blend to coat both sides.",
         "Thread the spiced beef ribbons onto soaked wooden skewers and rest for 20 minutes.",
         "Grill over hot charcoal or broil in a high oven for 6–8 minutes per side until charred and juicy.",
         "Serve immediately on a platter with crisp red onion rings, fresh tomatoes, and extra yaji spice."],
        "Nigerian suya recipe",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/5/54/Suya.jpg/960px-Suya.jpg",
        prep_time="30 mins",
    ),
    make_recipe(
        "local_moimoi", "Moi Moi", "Nigeria", "Beans",
        ["2 cups peeled brown or black-eyed beans", "1 large red bell pepper (tatashe)",
         "1 medium onion", "¼ cup vegetable oil or melted butter",
         "1 cup warm fish or chicken stock", "2 hard-boiled eggs, sliced (optional)",
         "1 tablespoon ground crayfish, salt, and seasoning"],
        ["Soak the peeled beans in cool water for 1 hour, rinse thoroughly, and drain.",
         "Blend the beans with red bell pepper, onion, crayfish, and warm stock until silky smooth.",
         "Whisk in the vegetable oil and seasoning until the batter turns glossy and airy.",
         "Ladle into greased ramekins, pouches, or banana leaves, topping each portion with a slice of boiled egg.",
         "Steam in a covered pot with simmering water for 45 minutes until firm and cooked through.",
         "Cool slightly for 5 minutes before serving."],
        "Nigerian moi moi recipe",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c8/Images_of_a_local_dish_in_Nigeria_called_Moi-Moi.jpg/960px-Images_of_a_local_dish_in_Nigeria_called_Moi-Moi.jpg",
        prep_time="55 mins",
    ),
    make_recipe(
        "local_akara", "Akara (Bean Cakes)", "Nigeria", "Beans",
        ["2 cups peeled black-eyed beans", "1 small red onion, finely diced",
         "1 fresh scotch bonnet or habanero pepper", "Salt to taste",
         "Vegetable oil for deep frying"],
        ["Soak the peeled beans for 30 minutes, drain well, and blend with minimal water until thick.",
         "Whisk the bean batter vigorously with a wooden spoon for 3–4 minutes to incorporate air.",
         "Fold in the finely diced onion, minced pepper, and salt right before frying so the batter stays fluffy.",
         "Heat 2 inches of oil in a deep pan to 180°C (350°F).",
         "Scoop rounded spoonfuls into the hot oil and fry for 3–4 minutes per side until crisp and golden brown.",
         "Drain on paper towels and enjoy warm."],
        "Nigerian akara bean cakes recipe",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/4/45/Akara.jpg/960px-Akara.jpg",
        prep_time="25 mins",
    ),
    make_recipe(
        "local_eba", "Eba Swallow", "Nigeria", "Swallow",
        ["2 cups yellow or white garri (cassava granules)", "2 cups freshly boiled water"],
        ["Pour the boiling water into a clean, heat-safe mixing bowl.",
         "Sprinkle the garri evenly across the water in a circular motion until it settles.",
         "Wait 1 minute for the granules to absorb the hot water, then fold firmly with a wooden paddle.",
         "Work the dough against the side of the bowl until smooth, elastic, and lump-free.",
         "Shape into a neat dome and serve warm alongside Egusi, Okra, or Ogbono soup."],
        "how to make Nigerian eba",
        image="https://thumb.wikimedia.org/wikipedia/commons/thumb/8/85/Eba_Swallow.jpg/960px-Eba_Swallow.jpg",
        prep_time="10 mins",
    ),
]

COUNTRY_OPTIONS = [
    "All countries", "Nigeria", "American", "British", "Canadian", "Chinese",
    "Croatian", "Dutch", "Egyptian", "Filipino", "French", "Greek", "Indian",
    "Irish", "Italian", "Jamaican", "Japanese", "Kenyan", "Malaysian",
    "Mexican", "Moroccan", "Polish", "Portuguese", "Russian", "Spanish",
    "Thai", "Tunisian", "Turkish", "Vietnamese"
]

QUICK_CATEGORIES = [
    ("All Dishes", "", "local_jollof"),
    ("Nigerian", "Nigeria", "local_egusi"),
    ("Pasta & Rice", "pasta", "cat_pasta"),
    ("Chicken", "chicken", "cat_chicken"),
    ("Beef & Grill", "beef", "cat_beef"),
    ("Seafood", "seafood", "cat_seafood"),
]


def clean_text(value):
    return str(value).strip() if value else ""


def api_meal_to_recipe(meal):
    ingredients = []
    for number in range(1, 21):
        ingredient = clean_text(meal.get(f"strIngredient{number}"))
        measure = clean_text(meal.get(f"strMeasure{number}"))
        if ingredient:
            ingredients.append(f"{measure} {ingredient}".strip())

    name = clean_text(meal.get("strMeal")) or "Untitled recipe"
    category = clean_text(meal.get("strCategory")) or "International"
    return {
        "id": "api_" + clean_text(meal.get("idMeal")),
        "api_id": clean_text(meal.get("idMeal")),
        "name": name,
        "country": clean_text(meal.get("strArea")) or "Global",
        "category": category,
        "ingredients": ingredients or ["No ingredient list was supplied by the API."],
        "instructions": clean_text(meal.get("strInstructions")) or "No instructions were supplied.",
        "image": clean_text(meal.get("strMealThumb")),
        "video": clean_text(meal.get("strYoutube")),
        "video_query": f"how to cook {name}",
        "source": "TheMealDB API",
        "prep_time": "35 mins",
    }


def load_favourites():
    try:
        with open(FAVOURITES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def save_favourites(favourites):
    with open(FAVOURITES_FILE, "w", encoding="utf-8") as file:
        json.dump(favourites, file, indent=2, ensure_ascii=False)


class WorldRecipeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("World Recipe Studio — Culinary Explorer")
        self.geometry("1320x860")
        self.minsize(1080, 720)
        self.configure(fg_color=COLOR_APP_BG)

        self.recipes = list(NIGERIAN_RECIPES)
        self.visible_recipes = list(self.recipes)
        self.favourites = load_favourites()
        self.selected_recipe = None
        self.showing_favourites = False
        self.active_nav = "all"

        # Pre-populate cache with embedded real food photographs
        self.pil_cache = {}
        for key in EMBEDDED_REAL_PHOTOS_B64:
            self.pil_cache[(key, "raw")] = load_embedded_real_photo(key)

        self.ctk_image_refs = []
        self.hero_buttons = []
        self.nav_buttons = {}
        self.hero_recipes = [
            NIGERIAN_RECIPES[0],
            NIGERIAN_RECIPES[1],
            NIGERIAN_RECIPES[2],
            NIGERIAN_RECIPES[3],
        ]
        self.card_buttons = {}
        self.detail_image_label = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main_area()

        self.render_recipe_list(self.visible_recipes)
        if self.visible_recipes:
            self.select_recipe(self.visible_recipes[0])

        self.set_status("Ready • Click any dish photo card to view its recipe.")
        threading.Thread(target=self.load_startup_foods, daemon=True).start()

    # -----------------------------------------------------------------------
    # Proportional Rounded Real-Photo Helpers
    # -----------------------------------------------------------------------
    def get_recipe_pil_image(self, recipe, size, radius=10):
        recipe_id = recipe.get("id") or recipe.get("name", "food")
        cache_key = (recipe_id, size, radius)
        if cache_key in self.pil_cache:
            return self.pil_cache[cache_key]

        raw_key = (recipe_id, "raw")
        if raw_key in self.pil_cache:
            raw_img = self.pil_cache[raw_key]
        else:
            fallback_key = choose_fallback_photo_key(recipe)
            raw_img = self.pil_cache[(fallback_key, "raw")]

        fitted = make_rounded_photo(raw_img, size, radius=radius)
        self.pil_cache[cache_key] = fitted
        return fitted

    def get_key_pil_image(self, photo_key, size, radius=8):
        cache_key = (photo_key, size, radius)
        if cache_key in self.pil_cache:
            return self.pil_cache[cache_key]
        raw_img = self.pil_cache.get((photo_key, "raw")) or load_embedded_real_photo("local_jollof")
        fitted = make_rounded_photo(raw_img, size, radius=radius)
        self.pil_cache[cache_key] = fitted
        return fitted

    def make_ctk_image(self, pil_img, size):
        c_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        self.ctk_image_refs.append(c_img)
        return c_img

    # -----------------------------------------------------------------------
    # Clean, Cohesive Sidebar Navigation
    # -----------------------------------------------------------------------
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=250, corner_radius=0,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Brand Header
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=20, pady=(24, 18))

        brand_pil = self.get_key_pil_image("local_jollof", (46, 46), radius=10)
        brand_ctk = self.make_ctk_image(brand_pil, (46, 46))
        ctk.CTkLabel(brand_frame, text="", image=brand_ctk).pack(side="left", padx=(0, 12))

        title_box = ctk.CTkFrame(brand_frame, fg_color="transparent")
        title_box.pack(side="left", fill="x")
        ctk.CTkLabel(
            title_box, text="CULINARY STUDIO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLOR_ACCENT,
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box, text="World Recipes",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.sidebar, text="COLLECTIONS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
        ).pack(padx=20, pady=(6, 6), anchor="w")

        # Uniform, proportional sidebar buttons with real food thumbnails
        nav_items = [
            ("all", "Explore All Dishes", "cat_pasta", self.show_all_recipes),
            ("nigeria", "Nigerian Classics", "local_jollof", self.show_nigerian_recipes),
            ("fav", "Saved Favourites", "cat_dessert", self.show_favourites),
            ("random", "Surprise Me Dish", "cat_chicken", self.load_random_spotlight),
        ]
        for nav_id, label_text, photo_key, cmd in nav_items:
            thumb_pil = self.get_key_pil_image(photo_key, NAV_THUMB_SIZE, radius=6)
            thumb_ctk = self.make_ctk_image(thumb_pil, NAV_THUMB_SIZE)
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {label_text}",
                image=thumb_ctk,
                compound="left",
                anchor="w",
                height=44,
                corner_radius=10,
                border_width=1,
                border_color=COLOR_BORDER,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=COLOR_SURFACE_ALT,
                text_color=COLOR_TEXT_PRIMARY,
                hover_color=COLOR_ACCENT_SOFT,
                command=cmd,
            )
            btn.pack(padx=16, pady=4, fill="x")
            self.nav_buttons[nav_id] = btn

        self.highlight_nav("all")

        ctk.CTkLabel(
            self.sidebar, text="COUNTRY FILTER",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
        ).pack(padx=20, pady=(20, 6), anchor="w")

        self.country_var = ctk.StringVar(value="All countries")
        self.country_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=COUNTRY_OPTIONS,
            variable=self.country_var,
            height=38,
            corner_radius=10,
            fg_color=COLOR_SURFACE_ALT,
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda _value: self.on_country_selected(_value),
        )
        self.country_menu.pack(padx=16, pady=(0, 16), fill="x")

        ctk.CTkLabel(
            self.sidebar, text="APPEARANCE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
        ).pack(padx=20, pady=(6, 6), anchor="w")

        self.theme_switch = ctk.CTkSegmentedButton(
            self.sidebar,
            values=["Light", "Dark"],
            selected_color=COLOR_ACCENT,
            selected_hover_color=COLOR_ACCENT_HOVER,
            command=lambda mode: ctk.set_appearance_mode(mode),
        )
        self.theme_switch.set("Light")
        self.theme_switch.pack(padx=16, pady=(0, 12), fill="x")

        ctk.CTkLabel(
            self.sidebar,
            text="Built-in Nigerian photography + live global recipes powered by TheMealDB.",
            wraplength=205, justify="left",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_MUTED,
        ).pack(side="bottom", padx=20, pady=20, anchor="w")

    def highlight_nav(self, active_key):
        self.active_nav = active_key
        for k, btn in self.nav_buttons.items():
            if not btn.winfo_exists():
                continue
            if k == active_key:
                btn.configure(
                    fg_color=COLOR_ACCENT,
                    text_color=("#FFFFFF", "#FFFFFF"),
                    border_color=COLOR_ACCENT,
                )
            else:
                btn.configure(
                    fg_color=COLOR_SURFACE_ALT,
                    text_color=COLOR_TEXT_PRIMARY,
                    border_color=COLOR_BORDER,
                )

    # -----------------------------------------------------------------------
    # Main Area: Embedded Food Hero Banner + Proportional Image Cards
    # -----------------------------------------------------------------------
    def build_main_area(self):
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=22, pady=16)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(3, weight=1)

        # 1. Embedded Food Photography Hero Banner + Integrated Search Bar
        hero_container = ctk.CTkFrame(
            self.main,
            corner_radius=16,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        hero_container.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        hero_container.grid_columnconfigure(0, weight=1)

        banner_pil = create_editorial_hero_banner(self.pil_cache, size=HERO_BANNER_SIZE)
        banner_ctk = self.make_ctk_image(banner_pil, HERO_BANNER_SIZE)
        banner_lbl = ctk.CTkLabel(hero_container, text="", image=banner_ctk)
        banner_lbl.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 8))

        # Search & Quick Category Bar inside the Hero Card
        search_bar = ctk.CTkFrame(hero_container, fg_color="transparent")
        search_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search recipes or ingredients (e.g., Jollof, Egusi, Pasta, Chicken, Seafood)...",
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE_ALT,
            text_color=COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(size=13),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda _event: self.search_recipes())

        search_icon_pil = self.get_key_pil_image("local_jollof", (26, 20), radius=4)
        search_icon_ctk = self.make_ctk_image(search_icon_pil, (26, 20))
        ctk.CTkButton(
            search_bar,
            text="Search Recipes",
            image=search_icon_ctk,
            compound="left",
            width=148,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=("#FFFFFF", "#FFFFFF"),
            command=self.search_recipes,
        ).grid(row=0, column=1)

        # 2. Proportional Category Filter Pills with Real Food Thumbnails
        cat_row = ctk.CTkFrame(self.main, fg_color="transparent")
        cat_row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        for idx, (cat_label, query_val, photo_key) in enumerate(QUICK_CATEGORIES):
            cat_row.grid_columnconfigure(idx, weight=1, uniform="cat_col")
            cat_pil = self.get_key_pil_image(photo_key, CAT_THUMB_SIZE, radius=5)
            cat_ctk = self.make_ctk_image(cat_pil, CAT_THUMB_SIZE)
            cat_btn = ctk.CTkButton(
                cat_row,
                text=f" {cat_label}",
                image=cat_ctk,
                compound="left",
                height=38,
                corner_radius=10,
                border_width=1,
                border_color=COLOR_BORDER,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=COLOR_SURFACE,
                text_color=COLOR_TEXT_PRIMARY,
                hover_color=COLOR_ACCENT_SOFT,
                command=lambda q=query_val, lbl=cat_label: self.quick_category_filter(q, lbl),
            )
            cat_btn.grid(row=0, column=idx, sticky="ew", padx=4)

        # 3. 4 Equal-Width Featured Dish Photo Buttons (Uniform Grid Proportions)
        showcase = ctk.CTkFrame(
            self.main,
            corner_radius=14,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        showcase.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        showcase.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="hero_col")

        showcase_header = ctk.CTkFrame(showcase, fg_color="transparent")
        showcase_header.grid(row=0, column=0, columnspan=4, sticky="ew", padx=14, pady=(8, 4))
        ctk.CTkLabel(
            showcase_header,
            text="FEATURED DISHES — CLICK ANY PHOTO CARD",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_ACCENT,
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            showcase_header,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT_MUTED,
        )
        self.status_label.pack(side="right")

        self.hero_buttons = []
        for idx in range(4):
            recipe = self.hero_recipes[idx]
            hero_pil = self.get_recipe_pil_image(recipe, SPOTLIGHT_IMG_SIZE, radius=10)
            hero_ctk = self.make_ctk_image(hero_pil, SPOTLIGHT_IMG_SIZE)

            hero_btn = ctk.CTkButton(
                showcase,
                text=self.format_spotlight_title(recipe),
                image=hero_ctk,
                compound="top",
                height=168,
                corner_radius=12,
                border_width=1,
                border_color=COLOR_BORDER,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=COLOR_SURFACE_ALT,
                text_color=COLOR_TEXT_PRIMARY,
                hover_color=COLOR_ACCENT_SOFT,
                command=lambda r=recipe: self.select_recipe(r),
            )
            hero_btn.grid(row=1, column=idx, sticky="ew", padx=7, pady=(2, 10))
            self.hero_buttons.append(hero_btn)

        # 4. Split View: Aligned Recipe List (Left) & Editorial Recipe Guide (Right)
        content = ctk.CTkFrame(self.main, fg_color="transparent")
        content.grid(row=3, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=5, uniform="split")
        content.grid_columnconfigure(1, weight=7, uniform="split")
        content.grid_rowconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(
            content,
            label_text="Recipe Directory",
            label_font=ctk.CTkFont(size=14, weight="bold"),
            label_fg_color=COLOR_SURFACE_ALT,
            label_text_color=COLOR_TEXT_PRIMARY,
            corner_radius=14,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.details_frame = ctk.CTkScrollableFrame(
            content,
            label_text="Selected Recipe & Instructions",
            label_font=ctk.CTkFont(size=14, weight="bold"),
            label_fg_color=COLOR_SURFACE_ALT,
            label_text_color=COLOR_TEXT_PRIMARY,
            corner_radius=14,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    def format_spotlight_title(self, recipe):
        name = recipe.get("name", "Dish")
        if len(name) > 24:
            name = name[:22] + "…"
        return f"{name}\n{recipe.get('country', 'Global')} • {recipe.get('prep_time', '35 mins')}"

    def format_card_label(self, recipe):
        name = recipe.get("name", "Recipe")
        if len(name) > 30:
            name = name[:28] + "…"
        meta = f"{recipe.get('country', 'Global')} • {recipe.get('category', 'Dish')} • {recipe.get('prep_time', '35 mins')}"
        return f"  {name}\n  {meta}"

    # -----------------------------------------------------------------------
    # Background Loader for Online TheMealDB Dishes & Photos
    # -----------------------------------------------------------------------
    def load_startup_foods(self):
        try:
            for idx in (2, 3):
                response = requests.get(f"{API_BASE}/random.php", headers=HTTP_HEADERS, timeout=8)
                response.raise_for_status()
                meals = (response.json() or {}).get("meals") or []
                if meals:
                    api_recipe = api_meal_to_recipe(meals[0])
                    img_url = api_recipe.get("image", "")
                    if img_url and self.download_and_cache_recipe_photo(api_recipe, img_url):
                        self.hero_recipes[idx] = api_recipe
                        if all(r.get("id") != api_recipe.get("id") for r in self.recipes):
                            self.recipes.append(api_recipe)
        except Exception:
            pass

        try:
            self.after(0, self.refresh_hero_and_cards)
        except Exception:
            pass

    def download_and_cache_recipe_photo(self, recipe, url):
        try:
            resp = requests.get(url, headers=HTTP_HEADERS, timeout=10)
            resp.raise_for_status()
            pil_img = Image.open(BytesIO(resp.content)).convert("RGB")
            recipe_id = recipe.get("id") or recipe.get("name", "food")
            self.pil_cache[(recipe_id, "raw")] = pil_img
            for key in list(self.pil_cache.keys()):
                if key[0] == recipe_id and key[1] != "raw":
                    del self.pil_cache[key]
            return True
        except Exception:
            return False

    def refresh_hero_and_cards(self):
        for idx, btn in enumerate(self.hero_buttons):
            if idx < len(self.hero_recipes) and btn.winfo_exists():
                recipe = self.hero_recipes[idx]
                hero_pil = self.get_recipe_pil_image(recipe, SPOTLIGHT_IMG_SIZE, radius=10)
                hero_ctk = self.make_ctk_image(hero_pil, SPOTLIGHT_IMG_SIZE)
                btn.configure(
                    image=hero_ctk,
                    text=self.format_spotlight_title(recipe),
                    command=lambda r=recipe: self.select_recipe(r),
                )
        self.apply_filters()

    # -----------------------------------------------------------------------
    # Recipe Directory List: Aligned Real-Photo Card Buttons
    # -----------------------------------------------------------------------
    def clear_recipe_list(self):
        self.card_buttons = {}
        for child in self.list_frame.winfo_children():
            child.destroy()

    def render_recipe_list(self, recipes):
        self.clear_recipe_list()
        if not recipes:
            ctk.CTkLabel(
                self.list_frame,
                text="No recipes found.\nTry another search term or country filter.",
                wraplength=240, justify="left",
                font=ctk.CTkFont(size=13),
                text_color=COLOR_TEXT_MUTED,
            ).pack(padx=14, pady=24, anchor="w")
            return

        for recipe in recipes:
            recipe_id = recipe.get("id", recipe["name"])
            thumb_pil = self.get_recipe_pil_image(recipe, CARD_THUMB_SIZE, radius=8)
            thumb_ctk = self.make_ctk_image(thumb_pil, CARD_THUMB_SIZE)

            is_selected = self.selected_recipe and self.selected_recipe.get("id") == recipe_id
            bg_color = COLOR_ACCENT_SOFT if is_selected else COLOR_SURFACE_ALT
            border_col = COLOR_ACCENT if is_selected else COLOR_BORDER
            txt_color = COLOR_ACCENT if is_selected else COLOR_TEXT_PRIMARY

            dish_btn = ctk.CTkButton(
                self.list_frame,
                text=self.format_card_label(recipe),
                image=thumb_ctk,
                compound="left",
                anchor="w",
                height=76,
                corner_radius=12,
                border_width=2 if is_selected else 1,
                border_color=border_col,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=bg_color,
                text_color=txt_color,
                hover_color=COLOR_ACCENT_SOFT,
                command=lambda selected=recipe: self.select_recipe(selected),
            )
            dish_btn.pack(fill="x", padx=6, pady=4)
            self.card_buttons[recipe_id] = dish_btn

            if recipe.get("image") and (recipe_id, "raw") not in self.pil_cache:
                threading.Thread(
                    target=self.load_card_thumbnail_async,
                    args=(recipe, dish_btn),
                    daemon=True,
                ).start()

    def load_card_thumbnail_async(self, recipe, button_widget):
        url = recipe.get("image", "")
        if not url:
            return
        if self.download_and_cache_recipe_photo(recipe, url):
            thumb_pil = self.get_recipe_pil_image(recipe, CARD_THUMB_SIZE, radius=8)
            thumb_ctk = self.make_ctk_image(thumb_pil, CARD_THUMB_SIZE)
            self.after(0, lambda: self.update_widget_image_safe(button_widget, thumb_ctk))

    def update_widget_image_safe(self, widget, ctk_img):
        try:
            if widget.winfo_exists():
                widget.configure(image=ctk_img)
        except Exception:
            pass

    # -----------------------------------------------------------------------
    # Recipe Details Panel
    # -----------------------------------------------------------------------
    def show_empty_details(self):
        for child in self.details_frame.winfo_children():
            child.destroy()
        ctk.CTkLabel(
            self.details_frame,
            text="Select a recipe card on the left to inspect its ingredients and cooking steps.",
            wraplength=420, justify="left",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXT_MUTED,
        ).pack(padx=18, pady=30, anchor="w")

    def select_recipe(self, recipe):
        self.selected_recipe = recipe
        for child in self.details_frame.winfo_children():
            child.destroy()

        for rid, btn in self.card_buttons.items():
            if btn.winfo_exists():
                if rid == recipe.get("id"):
                    btn.configure(
                        fg_color=COLOR_ACCENT_SOFT,
                        border_color=COLOR_ACCENT,
                        border_width=2,
                        text_color=COLOR_ACCENT,
                    )
                else:
                    btn.configure(
                        fg_color=COLOR_SURFACE_ALT,
                        border_color=COLOR_BORDER,
                        border_width=1,
                        text_color=COLOR_TEXT_PRIMARY,
                    )

        # Centered, proportional Dish Photo Banner
        detail_pil = self.get_recipe_pil_image(recipe, DETAIL_BANNER_SIZE, radius=12)
        detail_ctk = self.make_ctk_image(detail_pil, DETAIL_BANNER_SIZE)

        self.detail_image_label = ctk.CTkLabel(
            self.details_frame, text="", image=detail_ctk
        )
        self.detail_image_label.pack(anchor="center", padx=12, pady=(10, 10))

        image_url = recipe.get("image", "")
        recipe_id = recipe.get("id", recipe["name"])
        if image_url and (recipe_id, "raw") not in self.pil_cache:
            threading.Thread(
                target=self.load_detail_image_async,
                args=(recipe, self.detail_image_label),
                daemon=True,
            ).start()

        # Dish Name & Clean Metadata Pill Row
        ctk.CTkLabel(
            self.details_frame,
            text=recipe["name"],
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            wraplength=480, justify="left",
        ).pack(anchor="w", padx=14, pady=(2, 4))

        meta_text = (
            f"{recipe.get('country', 'Global')}   •   "
            f"{recipe.get('category', 'Dish')}   •   "
            f"Prep: {recipe.get('prep_time', '35 mins')}   •   "
            f"{recipe.get('source', 'Built-in')}"
        )
        ctk.CTkLabel(
            self.details_frame,
            text=meta_text,
            wraplength=480,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_ACCENT,
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # Action Buttons with Proportional Food Thumbnails
        buttons = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        buttons.pack(fill="x", padx=12, pady=(0, 14))

        is_favourite = any(item.get("id") == recipe.get("id") for item in self.favourites)
        fav_pil = self.get_key_pil_image("cat_dessert", (26, 20), radius=4)
        fav_ctk = self.make_ctk_image(fav_pil, (26, 20))

        ctk.CTkButton(
            buttons,
            text="♥ Saved in Favourites" if is_favourite else "♡ Save to Favourites",
            image=fav_ctk,
            compound="left",
            height=38,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_ACCENT if is_favourite else COLOR_BORDER,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_ACCENT_SOFT if is_favourite else COLOR_SURFACE_ALT,
            text_color=COLOR_ACCENT if is_favourite else COLOR_TEXT_PRIMARY,
            hover_color=COLOR_ACCENT_SOFT,
            command=lambda r=recipe: self.toggle_favourite(r),
        ).pack(side="left", padx=(0, 8))

        vid_pil = self.get_key_pil_image("local_suya", (26, 20), radius=4)
        vid_ctk = self.make_ctk_image(vid_pil, (26, 20))
        ctk.CTkButton(
            buttons,
            text="▶ Watch Cooking Video",
            image=vid_ctk,
            compound="left",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=("#FFFFFF", "#FFFFFF"),
            command=lambda r=recipe: self.open_video(r),
        ).pack(side="left")

        # Ingredients Box
        ing_box = ctk.CTkFrame(
            self.details_frame,
            corner_radius=12,
            fg_color=COLOR_SURFACE_ALT,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        ing_box.pack(fill="x", padx=12, pady=(2, 14))

        ctk.CTkLabel(
            ing_box,
            text="Ingredients",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", padx=14, pady=(10, 6))

        for ingredient in recipe.get("ingredients", []):
            ctk.CTkLabel(
                ing_box,
                text=f"•  {ingredient}",
                anchor="w", justify="left", wraplength=450,
                font=ctk.CTkFont(size=13),
                text_color=COLOR_TEXT_PRIMARY,
            ).pack(anchor="w", padx=16, pady=2)
        ctk.CTkLabel(ing_box, text="", height=6).pack()

        # Cooking Steps
        ctk.CTkLabel(
            self.details_frame,
            text="Preparation Steps",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
        ).pack(anchor="w", padx=14, pady=(4, 6))

        instructions = recipe.get("instructions", "No instructions available.")
        if isinstance(instructions, list):
            steps = instructions
        else:
            steps = [part.strip() for part in instructions.replace("\r", "").split("\n") if part.strip()]
            if len(steps) <= 1:
                steps = [part.strip() for part in re.split(r"(?<=[.!?])\s+", instructions) if part.strip()]

        for index, step in enumerate(steps, start=1):
            step_card = ctk.CTkFrame(
                self.details_frame,
                corner_radius=10,
                fg_color=COLOR_SURFACE_ALT,
                border_width=1,
                border_color=COLOR_BORDER,
            )
            step_card.pack(fill="x", padx=12, pady=4)
            ctk.CTkLabel(
                step_card,
                text=f"{index}.  {step}",
                anchor="w", justify="left", wraplength=450,
                font=ctk.CTkFont(size=13),
                text_color=COLOR_TEXT_PRIMARY,
            ).pack(anchor="w", padx=14, pady=8)

        ctk.CTkLabel(
            self.details_frame,
            text="Note: Cooking times and seasoning quantities can be adjusted to taste.",
            wraplength=450, justify="left",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_MUTED,
        ).pack(anchor="w", padx=14, pady=(10, 16))

    def load_detail_image_async(self, recipe, label_widget):
        url = recipe.get("image", "")
        if self.download_and_cache_recipe_photo(recipe, url):
            detail_pil = self.get_recipe_pil_image(recipe, DETAIL_BANNER_SIZE, radius=12)
            detail_ctk = self.make_ctk_image(detail_pil, DETAIL_BANNER_SIZE)
            self.after(0, lambda: self.update_widget_image_safe(label_widget, detail_ctk))

    # -----------------------------------------------------------------------
    # Search, Filters & Favourites
    # -----------------------------------------------------------------------
    def set_status(self, message):
        self.status_label.configure(text=message)

    def quick_category_filter(self, query_val, label_name):
        self.showing_favourites = False
        if not query_val:
            self.show_all_recipes()
            return
        if query_val.lower() == "nigeria":
            self.show_nigerian_recipes()
            return
        self.highlight_nav("all")
        self.country_var.set("All countries")
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, query_val)
        self.set_status(f"Filtering {label_name}…")
        self.search_recipes()

    def on_country_selected(self, country):
        self.showing_favourites = False
        if country == "Nigeria":
            self.show_nigerian_recipes()
            return
        if country == "All countries":
            self.highlight_nav("all")
            self.apply_filters()
            return

        self.highlight_nav("all")
        matching = [r for r in self.recipes if r.get("country", "").casefold() == country.casefold()]
        if matching:
            self.apply_filters()
        else:
            self.set_status(f"Loading {country} dishes…")
            threading.Thread(target=self.fetch_country_recipes_worker, args=(country,), daemon=True).start()

    def fetch_country_recipes_worker(self, country):
        fetched = []
        try:
            resp = requests.get(f"{API_BASE}/filter.php", params={"a": country}, headers=HTTP_HEADERS, timeout=10)
            resp.raise_for_status()
            meals = (resp.json() or {}).get("meals") or []
            for item in meals[:6]:
                meal_id = clean_text(item.get("idMeal"))
                if meal_id:
                    detail_resp = requests.get(f"{API_BASE}/lookup.php", params={"i": meal_id}, headers=HTTP_HEADERS, timeout=8)
                    detail_meals = (detail_resp.json() or {}).get("meals") or []
                    if detail_meals:
                        recipe = api_meal_to_recipe(detail_meals[0])
                        if recipe.get("image"):
                            self.download_and_cache_recipe_photo(recipe, recipe["image"])
                        fetched.append(recipe)
        except Exception:
            pass

        def finish():
            if fetched:
                self.recipes = list(NIGERIAN_RECIPES) + fetched
                self.apply_filters()
                if self.visible_recipes:
                    self.select_recipe(self.visible_recipes[0])
                self.set_status(f"Showing {len(self.visible_recipes)} {country} recipe(s).")
            else:
                self.apply_filters()
                self.set_status(f"No online {country} recipes found right now.")

        self.after(0, finish)

    def load_random_spotlight(self):
        self.highlight_nav("random")
        self.set_status("Loading surprise recipe…")
        threading.Thread(target=self._random_spotlight_worker, daemon=True).start()

    def _random_spotlight_worker(self):
        chosen = None
        try:
            resp = requests.get(f"{API_BASE}/random.php", headers=HTTP_HEADERS, timeout=8)
            resp.raise_for_status()
            meals = (resp.json() or {}).get("meals") or []
            if meals:
                chosen = api_meal_to_recipe(meals[0])
                if chosen.get("image"):
                    self.download_and_cache_recipe_photo(chosen, chosen["image"])
        except Exception:
            import random
            chosen = random.choice(NIGERIAN_RECIPES)

        if chosen:
            def show():
                if all(r.get("id") != chosen.get("id") for r in self.recipes):
                    self.recipes.insert(0, chosen)
                self.country_var.set("All countries")
                self.apply_filters()
                self.select_recipe(chosen)
                self.set_status(f"Surprise Dish: {chosen['name']}")
            self.after(0, show)

    def search_recipes(self):
        query = self.search_entry.get().strip()
        self.showing_favourites = False
        local_matches = [
            recipe for recipe in NIGERIAN_RECIPES
            if not query or query.lower() in recipe["name"].lower()
            or query.lower() in recipe["country"].lower()
            or query.lower() in recipe["category"].lower()
            or any(query.lower() in ingredient.lower() for ingredient in recipe["ingredients"])
        ]
        self.set_status("Searching recipes…")
        threading.Thread(
            target=self.api_search_worker, args=(query, local_matches), daemon=True
        ).start()

    def api_search_worker(self, query, local_matches):
        api_recipes = []
        error_message = ""
        try:
            if query:
                response = requests.get(
                    f"{API_BASE}/search.php", params={"s": query}, headers=HTTP_HEADERS, timeout=10
                )
                response.raise_for_status()
                meals = (response.json() or {}).get("meals") or []
                api_recipes = [api_meal_to_recipe(meal) for meal in meals[:12]]
            else:
                response = requests.get(f"{API_BASE}/random.php", headers=HTTP_HEADERS, timeout=10)
                response.raise_for_status()
                meal = (response.json() or {}).get("meals") or []
                api_recipes = [api_meal_to_recipe(item) for item in meal]
        except (requests.RequestException, ValueError):
            error_message = "Offline mode • Showing built-in recipes."

        combined = []
        seen = set()
        for recipe in local_matches + api_recipes:
            key = recipe.get("name", "").casefold()
            if key and key not in seen:
                combined.append(recipe)
                seen.add(key)
        self.after(0, lambda: self.finish_search(combined, error_message, query))

    def finish_search(self, recipes, error_message, query):
        self.recipes = recipes
        self.country_var.set("All countries")
        self.apply_filters()
        if self.visible_recipes:
            self.select_recipe(self.visible_recipes[0])
        if error_message:
            self.set_status(error_message)
        elif query:
            self.set_status(f"Found {len(recipes)} recipe(s) for '{query}'.")
        else:
            self.set_status(f"Showing {len(recipes)} recipe(s).")

    def apply_filters(self):
        country = self.country_var.get()
        recipes = list(self.recipes)
        if country != "All countries":
            recipes = [
                recipe for recipe in recipes
                if recipe.get("country", "").casefold() == country.casefold()
            ]
        self.visible_recipes = recipes
        self.render_recipe_list(recipes)

    def show_all_recipes(self):
        self.showing_favourites = False
        self.highlight_nav("all")
        self.country_var.set("All countries")
        self.search_entry.delete(0, "end")
        combined = list(NIGERIAN_RECIPES)
        for hr in self.hero_recipes:
            if all(r.get("id") != hr.get("id") for r in combined):
                combined.append(hr)
        self.recipes = combined
        self.apply_filters()
        if self.visible_recipes:
            self.select_recipe(self.visible_recipes[0])
        self.set_status("Showing all featured recipes.")

    def show_nigerian_recipes(self):
        self.showing_favourites = False
        self.highlight_nav("nigeria")
        self.country_var.set("Nigeria")
        self.recipes = list(NIGERIAN_RECIPES)
        self.apply_filters()
        if self.visible_recipes:
            self.select_recipe(self.visible_recipes[0])
        self.set_status("Showing Nigerian classics.")

    def show_favourites(self):
        self.showing_favourites = True
        self.highlight_nav("fav")
        self.country_var.set("All countries")
        self.recipes = list(self.favourites)
        self.apply_filters()
        if self.visible_recipes:
            self.select_recipe(self.visible_recipes[0])
        else:
            self.show_empty_details()
        self.set_status(f"{len(self.favourites)} saved favourite(s).")

    def toggle_favourite(self, recipe):
        existing_index = next(
            (index for index, item in enumerate(self.favourites)
             if item.get("id") == recipe.get("id")), None
        )
        if existing_index is None:
            self.favourites.append(recipe)
            message = "Added to favourites."
        else:
            self.favourites.pop(existing_index)
            message = "Removed from favourites."
        try:
            save_favourites(self.favourites)
            self.set_status(message)
        except OSError as exc:
            self.set_status(f"Could not save favourites: {exc}")
        self.select_recipe(recipe)
        if self.showing_favourites:
            self.show_favourites()

    def open_video(self, recipe):
        video_url = recipe.get("video", "")
        if video_url and video_url.startswith("https://"):
            webbrowser.open(video_url)
        else:
            query = quote_plus(recipe.get("video_query") or f"how to cook {recipe['name']}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


if __name__ == "__main__":
    app = WorldRecipeApp()
    app.mainloop()

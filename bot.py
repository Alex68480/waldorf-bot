# -*- coding: utf-8 -*-
import requests
import os
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputMediaPhoto

STYLE_FIXE = "waldorf kindergarten, close up of natural wooden toys, autumn leaves, wool felt, beeswax candles, nature table, soft warm light, cozy atmosphere, no people, no humans, photorealistic, high quality, instagram square format, warm earth tones"

FONT_PATH = "Lato-Bold.ttf"

if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Bold.ttf"
    r = requests.get(font_url)
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)
def generate_image_with_text(prompt, texte_slide, index=0):
    full_prompt = STYLE_FIXE + " " + prompt + " seed" + str(index * 42)
    url = "https://image.pollinations.ai/prompt/" + full_prompt.replace(" ", "%20")
    print("Lade Bild " + str(index+1) + " von URL: " + url)
    response = requests.get(url, timeout=90)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((1080, 1080))
    draw = ImageDraw.Draw(img)
    bande_hauteur = 220
    bande_y = 1080 - bande_hauteur
    draw.rectangle([0, bande_y, 1080, 1080], fill=(30, 30, 30))
    try:
        font = ImageFont.truetype(FONT_PATH, 38)
        font_small = ImageFont.truetype(FONT_PATH, 28)
    except:
        font = ImageFont.load_default()
        font_small = font
    mots = texte_slide.split()
    lignes = []
    ligne = ""
    for mot in mots:
        if len(ligne + mot) < 32:
            ligne += mot + " "
        else:
            lignes.append(ligne.strip())
            ligne = mot + " "
    lignes.append(ligne.strip())
    y_texte = bande_y + 25
    for i, ligne in enumerate(lignes[:4]):
        f = font if i == 0 else font_small
        draw.text((40, y_texte), ligne, font=f, fill="white")
        y_texte += 50
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def generer_slides_pour_sujet(sujet):
    sujet_lower = sujet.lower()
    
    if "rhythmus" in sujet_lower or "rhyth" in sujet_lower:
        return [
            "Rhythmus gibt Kindern Sicherheit",
            "Feste Tagesablaeufe staerken das Vertrauen",
            "Morgenkreis, Spiel, Mahlzeit, Ruhe",
            "Rhythmus foerdert die Entwicklung",
            "So leben wir Rhythmus im Alltag"
        ]
    elif "spiel" in sujet_lower:
        return [
            "Spielen ist die Arbeit des Kindes",
            "Freies Spiel staerkt die Kreativitaet",
            "Naturmaterialien regen die Fantasie an",
            "Kinder lernen durch Spielen",
            "Unser Spielraum im Kindergarten"
        ]
    elif "natur" in sujet_lower:
        return [
            "Die Natur ist unser groesster Lehrmeister",
            "Draussen spielen staerkt den Koerper",
            "Jahreszeiten erleben und feiern",
            "Naturmaterialien im Alltag",
            "Kinder und Natur gehoeren zusammen"
        ]
    else:
        # Slides generiques mais avec le sujet inclus
        return [
            sujet + " im Waldorf Kindergarten",
            "Warum ist " + sujet + " wichtig?",
            "So setzen wir " + sujet + " um",
            "Was lernen die Kinder dabei?",
            "Unser Alltag mit " + sujet
        ]
# -*- coding: utf-8 -*-
import requests
import os
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputMediaPhoto

FONT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Lato-Bold.ttf")

VARIANTES = [
    "close up wooden toys warm light waldorf kindergarten",
    "autumn leaves nature table candles waldorf kindergarten",
    "wool felt basket natural materials waldorf kindergarten",
    "morning light window plants indoor waldorf kindergarten",
    "beeswax crayons paper art craft waldorf kindergarten"
]

def generate_image_with_text(prompt, texte_slide, index=0):
    variante = VARIANTES[index % len(VARIANTES)]
    full_prompt = variante + " " + prompt + " seed" + str(index * 137)
    url = "https://image.pollinations.ai/prompt/" + full_prompt.replace(" ", "%20")
    print("Lade Bild " + str(index+1) + " von URL: " + url)
    response = requests.get(url, timeout=90)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((1080, 1080))
    draw = ImageDraw.Draw(img)
    bande_hauteur = 220
    bande_y = 1080 - bande_hauteur
    draw.rectangle([0, bande_y, 1080, 1080], fill=(30, 30, 30))
    try:
        font = ImageFont.truetype(FONT_PATH, 38)
        font_small = ImageFont.truetype(FONT_PATH, 28)
    except:
        font = ImageFont.load_default()
        font_small = font
    mots = texte_slide.split()
    lignes = []
    ligne = ""
    for mot in mots:
        if len(ligne + mot) < 32:
            ligne += mot + " "
        else:
            lignes.append(ligne.strip())
            ligne = mot + " "
    lignes.append(ligne.strip())
    y_texte = bande_y + 25
    for i, ligne in enumerate(lignes[:4]):
        f = font if i == 0 else font_small
        draw.text((40, y_texte), ligne, font=f, fill="white")
        y_texte += 50
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def generer_slides_pour_sujet(sujet):
    sujet_lower = sujet.lower()
    if "rhythmus" in sujet_lower or "rhyth" in sujet_lower:
        return [
            "Rhythmus gibt Kindern Sicherheit",
            "Feste Tagesablaeufe staerken das Vertrauen",
            "Morgenkreis, Spiel, Mahlzeit, Ruhe",
            "Rhythmus foerdert die Entwicklung",
            "So leben wir Rhythmus im Alltag"
        ]
    elif "spiel" in sujet_lower:
        return [
            "Spielen ist die Arbeit des Kindes",
            "Freies Spiel staerkt die Kreativitaet",
            "Naturmaterialien regen die Fantasie an",
            "Kinder lernen durch Spielen",
            "Unser Spielraum im Kindergarten"
        ]
    elif "natur" in sujet_lower:
        return [
            "Die Natur ist unser groesster Lehrmeister",
            "Draussen spielen staerkt den Koerper",
            "Jahreszeiten erleben und feiern",
            "Naturmaterialien im Alltag",
            "Kinder und Natur gehoeren zusammen"
        ]
    else:
        return [
            sujet + " im Waldorf Kindergarten",
            "Warum ist " + sujet + " wichtig?",
            "So setzen wir " + sujet + " um",
            "Was lernen die Kinder dabei?",
            "Unser Alltag mit " + sujet
        ]

def handle_message(update, context):
    texte = update.message.text
    if "carousel" in texte.lower() or "karussell" in texte.lower():
        slides = generer_slides_pour_sujet(texte)
        total = len(slides)
        update.message.reply_text("Erstellung deines Karussells gestartet! ✨ (" + str(total) + " Bilder)")
        medias = []
        for i, slide_texte in enumerate(slides):
            try:
                update.message.reply_text("Bild " + str(i+1) + " von " + str(total) + " wird erstellt...")
                img = generate_image_with_text(texte, slide_texte, i)
                medias.append(InputMediaPhoto(media=img))
                time.sleep(5)
            except Exception as e:
                print("Fehler bei Bild " + str(i) + ": " + str(e))
        if medias:
            update.message.reply_media_group(media=medias)
            update.message.reply_text(
                "Dein Karussell ist fertig! 🎉\n\n"
                "#waldorfkindergarten #waldorfpadagogik #kindergarten "
                "#waldorferziehung #naturkind #padagogik #waldorf "
                "#fruhkindlichebildung #spielenundlernen #kindergartenalltag"
            )
        else:
            update.message.reply_text("Leider konnten keine Bilder erstellt werden. Bitte versuche es nochmal.")
    else:
        update.message.reply_text("Erstellung deines Instagram-Bildes... ✨")
        try:
            img = generate_image_with_text(texte, texte, 0)
            update.message.reply_photo(
                photo=img,
                caption="#waldorfkindergarten #waldorf #natur #kindergarten #waldorfpadagogik"
            )
        except Exception as e:
            update.message.reply_text("Fehler: " + str(e))



import os
token = os.environ.get("TOKEN")

updater = Updater(token)
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
print("Bot demarre !")
updater.idle()

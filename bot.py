# -*- coding: utf-8 -*-
import requests
import os
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram.ext import Updater, MessageHandler, Filters
from telegram import InputMediaPhoto
from openai import OpenAI

FONT_PATH = "Lato-Bold.ttf"

if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Bold.ttf"
    r = requests.get(font_url)
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generer_prompt_dalle(sujet, index):
    styles = [
        "morning circle time",
        "bread baking in kitchen",
        "watercolor painting activity",
        "wool and felt craft table",
        "seasonal nature table with plants"
    ]
    style = styles[index % len(styles)]
    prompt_gpt = """Tu es un expert en photographie et en pedagogie Waldorf Steiner.
    Cree un prompt en anglais pour DALL-E 3 qui genere une belle photo Instagram sur le theme: """ + sujet + """
    Le style visuel doit etre: """ + style + """
    
    Regles strictes:
    - Photo realiste et chaleureuse, pas de style cartoon
    - Couleurs douces: beige, terre, pastel, blanc casse
    - Elements naturels: laine, tissu, plantes, argile, cire, aquarelle
    - Lumiere naturelle douce venant d'une fenetre
    - Composition simple et epuree, pas surchargee
    - Ambiance calme et bienveillante
    - PAS d'enfants ni de personnes
    - Format carre Instagram
    - Retourne UNIQUEMENT le prompt en anglais, rien d'autre
    """
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_gpt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def generer_textes_gpt(sujet, nombre=5):
    prompt = """Du bist ein Experte fuer Waldorf Steiner Paedagogik. 
    Erstelle """ + str(nombre) + """ kurze inspirierende Texte auf Deutsch fuer einen Instagram Karussell Post ueber: """ + sujet + """
    
    Regeln:
    - Jeder Text maximal 8 Woerter
    - Warm, poetisch und paedagogisch wertvoll
    - Passend fuer einen Waldorf Kindergarten Instagram Account
    - Nur die Texte zurueckgeben, einen pro Zeile, ohne Nummerierung
    """
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    textes = response.choices[0].message.content.strip().split("\n")
    textes = [t.strip() for t in textes if t.strip()]
    return textes[:nombre]

def generer_hashtags_gpt(sujet):
    prompt = """Erstelle 10 relevante Instagram Hashtags auf Deutsch fuer einen Waldorf Kindergarten Post ueber: """ + sujet + """
    Nur die Hashtags zurueckgeben, alle in einer Zeile, mit # davor."""
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def generate_dalle_image(sujet, index=0):
    prompt = generer_prompt_dalle(sujet, index)
    print("DALL-E prompt: " + prompt)
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    img_response = requests.get(image_url, timeout=60)
    img = Image.open(BytesIO(img_response.content)).convert("RGB")
    img = img.resize((1080, 1080))
    return img

def generate_image_with_text(sujet, texte_slide, index=0):
    img = generate_dalle_image(sujet, index)
    draw = ImageDraw.Draw(img)
    bande_hauteur = 220
    bande_y = 1080 - bande_hauteur
    draw.rectangle([0, bande_y, 1080, 1080], fill=(45, 35, 25))
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
        draw.text((40, y_texte), ligne, font=f, fill=(245, 235, 220))
        y_texte += 50
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def generate_image_sans_text(sujet, index=0):
    img = generate_dalle_image(sujet, index)
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def handle_message(update, context):
    texte = update.message.text
    avec_texte = "ohne text" not in texte.lower()
    if "carousel" in texte.lower() or "karussell" in texte.lower():
        update.message.reply_text("GPT erstellt die Texte und Bildprompts... ✨")
        slides = generer_textes_gpt(texte)
        hashtags = generer_hashtags_gpt(texte)
        total = len(slides)
        update.message.reply_text("Erstellung von " + str(total) + " Bildern mit DALL-E 3 gestartet!")
        medias = []
        for i, slide_texte in enumerate(slides):
            try:
                update.message.reply_text("Bild " + str(i+1) + " von " + str(total) + " wird erstellt...")
                if avec_texte:
                    img = generate_image_with_text(texte, slide_texte, i)
                else:
                    img = generate_image_sans_text(texte, i)
                medias.append(InputMediaPhoto(media=img))
                time.sleep(2)
            except Exception as e:
                print("Fehler bei Bild " + str(i) + ": " + str(e))
                update.message.reply_text("Fehler bei Bild " + str(i+1) + ": " + str(e))
        if medias:
            update.message.reply_media_group(media=medias)
            update.message.reply_text("Dein Karussell ist fertig! 🎉\n\n" + hashtags)
        else:
            update.message.reply_text("Leider konnten keine Bilder erstellt werden.")
    else:
        update.message.reply_text("Erstellung deines Instagram-Bildes mit DALL-E 3... ✨")
        try:
            if avec_texte:
                img = generate_image_with_text(texte, texte, 0)
            else:
                img = generate_image_sans_text(texte, 0)
            hashtags = generer_hashtags_gpt(texte)
            update.message.reply_photo(photo=img, caption=hashtags)
        except Exception as e:
            update.message.reply_text("Fehler: " + str(e))

token = os.environ.get("TOKEN")

updater = Updater(token)
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
print("Bot demarre !")
updater.idle()

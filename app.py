# app.py — Backend for "The Cosmic Oracle" Astrology Chatbot
# Flask + API Ninjas Horoscope API Integration
# Adds believable wedding-year, lifeline (death year), and true-love predictions
# Uses crush/ex inputs for compatibility messages

from flask import Flask, request, jsonify, render_template
import requests
import random
from datetime import datetime

# -----------------------------
# Put your API Ninjas key here
# -----------------------------
import os
API_NINJAS_KEY = os.getenv("LGxSEyv5xLCzge0dacGJtA==sLDnyM5k1I1u2Fam")

# -----------------------------

app = Flask(__name__)

# -----------------------------
# Helper: fetch horoscope
# -----------------------------
def get_horoscope(sign_name: str, day: str):
    url = "https://api.api-ninjas.com/v1/horoscope"
    params = {"zodiac": sign_name.lower(), "day": day.lower()}
    headers = {"X-Api-Key": API_NINJAS_KEY}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"[DEBUG] API Error {resp.status_code}: {resp.text}")
            return None
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None

# -----------------------------
# Helper: compute predictions from DOB
# -----------------------------
def compute_life_predictions(dob_str: str):
    """
    Accepts dob as 'YYYY-MM-DD' (ISO). Returns a dict with:
      - birth_year (int or None)
      - probable_wedding_age (int)
      - probable_wedding_year (int or None)
      - probable_death_age (int)
      - probable_death_year (int or None)
      - suggested_true_love_age (int)
      - already_met_true_love (bool)  # randomly decided
    """
    now = datetime.now().year
    birth_year = None
    try:
        if dob_str:
            parts = dob_str.split('-')
            if len(parts) >= 1 and parts[0].isdigit():
                birth_year = int(parts[0])
    except Exception:
        birth_year = None

    # Wedding age: believable range 28-36
    wedding_age = random.randint(28, 36)

    # Death age (lifeline): more conservative but random 45-75 (as requested)
    death_age = random.randint(45, 75)

    # True-love suggested age range: often younger - between 20 and 35
    true_love_age = random.randint(20, 28)

    # Decide "already met" randomly (25% chance already met if older than true_love_age)
    already_met = False
    if birth_year:
        current_age = now - birth_year
        # if user older than true_love_age, slightly higher chance of already met
        if current_age >= true_love_age:
            already_met = random.random() < 0.45  # 45% chance
        else:
            already_met = random.random() < 0.12  # 12% chance
    else:
        # no dob provided, random small chance
        already_met = random.random() < 0.2

    # compute years if birth_year known
    wedding_year = (birth_year + wedding_age) if birth_year else None
    death_year = (birth_year + death_age) if birth_year else None

    return {
        "birth_year": birth_year,
        "wedding_age": wedding_age,
        "wedding_year": wedding_year,
        "death_age": death_age,
        "death_year": death_year,
        "true_love_age": true_love_age,
        "already_met": already_met
    }

# -----------------------------
# Compatibility / relationship fun text
# -----------------------------
def love_compatibility_response(crush: str, ex: str):
    """Return a short, believable compatibility message (string or None)."""
    crush = (crush or "").strip()
    ex = (ex or "").strip()

    if crush and not ex:
        chance = random.randint(1, 100)
        if chance > 75:
            return f"💖 The stars smile on you and {crush.title()} — a strong spark is present; nurture it."
        elif chance > 45:
            return f"💞 You and {crush.title()} have gentle chemistry — take it slow and see how it grows."
        else:
            return f"💔 The planets are a bit cloudy for you and {crush.title()} right now; timing may improve later."

    if ex and not crush:
        ex_list = [n.strip() for n in ex.split(",") if n.strip()]
        chosen = random.choice(ex_list) if ex_list else None
        chance = random.randint(1, 100)
        if chosen:
            if chance > 60:
                return f"🔮 The past with {chosen.title()} still whispers — lessons remain, but reconciliation is possible."
            else:
                return f"🌘 The stars advise closure regarding {chosen.title()} — healing comes when you let go."
        else:
            return None

    if crush and ex:
        # both present; pick a dramatic blended message
        return f"❤️‍🔥 Your heart is pulled between past stars and new constellations — {crush.title()} could be a fresh chapter."

    return None

# -----------------------------
# Build the final formatted text
# -----------------------------
def format_horoscope_response(data: dict, sign: str, day: str, dob: str, crush: str, ex: str):
    # If API failed, return friendly error
    if not data or "horoscope" not in data:
        return {
            "text": (
                "🌌 **Cosmic Signal Lost!** I couldn’t retrieve the horoscope.\n"
                "Please check your API key or try again later."
            ),
            "style": "error"
        }

    description = data.get("horoscope", "The stars are silent today.")
    colors = ["Red", "Blue", "Pink", "Yellow", "White", "Black", "Green"]
    color = random.choice(colors)
    lucky_num = str(random.randint(0, 9))

    # mood from an internal list
    moods = ["Radiant", "Reflective", "Adventurous", "Calm", "Hopeful", "Balanced", "Playful"]
    mood = random.choice(moods)

    # life predictions
    preds = compute_life_predictions(dob)

    # prepare human-friendly lines for predictions
    wedding_line = "Unknown"
    if preds["wedding_year"]:
        wedding_line = f"Likely around age {preds['wedding_age']} → ≈ {preds['wedding_year']}"
    else:
        # if no dob, compute approximate year from current year
        approx_year = datetime.now().year + (preds["wedding_age"] - 25)
        wedding_line = f"Likely around age {preds['wedding_age']} → ≈ {approx_year}"

    death_line = "Unknown"
    if preds["death_year"]:
        death_line = f"Approximate lifeline to age {preds['death_age']} → {preds['death_year']}"
    else:
        death_line = f"Approximate lifeline to age {preds['death_age']}"

    true_love_line = ""
    if preds["already_met"]:
        true_love_line = f"✨ The stars hint you may have already crossed paths with your true love (around age {preds['true_love_age']})."
    else:
        true_love_line = f"✨ Your true love may arrive around age {preds['true_love_age']}."

    # love compatibility based on inputs
    love_msg = love_compatibility_response(crush, ex)

    # Compose final message (with \n for line breaks)
    formatted_text = (
        f"✨ **Behold, {sign.title()}!** ✨\n\n"
        f"Your cosmic forecast for **{day.title()}** is revealed:\n\n"
        f"***The Oracle Speaks:***\n"
        f"> *{description}*\n\n"
        f"**Lucky Number:** {lucky_num}\n"
        f"**Color Aura:** {color}\n"
        f"**Mood:** {mood}\n\n"
        f"🔮 **Cosmic Predictions:**\n"
        f"💍 Wedding: {wedding_line}\n"
        f"💘 True Love: {true_love_line}\n"
        f"🕯️ Lifeline: {death_line}\n"
    )

    if love_msg:
        formatted_text += f"\n💘 **Compatibility Note:**\n{love_msg}\n"

    formatted_text += "\nWalk your path with light — the stars are watching over you 🌠"

    return {"text": formatted_text, "style": "success"}

# -----------------------------
# Flask routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask_oracle", methods=["POST"])
def ask_oracle():
    payload = request.get_json() or {}
    sign = payload.get("sign", "aries")
    day = payload.get("day", "today")
    name = payload.get("name", "")
    dob = payload.get("dob", "")
    crush = payload.get("crush", "").strip()
    ex = payload.get("ex", "").strip()

    print(f"[INFO] Horoscope requested for {sign.title()} ({day}) | name={name} dob={dob} crush={crush} ex={ex}")

    horoscope_data = get_horoscope(sign, day)
    formatted = format_horoscope_response(horoscope_data, sign, day, dob, crush, ex)
    return jsonify(formatted)

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

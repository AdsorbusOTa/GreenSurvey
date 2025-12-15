import json
from pathlib import Path
from PIL import Image
from typing import List, Dict, Any
import streamlit as st

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone

# ============================================================
# DESIGN-FARBEN (RGB -> CSS)
# ============================================================
DARK_GREEN = "rgb(0, 85, 56)"       # Hintergrund & Titel-Farbe
LIGHT_GREEN = "rgb(138, 189, 36)"   # Schriftfarbe & Titelblock-Hintergrund

# ============================================================
# GRUNDEINSTELLUNGEN DER APP
# ============================================================
ICON_PATH = Path(__file__).parent / "sunflower.png"
page_icon = "🌻"
if ICON_PATH.exists():
    page_icon = Image.open(ICON_PATH) # <- Bilddatei im selben Ordner (Sonnenblume)

st.set_page_config(
    page_title="Anonyme Mitgliederumfrage – Bündnis 90/Die Grünen",
    page_icon=page_icon,  
    layout="centered"
)

# ------------------------------------------------------------
# Hilfsfunktionen für die persistent gespeicherte Avatar-Liste
# ------------------------------------------------------------

AVATAR_FILE = Path("used_avatars.json")


def load_used_avatars() -> List[str]:
    """
    Lädt die Liste bereits verwendeter Avatare (Emojis) aus einer JSON-Datei.

    WICHTIG:
    - Hier wird nur eine kleine Emoji-Liste gespeichert, KEINE Antworten.
    - Falls die Datei nicht existiert oder fehlerhaft ist, wird eine leere Liste zurückgegeben.
    """
    if not AVATAR_FILE.exists():
        return []

    try:
        with AVATAR_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(x) for x in data]
        return []
    except Exception:
        return []


def save_used_avatars(used_avatars: List[str]) -> None:
    """
    Speichert die Liste bereits verwendeter Avatare (Emojis) in eine JSON-Datei.

    WICHTIG:
    - Nur Emoji-Zeichen werden gespeichert.
    - Keine Inhalte der Umfrage, keine personenbezogenen Daten.
    """
    try:
        with AVATAR_FILE.open("w", encoding="utf-8") as f:
            json.dump(used_avatars, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(
            f"Die Avatar-Liste konnte nicht dauerhaft gespeichert werden "
            f"(technischer Hinweis: {e})."
        )

def send_results_email(*, subject: str, body_text: str) -> None:
    """
    Sendet eine E-Mail via SMTP über Streamlit Secrets.
    Credentials werden ausschließlich über st.secrets bezogen (keine Hardcodes).
    """
    host = st.secrets.get("SMTP_HOST")
    port = int(st.secrets.get("SMTP_PORT", 465))
    user = st.secrets.get("SMTP_USER")
    pw = st.secrets.get("SMTP_PASS")
    mail_to = st.secrets.get("MAIL_TO")
    mail_from = st.secrets.get("MAIL_FROM", user)

    missing = [k for k in ["SMTP_HOST", "SMTP_USER", "SMTP_PASS", "MAIL_TO"] if st.secrets.get(k) is None]
    if missing:
        raise RuntimeError(f"Fehlende secrets: {', '.join(missing)}")

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user, pw)
        server.send_message(msg)

# ------------------------------------------------------------
# Definition der Avatar-Emojis
# ------------------------------------------------------------
ALL_AVATAR_EMOJIS: List[Dict[str, str]] = [
    {"emoji": "🦇", "name": "Fledermaus"},
    {"emoji": "🦉", "name": "Eule"},
    {"emoji": "🦅", "name": "Adler"},
    {"emoji": "🦆", "name": "Ente"},
    {"emoji": "🦢", "name": "Schwan"},
    {"emoji": "🦜", "name": "Papagei"},
    {"emoji": "🦚", "name": "Pfau"},
    {"emoji": "🦩", "name": "Flamingo"},
    {"emoji": "🕊️", "name": "Taube"},
    {"emoji": "🦤", "name": "Dodo"},
    {"emoji": "🦝", "name": "Waschbär"},
    {"emoji": "🦨", "name": "Stinktier"},
    {"emoji": "🦡", "name": "Dachs"},
    {"emoji": "🦫", "name": "Biber"},
    {"emoji": "🦦", "name": "Otter"},
    {"emoji": "🦥", "name": "Faultier"},
    {"emoji": "🦘", "name": "Känguru"},
    {"emoji": "🦙", "name": "Lama"},
    {"emoji": "🦒", "name": "Giraffe"},
    {"emoji": "🦬", "name": "Bison"},
    {"emoji": "🦏", "name": "Nashorn"},
    {"emoji": "🦛", "name": "Nilpferd"},
    {"emoji": "🐆", "name": "Leopard"},
    {"emoji": "🐅", "name": "Tiger"},
    {"emoji": "🐊", "name": "Krokodil"},
    {"emoji": "🦈", "name": "Hai"},
    {"emoji": "🐋", "name": "Wal"},
    {"emoji": "🐬", "name": "Delfin"},
    {"emoji": "🦭", "name": "Robbe"},
    {"emoji": "🦎", "name": "Eidechse"},
    {"emoji": "🐢", "name": "Schildkröte"},
    {"emoji": "🦕", "name": "Sauropode"},
    {"emoji": "🦖", "name": "T-Rex"},
    {"emoji": "🦟", "name": "Mücke"},
    {"emoji": "🕷️", "name": "Spinne"},
    {"emoji": "🦂", "name": "Skorpion"},
    {"emoji": "🐙", "name": "Oktopus"},
    {"emoji": "🦑", "name": "Kalmar"},
    {"emoji": "🪼", "name": "Qualle"},
]

# ------------------------------------------------------------
# Custom CSS: Dunkelgrüner Hintergrund, hellgrüne Schrift,
# Titelblock hellgrün mit dunkelgrüner Überschrift,
# größere Emoji-Icons
# ------------------------------------------------------------
def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
        /* ================= GOOGLE FONTS ================= */
        @import url('https://fonts.googleapis.com/css2?family=PT+Sans:ital,wght@0,400;0,700;1,400&family=Oswald:ital,wght@1,600;1,700&display=swap');

        /* App-Hintergrund */
        .stApp {{
            background: {DARK_GREEN};
        }}

        /* Standard-Textfarbe (Absätze, Hinweise, Labels etc.) */
        html, body, [class*="css"] {{
            font-family: "PT Sans", Arial, sans-serif;
            color: {LIGHT_GREEN} !important;
        }}

        /* Streamlit Markdown/Text */
        .stMarkdown, .stMarkdown p, .stMarkdown li {{
            color: {LIGHT_GREEN} !important;
        }}

        /* Captions / Help-Text */
        .stCaption, small {{
            color: {LIGHT_GREEN} !important;
            opacity: 0.9;
        }}

        /* Expander Header */
        div[data-testid="stExpander"] > details > summary {{
            color: {LIGHT_GREEN} !important;
        }}

        /* Inputs/Selectbox Labels */
        label, .stTextInput label, .stSelectbox label, .stMultiSelect label {{
            color: {LIGHT_GREEN} !important;
        }}

        /* Karten/Container (leicht transparent, damit es "modern" wirkt) */
        .survey-card {{
            background: rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            border: 1px solid rgba(138, 189, 36, 0.35);
            box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        }}

        /* Titel-Block: hellgrün, Text dunkelgrün */
        .title-block {{
            background: {LIGHT_GREEN};
            border-radius: 18px;
            padding: 1.1rem 1.3rem;
            border: 1px solid rgba(0,0,0,0.08);
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
            margin-bottom: 1rem;
        }}
        .title-block h1 {{
            margin: 0;
            padding: 0;
            font-size: 2.25rem;
            line-height: 1.1;
            color: {DARK_GREEN} !important;
            /*GrueneType fallback*/
            font-family: "Oswald", "Arial Narrow", Arial, sans-serif;
            font-style: italic;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}
        .title-block h2 {{
            margin: 0.35rem 0 0 0;
            padding: 0;
            font-size: 1.1rem;
            line-height: 1.2;
            color: {DARK_GREEN} !important;
            font-weight: 600;
            opacity: 0.95;
        }}

        /* Trennlinie */
        hr {{
            border: none;
            border-top: 1px solid rgba(138, 189, 36, 0.35);
            margin: 1.0rem 0;
        }}

        /* Buttons */
        button[kind="primary"] {{
            background-color: {LIGHT_GREEN} !important;
            color: {DARK_GREEN} !important;
            border: 1px solid rgba(0,0,0,0.08) !important;
            font-weight: 700 !important;
        }}

        /* Emoji-Übersicht (größer) */
        .avatar-box {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 0.6rem 0 0.2rem 0;
        }}

        /* Größere Icons */
        .avatar-pill {{
            font-size: 2.35rem;   /* <- größer */
            line-height: 1;
            border-radius: 999px;
            padding: 0.35rem 0.85rem;
            border: 1px solid rgba(138, 189, 36, 0.55);
            cursor: default;
            user-select: none;
        }}
        .avatar-pill.used {{
            opacity: 0.30;
        }}
        .avatar-pill.free {{
            background: rgba(138, 189, 36, 0.14);
        }}
        .avatar-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(72px, 1fr));
            gap: 0.9rem;
            margin-top: 0.8rem;
        }}

        .avatar-tile {{
            font-size: 3rem;
            line-height: 1;
            text-align: center;
            padding: 0.6rem 0.2rem;
            border-radius: 16px;
            cursor: pointer;
            border: 2px solid transparent;
            background: rgba(138, 189, 36, 0.14);
            transition: all 0.15s ease-in-out;
        }}

        .avatar-tile:hover {{
            border-color: rgb(138, 189, 36);
            transform: scale(1.05);
        }}

        .avatar-tile.used {{
            opacity: 0.25;
            cursor: not-allowed;
        }}

        .avatar-tile.selected {{
            border-color: rgb(138, 189, 36);
            box-shadow: 0 0 0 3px rgba(138, 189, 36, 0.35);
            background: rgba(138, 189, 36, 0.25);
        }}

        /* Avatar-Kachel (Emoji + Name) */
        .avatar-card {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.75rem 0.9rem;
            border-radius: 16px;
            border: none;
            background: rgba(138, 189, 36, 0.12);
        }}

        .avatar-card.used {{
            opacity: 0.30;
        }}

        .avatar-card.selected {{
            box-shadow: 0 0 0 3px rgba(138, 189, 36, 0.35);
            background: rgba(138, 189, 36, 0.22);
        }}

        .avatar-emoji {{
            font-size: 2.6rem;
            line-height: 1;
        }}

        .avatar-name {{
            font-size: 1.05rem;
            font-weight: 700;
            color: rgb(138, 189, 36);
        }}



        /* Fußnote */
        .footnote {{
            font-size: 0.85rem;
            color: {LIGHT_GREEN} !important;
            opacity: 0.9;
            margin-top: 0.8rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


inject_custom_css()

# ============================================================
# TITEL & EINLEITUNG (mit Titelblock)
# ============================================================

st.markdown(
    f"""
    <div class="title-block">
        <h1>🌻 Anonyme Mitgliederumfrage</h1>
        <h2>Ortsverband – Bündnis 90/Die Grünen</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="survey-card">
    Diese Seite ist ein <b>Entwurf</b>, um die geplante Umfrage zu zeigen:

    - Teilnahme ist <b>anonym</b><br>
    - Jede Person wählt einen <b>Tier-Avatar (nur Emoji)</b><br>
    - Es werden <b>keine Antworten gespeichert</b>, nur die Avatar-Belegung<br>
    - Später sollen Antworten als E-Mail verschickt und ausgewertet werden
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# AVATAR-BEREICH (Emojis + globale Memory-Liste)
# ============================================================

used_avatars_global: List[str] = load_used_avatars()

if "chosen_avatar" not in st.session_state:
    st.session_state.chosen_avatar = None

if "reserved_avatar" not in st.session_state:
    st.session_state.reserved_avatar = None

st.markdown("### 🐾 Dein anonymes Tier-Emoji")
st.markdown("Klicke auf ein Emoji, um es auszuwählen.")

cols = st.columns(4)

for i, av in enumerate(ALL_AVATAR_EMOJIS):
    col = cols[i % 4]
    emoji = av["emoji"]
    name = av["name"]

    is_used = emoji in used_avatars_global
    is_selected = emoji == st.session_state.chosen_avatar

    classes = ["avatar-card"]
    if is_used:
        classes.append("used")
    if is_selected:
        classes.append("selected")

    with col:
        st.markdown(
            f"""
            <div class="{' '.join(classes)}">
                <div class="avatar-emoji">{emoji}</div>
                <div class="avatar-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Auswahl-Button separat (Streamlit-Buttons sind zuverlässig klickbar)
        if st.button("Auswählen", key=f"pick_{emoji}", disabled=is_used):
            # nur lokal auswählen – noch NICHT global reservieren
            st.session_state.chosen_avatar = emoji
            st.rerun()

if st.session_state.chosen_avatar:
    st.success(f"Dein Avatar ist: {st.session_state.chosen_avatar}")


# ============================================================
# FRAGENBLOCK – nur Frontend, keine Speicherung
# ============================================================

st.markdown("### 📋 Fragen an Dich")

st.markdown(
    """
    Unten siehst Du die geplanten Fragen.  
    Für jede Frage gibt es **Auswahlmöglichkeiten** und ein **Freitextfeld**.
    """
)

def question_checkboxes(
    key_prefix: str,
    title: str,
    options: List[str],
    max_choices: int | None = None
) -> Dict[str, Any]:
    """
    Zeigt echte Checkboxen (eine pro Option) + Freitextfeld.
    Optional kann die maximale Anzahl an Auswahloptionen begrenzt werden.

    UX:
    - Wenn max_choices erreicht ist, werden die übrigen (noch nicht angehakten)
      Checkboxen automatisch deaktiviert.
    """
    st.markdown(f"#### {title}")

    if max_choices is not None:
        st.caption(f"Bitte höchstens **{max_choices}** Antworten auswählen.")

    # Aktuellen Zustand zählen
    checked_count = 0
    for opt in options:
        if st.session_state.get(f"{key_prefix}_cb_{opt}", False):
            checked_count += 1

    selected: List[str] = []

    # Checkboxen rendern
    for opt in options:
        state_key = f"{key_prefix}_cb_{opt}"

        # Deaktivieren, wenn Limit erreicht und diese Box nicht schon aktiv ist
        disabled = False
        if max_choices is not None:
            already_checked = st.session_state.get(state_key, False)
            if (checked_count >= max_choices) and (not already_checked):
                disabled = True

        value = st.checkbox(opt, key=state_key, disabled=disabled)
        if value:
            selected.append(opt)

    # Freitext
    other = st.text_input(
        label="Sonstiges / eigene Antwort:",
        key=f"{key_prefix}_other"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    return {"selected": selected, "other": other}



antworten: Dict[str, Any] = {}

antworten["q1_motive"] = question_checkboxes(
    key_prefix="q1",
    title="1. Was sind Deine Motive dabei zu sein?",
    options=[
        "Politische Veränderung bewirken",
        "Klima- und Umweltschutz",
        "Soziale Gerechtigkeit",
        "Engagement vor Ort",
        "Mitgestaltung kommunaler Politik",
        "Vernetzung & Gemeinschaft"
    ],
    max_choices=3
)

antworten["q2_erwartung"] = question_checkboxes(
    key_prefix="q2",
    title="2. Was ist Deine Erwartung an den Ortsverband?",
    options=[
        "Transparente politische Arbeit",
        "Mehr Austausch untereinander",
        "Konkrete Projektarbeit",
        "Unterstützung im Engagement",
        "Weiterbildung / politische Bildung"
    ],
    max_choices=3
)

antworten["q3_themen"] = question_checkboxes(
    key_prefix="q3",
    title="3. Welche Themen bewegen Dich besonders?",
    options=[
        "Energie & Klima",
        "Verkehr & Mobilität",
        "Soziales & Integration",
        "Naturschutz & Biodiversität",
        "Digitalisierung",
        "Bildung",
        "Landwirtschaft",
        "Gesundheit"
    ],
    max_choices=4
)

antworten["q4_aendern"] = question_checkboxes(
    key_prefix="q4",
    title="4. Was würdest Du im Ortsverband anders machen?",
    options=[
        "Offener kommunizieren",
        "Entscheidungswege verkürzen",
        "Mehr Aktionen & Veranstaltungen",
        "Bessere Einbindung neuer Mitglieder"
    ],
    max_choices=3
)

antworten["q5_hemmnisse"] = question_checkboxes(
    key_prefix="q5",
    title="5. Was hält Dich ab, Dich (noch) mehr einzubringen?",
    options=[
        "Zeitmangel",
        "Unklare Rollen / Aufgaben",
        "Zu wenig Informationen",
        "Hemmschwelle in der Gruppe",
        "Strukturen sind unübersichtlich"
    ],
    max_choices=3
)

antworten["avatar"] = st.session_state.get("chosen_avatar", None)

# ============================================================
# VORSCHAU DER ANTWORTEN (nur lokal, keine Speicherung)
# ============================================================

st.markdown("### 🔍 Vorschau (nur zur Präsentation)")

st.markdown(
    """
    Diese Daten werden derzeit **nirgendwo gespeichert** – sie sind nur in
    dieser Session sichtbar.
    """
)

if st.button("Antworten als Beispiel anzeigen", type="primary"):
    st.json(antworten)

st.markdown(
    """
    <div class="footnote">
    In der endgültigen Version wird hier ein Button ergänzt, der die Antworten
    anonym als E-Mail an den Ortsverband sendet und ggf. einen PDF-Export erlaubt.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### ✉️ Ergebnisse per E-Mail senden")

send_opt_in = st.checkbox(
    "Ich möchte meine Ergebnisse anonym per E-Mail an den Ortsverband senden.",
    value=False
)

st.caption("Hinweis: Es werden keine Antworten gespeichert. Beim Versand werden die Antworten nur per E-Mail übertragen.")

# Für klare Logik: Versand nur erlauben, wenn ein Avatar reserviert ist (falls Du reservieren/auswählen getrennt hast).
# Wenn Du noch KEIN reserved_avatar verwendest, ersetze reserved_avatar durch chosen_avatar.
avatar_for_sending = st.session_state.get("reserved_avatar") or st.session_state.get("chosen_avatar")

can_send = send_opt_in and (avatar_for_sending is not None)

if st.button("📨 Ergebnisse jetzt senden", type="primary", disabled=not can_send):
    try:
        # Payload: gut maschinenlesbar (JSON), plus ein paar Metadaten
        payload = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "avatar": avatar_for_sending,
            "answers": antworten,
        }

        subject = "Neue Umfrageantwort (anonym)"
        body = json.dumps(payload, ensure_ascii=False, indent=2)

        send_results_email(subject=subject, body_text=body)

        st.success("Vielen Dank! Die Ergebnisse wurden per E-Mail versendet.")
    except Exception as e:
        st.error(f"E-Mail konnte nicht versendet werden: {e}")
        st.info("Prüfe SMTP-Daten in .streamlit/secrets.toml oder in den Streamlit-Cloud-Secrets.")

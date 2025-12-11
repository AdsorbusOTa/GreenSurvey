import json
from pathlib import Path
from typing import List, Dict, Any

import streamlit as st

# ============================================================
# GRUNDEINSTELLUNGEN DER APP
# ============================================================

# Seiten-Layout & Titel konfigurieren
st.set_page_config(
    page_title="Anonyme Mitgliederumfrage – Bündnis 90/Die Grünen",
    page_icon="🌿",
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
        # Wenn irgendetwas schiefgeht, lieber mit einer leeren Liste arbeiten,
        # statt die App abstürzen zu lassen.
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
        # Falls das Schreiben auf dem Server nicht erlaubt ist,
        # zeigen wir eine dezente Warnung – die App funktioniert trotzdem weiter.
        st.warning(
            f"Die Avatar-Liste konnte nicht dauerhaft gespeichert werden "
            f"(technischer Hinweis: {e})."
        )


# ------------------------------------------------------------
# Definition der Avatar-Emojis
# Statt Tiernamen verwenden wir nur Emojis in der Oberfläche.
# ------------------------------------------------------------

ALL_AVATAR_EMOJIS: List[str] = [
    "🦇", "🦉", "🦅", "🦆", "🦢",
    "🦜", "🦚", "🦩", "🕊️", "🦤",
    "🦝", "🦨", "🦡", "🦫", "🦦",
    "🦥", "🦘", "🦙", "🦒", "🦬",
    "🦏", "🦛", "🐆", "🐅", "🐊",
    "🦈", "🐋", "🐬", "🦭", "🦈",
    "🦎", "🐢", "🦕", "🦖", "🦟",
    "🕷️", "🦂", "🐙", "🦑", "🪼"
]

# Kleine Bereinigung, falls versehentlich doppelte Emojis eingetragen wurden
ALL_AVATAR_EMOJIS = list(dict.fromkeys(ALL_AVATAR_EMOJIS))


# ------------------------------------------------------------
# Custom CSS für modernes "grünes" Design
# ------------------------------------------------------------

def inject_custom_css() -> None:
    """
    Fügt ein schlichtes, modernes, grün-betontes Design via CSS ein.
    """
    st.markdown(
        """
        <style>
        /* Grundschrift & Hintergrund */
        html, body, [class*="css"]  {
            font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Überschriften */
        h1, h2, h3 {
            color: #0B7A3B; /* kräftiges Grün */
        }

        /* Container-Card für Inhalte */
        .survey-card {
            background-color: #f6fff9;
            border-radius: 16px;
            padding: 1.3rem 1.5rem;
            border: 1px solid #ccead8;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }

        /* Avatar-Box */
        .avatar-box {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-bottom: 0.7rem;
        }

        .avatar-pill {
            font-size: 1.6rem;
            border-radius: 999px;
            padding: 0.2rem 0.8rem;
            border: 1px solid #ccead8;
            cursor: default;
        }

        .avatar-pill.used {
            opacity: 0.35;
        }

        .avatar-pill.free {
            background: #e3f6ea;
        }

        /* Buttons akzentuieren */
        button[kind="primary"] {
            background-color: #0B7A3B !important;
            color: white !important;
        }

        /* Kleine Fußnote */
        .footnote {
            font-size: 0.8rem;
            color: #666666;
            margin-top: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


inject_custom_css()

# ============================================================
# TITEL & EINLEITUNG
# ============================================================

st.title("🌿 Anonyme Mitgliederumfrage")
st.subheader("Ortsverband – Bündnis 90/Die Grünen")

st.markdown(
    """
    Diese Seite ist ein **Entwurf**, um die geplante Umfrage zu zeigen:

    - Teilnahme ist **anonym**  
    - Jede Person wählt einen **Tier-Avatar (nur Emoji)**  
    - Es werden **keine Antworten gespeichert**, nur die Avatar-Belegung  
    - Später sollen Antworten als E-Mail verschickt und ausgewertet werden

    ---
    """
)

# ============================================================
# AVATAR-BEREICH (Emojis + globale Memory-Liste)
# ============================================================

# Bereits verwendete Emojis aus Datei laden (global)
used_avatars_global: List[str] = load_used_avatars()

# Streamlit-Session-Cache für aktuell gewählten Avatar
if "chosen_avatar" not in st.session_state:
    st.session_state.chosen_avatar = None

st.markdown("### 🐾 Dein anonymes Tier-Emoji")

st.markdown(
    """
    Wähle ein Emoji, das Dich heute symbolisiert.  
    **Ein Emoji soll möglichst nur einmal vergeben werden.**
    """
)

# Liste freier Emojis für die Auswahl
available_emojis = [e for e in ALL_AVATAR_EMOJIS if e not in used_avatars_global]

if not available_emojis:
    st.warning(
        "Aktuell sind alle Tier-Emojis vergeben. "
        "Für die endgültige Version können wir die Liste erweitern oder "
        "ein Zurücksetzen der Avatare ermöglichen."
    )
else:
    # Auswahl des Avatars
    selected_avatar = st.selectbox(
        "Wähle Deinen Avatar (nur Emoji – keine Namen):",
        options=["(bitte auswählen)"] + available_emojis,
        index=0,
        help="Das Emoji wird als anonymer Platzhalter in der Auswertung verwendet."
    )

    # Button zum "Reservieren"
    if st.button("Avatar auswählen / reservieren"):
        if selected_avatar == "(bitte auswählen)":
            st.error("Bitte zuerst ein Emoji auswählen.")
        else:
            st.session_state.chosen_avatar = selected_avatar

            # In globale Liste aufnehmen, falls noch nicht enthalten
            if selected_avatar not in used_avatars_global:
                used_avatars_global.append(selected_avatar)
                save_used_avatars(used_avatars_global)

            st.success(f"Dein Avatar ist: {selected_avatar}")

# Kleine Übersicht, welche Emojis bereits vergeben sind (ohne Namen)
with st.expander("Vergebene & freie Emojis anzeigen (nur zur Demo)"):
    st.markdown("**Legende:** hellgrün = frei, transparent = bereits vergeben")
    st.markdown('<div class="avatar-box">', unsafe_allow_html=True)
    for emoji in ALL_AVATAR_EMOJIS:
        css_class = "avatar-pill used" if emoji in used_avatars_global else "avatar-pill free"
        st.markdown(f'<span class="{css_class}">{emoji}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FRAGENBLOCK – nur Frontend, keine Speicherung
# ============================================================

st.markdown("### 📋 Fragen an Dich")

st.markdown(
    """
    Unten siehst Du die geplanten Fragen.  
    Für jede Frage gibt es **Auswahlmöglichkeiten (Checkboxen)** und ein **Freitextfeld**.
    
    In der späteren Version werden die Antworten:
    - per E-Mail anonym an den Ortsverband gesendet
    - automatisch ausgewertet (Diagramme etc.)
    """
)


def question_multiselect(
    key_prefix: str,
    title: str,
    options: List[str],
    max_choices: int | None = None
) -> Dict[str, Any]:
    """
    Zeigt eine Frage mit Mehrfachauswahl (Checkbox-Stil via multiselect) und
    einem zusätzlichen Freitextfeld "Sonstiges".

    Parameter:
    - key_prefix : eindeutiger Präfix für Streamlit-Schlüssel
    - title      : Frage-Text
    - options    : Liste der Antwortoptionen als Strings
    - max_choices: maximale Anzahl erlaubter Auswahloptionen (oder None = unbegrenzt)

    Rückgabe:
    - dict mit "selected" (Liste) und "other" (String)
    """
    st.markdown(f"#### {title}")

    # Hinweis zu maximaler Auswahl
    if max_choices is not None:
        st.caption(f"Bitte höchstens **{max_choices}** Antworten auswählen.")

    selected = st.multiselect(
        label="Auswahl:",
        options=options,
        key=f"{key_prefix}_multiselect"
    )

    # Soft-Validierung der Auswahlmenge
    if max_choices is not None and len(selected) > max_choices:
        st.error(
            f"Du hast {len(selected)} Antworten ausgewählt. "
            f"Bitte auf maximal {max_choices} reduzieren."
        )

    other = st.text_input(
        label="Sonstiges / eigene Antwort:",
        key=f"{key_prefix}_other"
    )

    st.markdown("---")

    return {
        "selected": selected,
        "other": other
    }


# ---------------------- Fragen definieren --------------------

antworten: Dict[str, Any] = {}

antworten["q1_motive"] = question_multiselect(
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
    max_choices=3  # Beispiel: max. 3 Antworten
)

antworten["q2_erwartung"] = question_multiselect(
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

antworten["q3_themen"] = question_multiselect(
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

antworten["q4_aendern"] = question_multiselect(
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

antworten["q5_hemmnisse"] = question_multiselect(
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

# Avatar bei den Antworten ergänzen (nur Emoji, keine Klarnamen)
antworten["avatar"] = st.session_state.get("chosen_avatar", None)

# ============================================================
# VORSCHAU DER ANTWORTEN (nur lokal, keine Speicherung)
# ============================================================

st.markdown("### 🔍 Vorschau (nur zur Präsentation)")

st.markdown(
    """
    Hier siehst Du, wie die Antworten in der späteren Version strukturiert
    erfasst werden könnten.  
    Diese Daten werden derzeit **nirgendwo gespeichert** – sie sind nur in
    dieser Session sichtbar.
    """
)

if st.button("Antworten als Beispiel anzeigen"):
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

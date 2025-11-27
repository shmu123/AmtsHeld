import streamlit as st
import google.generativeai as genai
from PIL import Image

# Das ist der Titel deiner App
st.set_page_config(page_title="Mein AmtsHeld", page_icon="🦁")

st.title("🦁 Mein AmtsHeld")
st.write("Mach ein Foto von deinem Brief. Die KI hilft dir.")

# Hier kommt der Schlüssel rein (linke Seitenleiste)
with st.sidebar:
    st.header("Einstellungen")
    api_key = st.text_input("Dein Google Key", type="password")
    st.markdown("[Hier Key kostenlos holen](https://aistudio.google.com/app/apikey)")

# Die Funktion, die Google fragt
def frage_google(bild, befehl, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    antwort = model.generate_content([befehl, bild])
    return antwort.text

# Auswahl: Was ist es?
modus = st.radio("Was hast du bekommen?", ["Behörden-Brief / Rechnung", "Arzt-Brief / Befund"])
upload = st.file_uploader("Foto hochladen", type=["jpg", "png", "jpeg", "webp"])

if upload and api_key:
    # Bild anzeigen
    bild = Image.open(upload)
    st.image(bild, caption="Dein Bild", use_column_width=True)
    
    if st.button("🚀 Analysieren!"):
        with st.spinner("Ich lese den Brief..."):
            try:
                # Hier sind deine spezialisierten Befehle
                if modus == "Behörden-Brief / Rechnung":
                    befehl = """
                    Du bist 'AmtsHeld'. Analysiere dieses Dokument.
                    Antworte GENAU so:
                    
                    🚦 **STATUS: [🔴 ROT / 🟡 GELB / 🟢 GRÜN]**
                    TIMELINE: 📅 [Fristdatum oder 'Keine Eile']
                    
                    🧐 **WORUM GEHT ES?**
                    (Max 2 einfache Sätze).
                    
                    ✅ **TO-DO:**
                    1. [Schritt 1]
                    2. [Schritt 2]
                    
                    💰 **KOSTEN:** [Betrag]
                    """
                else:
                    befehl = """
                    Du bist 'MediHelp'. Übersetze dieses medizinische Dokument.
                    Antworte GENAU so:
                    
                    🧠 **ÜBERSETZUNG (Was habe ich?):**
                    (Fachbegriffe einfach erklärt).
                    
                    🏥 **WOHIN MUSS ICH?**
                    (Welcher Facharzt?).
                    
                    📝 **TELEFON-SKRIPT:**
                    (Ein Satz für die Terminvereinbarung).
                    
                    ⚠️ Ich bin eine KI, kein Arzt.
                    """
                
                # Google fragen
                ergebnis = frage_google(bild, befehl, api_key)
                st.write(ergebnis)
                
            except Exception as e:
                st.error(f"Fehler: Der Key ist falsch oder das Bild unlesbar. ({e})")
elif upload and not api_key:
    st.warning("Bitte gib links oben deinen Google Key ein!")
  

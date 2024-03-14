"""
Moodle Language String Translator

Version: 2024031401

"""

import streamlit as st
import sentencepiece as spm
import ctranslate2
from nltk import sent_tokenize
import pyperclip

def translate(source, translator, sp_source_model, sp_target_model):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): Source sentences to translate
        translator (object): Object of Translator, with the CTranslate2 model
        sp_source_model (object): Object of SentencePieceProcessor, with the SentencePiece source model
        sp_target_model (object): Object of SentencePieceProcessor, with the SentencePiece target model
    Returns:
        Translation of the source text
    """

    source_sentences = sent_tokenize(source)
    source_tokenized = sp_source_model.encode(source_sentences, out_type=str)
    translations = translator.translate_batch(source_tokenized)
    translations = [translation.hypotheses[0] for translation in translations]
    translations_detokenized = sp_target_model.decode(translations)
    translation = " ".join(translations_detokenized)

    # Remove double quotes from translation
    translation = translation.replace('"', '')

    return translation


# [Modify] File paths here to the CTranslate2 SentencePiece models.
ct_model_path = "models/enslo_ctranslate2/"
sp_source_model_path = "models/source.model"
sp_target_model_path = "models/target.model"

# Create objects of CTranslate2 Translator and SentencePieceProcessor to load the models
translator = ctranslate2.Translator(ct_model_path, "cpu")    # or "cuda" for GPU
sp_source_model = spm.SentencePieceProcessor(sp_source_model_path)
sp_target_model = spm.SentencePieceProcessor(sp_target_model_path)


# Title for the page and nice icon
st.set_page_config(page_title="Moodle Language String Translator", page_icon="🇸🇮")
# Header
st.title("Moodle Language String Translator")
st.write("This application aims to provide machine translation specialized for Moodle LMS. It currently supports translation from English to Slovenian.")

# Form to add your items
with st.form("my_form"):
    # Textarea to type the source text.
    user_input = st.text_area("English Text", key="textarea")

    # Translate with CTranslate2 model if form is submitted for the first time
    if st.form_submit_button("Translate", "Translate from English to Slovenian"):
        st.session_state.translation = translate(user_input, translator, sp_source_model, sp_target_model)

    # Display Slovenian Translation
    st.write("Slovenian Translation")
    st.info(st.session_state.get("translation", ""))

    # Copy to clipboard of Slovenian Translation
    copytoclipboard = st.form_submit_button("Copy to Clipboard", "Copy from Slovenian translation to clipboard")
    if copytoclipboard:
       pyperclip.copy(st.session_state.get("translation", ""))

# Optional Style
# Source: https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

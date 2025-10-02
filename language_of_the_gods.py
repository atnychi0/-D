# -*- coding: utf-8 -*-
"""Toolkit for translating phrases into the so-called "Language of the Gods".

This module exposes two public helpers:

``translate_to_divine``
    Performs a best-effort word-for-word translation from a limited English
    vocabulary into the divine language found in the source manuscripts.
``symbolic_encrypt_layer2``
    Applies the "Layer 2" vowel-stripping cipher that appears in the lore.

The original script bundled a small dictionary, however the translator would
silently drop any word that was not an *exact* match.  That meant phrases such
as "Light expands into growth" translated to "Lumir Orasen", because the
inflected form "expands" was not found.  This module now includes a lightweight
normalisation layer so that a handful of common inflections automatically map
back to their dictionary lemmas before translation.
"""

from __future__ import annotations

from typing import Dict, Iterable

# Consolidated vocabulary from all provided documents.
# In cases of multiple words for one concept, a primary one is chosen.
VOCABULARY: Dict[str, str] = {
    # Nouns and Concepts
    "creation": "Naeth",
    "light": "Lumir",
    "energy": "Setir",
    "growth": "Orasen",
    "expansion": "Critos",
    "time": "Traven",
    "harmony": "Seranik",
    "reflection": "Ecovis",
    "spirit": "Ethir",
    "source": "Fulah",
    "movement": "Rairt",
    "existence": "Daieth",
    "soul": "Dib",
    "weight": "Omnen",
    "totality": "Omnel",
    "flow": "Jumiir",
    "eternity": "Rqai",

    # Verbs
    "create": "Naeth",  # Note: "Naeth" is used for both the noun and verb
    "command": "Restir",
    "rise": "Dirim",
    "align": "Kinnas",  # As in "I align"
    "unite": "Qeren",

    # Pronouns
    "i": "Kinnas",  # As in "I reflect..."

    # Prepositions / Conjunctions
    "into": "",  # Often implied by word order
    "of": "",    # Often implied
    "the": "",   # Not used
    "and": "",   # Implied
}

# Manual fixes for common inflected forms observed in the manuscripts and demo
# phrases shipped with the repository.
_MANUAL_NORMALISATIONS: Dict[str, str] = {
    "expands": "expansion",
    "expanding": "expansion",
    "expanded": "expansion",
    "expand": "expansion",
    "reflects": "reflection",
    "reflecting": "reflection",
    "reflected": "reflection",
    "creates": "create",
    "creating": "create",
    "created": "create",
    "eternal": "eternity",
    "eternally": "eternity",
}

# Simple suffix based rules provide a last-resort fallback for other inflected
# variants.  The rules are intentionally conservative to avoid accidental
# rewrites of already valid dictionary entries.
_SUFFIX_RULES: Iterable[tuple[str, str]] = (
    ("ies", "y"),
    ("es", ""),
    ("s", ""),
    ("ing", ""),
    ("ed", ""),
    ("ly", ""),
)

VOWELS = "aeiouAEIOU"


def _normalise_word(word: str) -> str:
    """Return the best dictionary candidate for ``word``.

    The function first checks the manual normalisation map, then attempts a
    small collection of suffix stripping rules.  If no better match can be
    found the original word is returned.
    """

    if word in VOCABULARY:
        return word

    manual_candidate = _MANUAL_NORMALISATIONS.get(word)
    if manual_candidate:
        return manual_candidate

    for suffix, replacement in _SUFFIX_RULES:
        if len(word) > len(suffix) and word.endswith(suffix):
            candidate = f"{word[:-len(suffix)]}{replacement}"
            if candidate in VOCABULARY:
                return candidate

    return word


def translate_to_divine(english_phrase: str) -> str:
    """Translate a simple English phrase into the Language of the Gods.

    The translator performs a word-for-word conversion based on the known
    vocabulary.  Words not present in the dictionary are ignored; callers can
    inspect the result to detect gaps if needed.
    """

    cleaned_phrase = english_phrase.lower().replace(".", "").replace(",", "")
    words = cleaned_phrase.split()

    translated_words = []
    for word in words:
        dictionary_key = _normalise_word(word)
        translated = VOCABULARY.get(dictionary_key)
        if translated:
            translated_words.append(translated)

    # Capitalize the first letter of each word for stylistic consistency.
    formatted_words = [word.capitalize() for word in translated_words]

    return (
        " ".join(formatted_words)
        if formatted_words
        else "Translation failed: Words not found in vocabulary."
    )


def symbolic_encrypt_layer2(divine_phrase: str) -> str:
    """Apply Layer 2 symbolic encryption (vowel removal) to a phrase."""

    encrypted_words = []
    for word in divine_phrase.split():
        # Keep the first letter (as it's often capitalized) and remove subsequent vowels.
        first_letter = word[0]
        rest_of_word = word[1:]
        compressed_rest = "".join(char for char in rest_of_word if char not in VOWELS)
        encrypted_words.append(first_letter + compressed_rest)

    return " ".join(encrypted_words)


if __name__ == "__main__":
    print("--- Language of the Gods Toolkit ---")
    print("\nThis script demonstrates translation and encryption based on the provided lore.\n")

    # --- Demonstration 1: Translation from Template 1 ---
    phrase1_en = "Light expands into growth"
    phrase1_divine = translate_to_divine(phrase1_en)
    print(f"Translating: '{phrase1_en}'")
    print(f"Result: {phrase1_divine}")
    print("-" * 20)

    # --- Demonstration 2: Translation from Template 2 ---
    phrase2_en = "Time reflects the harmony of spirit"
    phrase2_divine = translate_to_divine(phrase2_en)
    print(f"Translating: '{phrase2_en}'")
    print(f"Result: {phrase2_divine}")
    print("-" * 20)

    # --- Demonstration 3: Symbolic Encryption ---
    phrase3_divine = "Restir Omnen"
    phrase3_encrypted = symbolic_encrypt_layer2(phrase3_divine)
    print(f"Encrypting (Layer 2): '{phrase3_divine}'")
    print(f"Result: {phrase3_encrypted}")
    print("-" * 20)

    # --- Demonstration 4: Full Workflow ---
    phrase4_en = "Create energy eternally"
    phrase4_divine = translate_to_divine(phrase4_en)
    phrase4_encrypted = symbolic_encrypt_layer2(phrase4_divine)
    print("Full Workflow Example:")
    print(f"1. English Phrase:         '{phrase4_en}'")
    print(f"2. Translated to Divine:   '{phrase4_divine}'")
    print(f"3. Symbolically Encrypted: '{phrase4_encrypted}'")
    print("-" * 20)

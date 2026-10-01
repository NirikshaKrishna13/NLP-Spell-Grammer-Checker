import re
from difflib import get_close_matches

import spacy
from nltk.corpus import words


# Common words that may not be present in the NLTK dictionary
COMMON_WORDS = {
    "ai",
    "ml",
    "nlp",
    "python",
    "github",
    "streamlit",
    "spacy",
    "nltk",
    "college",
    "university",
    "internet",
    "website",
    "email",
    "computer",
    "science",
    "engineering",
    "project",
    "application",
    "data",
    "database",
    "machine",
    "learning",
    "software",
    "developer",
    "development",
}


# Frequently seen spelling mistakes
COMMON_CORRECTIONS = {
    "recieve": "receive",
    "recieved": "received",
    "recieving": "receiving",
    "teh": "the",
    "adress": "address",
    "becuase": "because",
    "definately": "definitely",
    "seperate": "separate",
    "occured": "occurred",
    "untill": "until",
    "wich": "which",
    "whcih": "which",
    "dont": "don't",
    "doesnt": "doesn't",
    "didnt": "didn't",
    "cant": "can't",
    "wont": "won't",
    "isnt": "isn't",
    "arent": "aren't",
    "im": "I'm",
    "ive": "I've",
    "frend": "friend",
    "frends": "friends",
    "mesage": "message",
    "mesages": "messages",
    "grammer": "grammar",
    "speling": "spelling",
}


# Rule-based grammar patterns
GRAMMAR_RULES = [
    (
        re.compile(r"\b(I|i)\s+is\b"),
        lambda m: f"{m.group(1)} am",
        "Use 'am' with I.",
    ),

    (
        re.compile(r"\b(he|she|it)\s+go\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} goes",
        "Use 'goes' with a third-person singular subject.",
    ),

    (
        re.compile(r"\b(he|she|it)\s+do\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} does",
        "Use 'does' with a third-person singular subject.",
    ),

    (
        re.compile(r"\b(he|she|it)\s+don't\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} doesn't",
        "Use 'doesn't' with a third-person singular subject.",
    ),

    (
        re.compile(r"\b(I|you|we|they)\s+does\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} do",
        "Use 'do' with I, you, we, and they.",
    ),

    (
        re.compile(r"\b(I|you|we|they)\s+goes\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} go",
        "Use 'go' with I, you, we, and they.",
    ),

    (
        re.compile(r"\b(it|he|she)\s+are\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} is",
        "Use 'is' with a singular subject.",
    ),

    (
        re.compile(r"\b(we|they|you)\s+is\b", re.IGNORECASE),
        lambda m: f"{m.group(1)} are",
        "Use 'are' with plural subjects and 'you'.",
    ),
]


def load_nlp():
    """
    Load spaCy English model.
    """

    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp

    except OSError:
        raise RuntimeError(
            "spaCy English model is not installed.\n\n"
            "Run this command in VS Code terminal:\n\n"
            "python -m spacy download en_core_web_sm"
        )


def build_dictionary():
    """
    Build spelling dictionary using NLTK words corpus.
    """

    try:
        nltk_words = words.words()

    except LookupError:
        raise RuntimeError(
            "NLTK words corpus is missing.\n\n"
            "Run:\n"
            "python download_nltk_data.py"
        )

    dictionary = set()

    for word in nltk_words:

        if word.isalpha() and len(word) > 1:
            dictionary.add(word.lower())

    dictionary.update(COMMON_WORDS)

    dictionary.update(
        word.lower()
        for word in COMMON_CORRECTIONS.values()
    )

    return dictionary


def preserve_case(original, corrected):
    """
    Preserve capitalization.
    """

    if original.isupper():
        return corrected.upper()

    if original[0].isupper():
        return corrected.capitalize()

    return corrected


def get_spelling_suggestion(word, dictionary):
    """
    Find a spelling correction.
    """

    lower_word = word.lower()

    # Known correction
    if lower_word in COMMON_CORRECTIONS:

        correction = COMMON_CORRECTIONS[lower_word]

        return (
            preserve_case(word, correction),
            "Known spelling correction",
        )

    # Correct word
    if lower_word in dictionary:
        return None, None

    # Ignore very short words
    if len(lower_word) <= 2:
        return None, None

    # Find closest word
    matches = get_close_matches(
        lower_word,
        dictionary,
        n=1,
        cutoff=0.75,
    )

    if matches:

        correction = preserve_case(
            word,
            matches[0],
        )

        return (
            correction,
            "Closest dictionary match",
        )

    return None, None


def find_spelling_errors(text, dictionary):
    """
    Detect spelling errors.
    """

    errors = []

    pattern = r"\b[A-Za-z][A-Za-z']+\b"

    for match in re.finditer(pattern, text):

        word = match.group()

        suggestion, reason = get_spelling_suggestion(
            word,
            dictionary,
        )

        if suggestion:

            errors.append(
                {
                    "word": word,
                    "suggestion": suggestion,
                    "reason": reason,
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    return errors


def apply_spelling_corrections(text, errors):
    """
    Apply spelling corrections.
    """

    corrected_text = text

    for error in reversed(errors):

        corrected_text = (
            corrected_text[:error["start"]]
            + error["suggestion"]
            + corrected_text[error["end"]:]
        )

    return corrected_text


def find_grammar_errors(text):
    """
    Detect common grammar errors.
    """

    errors = []

    for pattern, replacement, reason in GRAMMAR_RULES:

        for match in pattern.finditer(text):

            original = match.group()

            suggestion = replacement(match)

            if original != suggestion:

                errors.append(
                    {
                        "original": original,
                        "suggestion": suggestion,
                        "reason": reason,
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

    errors.sort(
        key=lambda error: error["start"]
    )

    return errors


def apply_grammar_corrections(text, errors):
    """
    Apply grammar corrections.
    """

    corrected_text = text

    for error in reversed(errors):

        corrected_text = (
            corrected_text[:error["start"]]
            + error["suggestion"]
            + corrected_text[error["end"]:]
        )

    return corrected_text


def analyze_text(text):
    """
    MAIN FUNCTION

    This is the function imported by app.py:

        from src.analyzer import analyze_text
    """

    if not text or not text.strip():

        return {
            "word_count": 0,
            "sentence_count": 0,
            "character_count": 0,
            "unique_words": 0,
            "tokens": [],
            "pos_tags": [],
            "spelling_errors": [],
            "grammar_errors": [],
            "all_suggestions": [],
            "corrected_text": "",
        }

    # Load spaCy
    nlp = load_nlp()

    # Load spelling dictionary
    dictionary = build_dictionary()

    # -----------------------------
    # NLP PROCESSING
    # -----------------------------

    doc = nlp(text)

    # Tokens
    tokens = [
        token.text
        for token in doc
        if not token.is_space
    ]

    # POS tags
    pos_tags = []

    for token in doc:

        if not token.is_space:

            pos_tags.append(
                (
                    token.text,
                    token.pos_,
                    token.tag_,
                )
            )

    # -----------------------------
    # SPELL CHECK
    # -----------------------------

    spelling_errors = find_spelling_errors(
        text,
        dictionary,
    )

    corrected_text = apply_spelling_corrections(
        text,
        spelling_errors,
    )

    # -----------------------------
    # GRAMMAR CHECK
    # -----------------------------

    grammar_errors = find_grammar_errors(
        corrected_text,
    )

    corrected_text = apply_grammar_corrections(
        corrected_text,
        grammar_errors,
    )

    # -----------------------------
    # STATISTICS
    # -----------------------------

    word_tokens = [
        token.text.lower()
        for token in doc
        if token.is_alpha
    ]

    sentence_count = len(
        list(doc.sents)
    )

    word_count = len(word_tokens)

    unique_words = len(
        set(word_tokens)
    )

    character_count = len(text)

    # -----------------------------
    # FINAL RESULT
    # -----------------------------

    return {

        "word_count": word_count,

        "sentence_count": sentence_count,

        "character_count": character_count,

        "unique_words": unique_words,

        "tokens": tokens,

        "pos_tags": pos_tags,

        "spelling_errors": spelling_errors,

        "grammar_errors": grammar_errors,

        "all_suggestions": (
            spelling_errors
            + grammar_errors
        ),

        "corrected_text": corrected_text,
    }
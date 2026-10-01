import streamlit as st
from src.analyzer import analyze_text

st.set_page_config(
    page_title="NLP Grammar & Spell Checker",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ NLP-Based Grammar and Spell Checker")
st.caption("A local NLP application using NLTK + spaCy for spelling, grammar, tokenization and linguistic analysis.")

with st.sidebar:
    st.header("Settings")
    show_tokens = st.checkbox("Show token analysis", value=True)
    show_pos = st.checkbox("Show POS tags", value=True)
    show_clean = st.checkbox("Show corrected text", value=True)

text = st.text_area(
    "Enter text to analyze:",
    height=220,
    placeholder="Type your sentence or paragraph here..."
)

if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing text..."):
            result = analyze_text(text)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Words", result["word_count"])
        c2.metric("Spelling Issues", len(result["spelling_errors"]))
        c3.metric("Grammar Issues", len(result["grammar_errors"]))
        c4.metric("Suggestions", len(result["all_suggestions"]))

        st.markdown("### 📄 Analysis Result")

        if show_clean:
            st.subheader("Corrected Text")
            st.success(result["corrected_text"])

        st.subheader("📝 Spelling Suggestions")
        if result["spelling_errors"]:
            for err in result["spelling_errors"]:
                st.write(
                    f"**{err['word']}** → **{err['suggestion']}** "
                    f"({err['reason']})"
                )
        else:
            st.success("No spelling errors detected.")

        st.subheader("📚 Grammar Suggestions")
        if result["grammar_errors"]:
            for err in result["grammar_errors"]:
                st.write(
                    f"**{err['original']}** → **{err['suggestion']}**  \n"
                    f"Reason: {err['reason']}"
                )
        else:
            st.success("No rule-based grammar errors detected.")

        if show_tokens:
            st.subheader("🔤 Tokenization")
            st.code(" | ".join(result["tokens"]))

        if show_pos:
            st.subheader("🏷️ Part-of-Speech Analysis")
            import pandas as pd
            df = pd.DataFrame(result["pos_tags"], columns=["Token", "POS", "Description"])
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("📊 Linguistic Statistics")
        s1, s2, s3 = st.columns(3)
        s1.metric("Sentences", result["sentence_count"])
        s2.metric("Characters", result["character_count"])
        s3.metric("Unique Words", result["unique_words"])

st.markdown("---")
st.caption("NLP-Based Grammar and Spell Checker | Python • NLTK • spaCy • Streamlit")

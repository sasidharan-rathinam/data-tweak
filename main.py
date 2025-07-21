import streamlit as st

st.title("Convert Multiline Numbers to Comma-Separated Line")

# Multiline input
numbers_input = st.text_area("Enter numbers (one per line):", height=300)

if numbers_input:
    # Split lines, strip whitespace, filter non-empty, and join with commas
    numbers = [line.strip() for line in numbers_input.splitlines() if line.strip()]
    comma_separated = ", ".join(numbers)

    st.subheader("Comma-Separated Output:")
    st.code(comma_separated, language="text")

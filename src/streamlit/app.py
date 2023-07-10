import streamlit as st


def do_something(text: str, value: int) -> None:
    st.markdown("## **result**")
    st.markdown(f"{text}")
    st.markdown(f"{value}")


def main() -> None:
    st.title("This is title")
    st.header("This is header")

    value = st.sidebar.slider("slider", 0, 100, 50)
    st.sidebar.text_area("text area")

    text = st.text_input("text input")
    if st.button("button"):
        do_something(text, value)


if __name__ == "__main__":
    main()

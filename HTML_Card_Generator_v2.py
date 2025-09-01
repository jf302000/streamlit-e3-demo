import streamlit as st
from streamlit_tags import st_tags

# ---------- Helper Functions ----------
ANIMATIONS = {
    "bounce": "@keyframes bounce {0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-10px);} 60% {transform: translateY(-5px);}}",
    "fade-in": "@keyframes fade-in {from {opacity: 0;} to {opacity: 1;}}",
    "slide-in": "@keyframes slide-in {from {transform: translateX(-100%);} to {transform: translateX(0);}}",
    "rotate": "@keyframes rotate {from {transform: rotate(0deg);} to {transform: rotate(360deg);}}",
    "zoom": "@keyframes zoom {from {transform: scale(0);} to {transform: scale(1);}}"
}

def generate_animation_styles(animations):
    styles = {
        "bounce": "@keyframes bounce {0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-10px);} 60% {transform: translateY(-5px);}}",
        "fade-in": "@keyframes fade-in {from {opacity: 0;} to {opacity: 1;}}",
        "slide-in": "@keyframes slide-in {from {transform: translateX(-100%);} to {transform: translateX(0);}}",
        "rotate": "@keyframes rotate {from {transform: rotate(0deg);} to {transform: rotate(360deg);}}",
        "zoom": "@keyframes zoom {from {transform: scale(0);} to {transform: scale(1);}}"
    }
    return "<style>" + "".join([styles[a] for a in animations if a in styles]) + "</style>"

def generate_card_html(title, text, bg_color, shape, width, height, animation, font, text_align, padding, title_size, desc_size, title_color, desc_color):
    border_radius = "10px" if shape == "Rounded" else "50%" if shape == "Circle" else "0px"
    animation_css = animation.lower().replace(" ", "-")
    style_block = generate_animation_styles([animation_css]) if animation != "None" else ""

    return f"""
        {style_block}
        <div style="
            background-color: {bg_color};
            padding: {padding}px;
            border-radius: {border_radius};
            width: {width}px;
            height: {height}px;
            text-align: {text_align.lower()};
            animation: {animation_css} 1s ease;
            font-family: {font};
            display: flex;
            justify-content: center;
            align-items: center;
        ">
            <div>
                <h3 style="font-size: {title_size}px; color: {title_color};">{title}</h3>
                <p style="font-size: {desc_size}px; color: {desc_color};">{text}</p>
            </div>
        </div>
    """

# ---------- UI ----------
st.title("HTML Generator")
st.write("Welcome to the HTML Generator Tool! Customise cards with advanced formatting options, and merge HTML and CSS.")

# Consolidate tab initialization
tabs = st.tabs(["Cards", "HTML + CSS Merger"])

# ---------- Cards Tab ----------
tabs[0].header("Card Customisation")
card_title = tabs[0].text_input("Enter Card Title", "Card Title")
card_desc = tabs[0].text_area("Enter Card Description", "This is a card with some description.")
card_color = tabs[0].color_picker("Pick a Card Background Color", "#A9D0F5")
card_shape = tabs[0].selectbox("Select Card Shape", ["Rounded", "Square", "Circle"], key="card_shape")
card_font = tabs[0].selectbox("Select Font Style", ["Arial", "Verdana", "Times New Roman", "Courier New"], key="card_font")
card_text_align = tabs[0].selectbox("Text Alignment", ["Left", "Center", "Right"], key="card_text_align")
card_padding = tabs[0].slider("Padding (px)", 0, 50, 20, key="card_padding")
card_title_size = tabs[0].slider("Title Font Size (px)", 12, 48, 24, key="card_title_size")
card_desc_size = tabs[0].slider("Description Font Size (px)", 10, 36, 16, key="card_desc_size")
card_title_color = tabs[0].color_picker("Title Color", "#000000", key="card_title_color")
card_desc_color = tabs[0].color_picker("Description Color", "#333333", key="card_desc_color")
card_width = tabs[0].slider("Card Width (px)", 100, 500, 300, key="card_width")
card_height = tabs[0].slider("Card Height (px)", 100, 500, 200, key="card_height")

# Enhance card customization with additional animation options
card_animation = tabs[0].selectbox("Select Animation", ["None", "Bounce", "Fade-In", "Slide-In", "Rotate", "Zoom"], key="card_animation")

# Fix the border and shadow effects to ensure they are applied correctly in the card generation logic
if card_title and card_desc:
    card_html = generate_card_html(
        card_title, card_desc, card_color, card_shape, card_width, card_height, card_animation,
        card_font, card_text_align,
        card_padding, card_title_size, card_desc_size,
        card_title_color, card_desc_color
    )
    tabs[0].markdown(card_html, unsafe_allow_html=True)
    tabs[0].subheader("Generated HTML Code:")
    tabs[0].code(card_html)
    if tabs[0].button("Convert to Power BI Code", key="card_pbi_conversion"):
        # Unescape HTML and escape double quotes for DAX
        pbi_card_code = (
            "<HTML> Card Measure = \"" +
            card_html.replace("&lt;", "<").replace("&gt;", ">").replace("\"", "\"\"") +
            "\""
        ).replace("+", "&")
        tabs[0].code(pbi_card_code)

# ---------- HTML + CSS Merger Tab ----------
tabs[1].header("Merge HTML and CSS")
html_input = tabs[1].text_area("Paste your HTML code here", height=200)
css_input = tabs[1].text_area("Paste your CSS code here", height=200)

if html_input and css_input:
    merged_code = f"<style>\n{css_input}\n</style>\n{html_input}"
    tabs[1].subheader("Merged HTML + CSS Code")
    tabs[1].code(merged_code, language="html")
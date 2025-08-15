import streamlit as st
from streamlit_tags import st_tags

# ---------- Helper Functions ----------
def generate_animation_styles(animations):
    styles = {
        "bounce": "@keyframes bounce {0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-10px);} 60% {transform: translateY(-5px);}}",
        "fade-in": "@keyframes fade-in {from {opacity: 0;} to {opacity: 1;}}",
        "slide-in": "@keyframes slide-in {from {transform: translateX(-100%);} to {transform: translateX(0);}}",
        "rotate": "@keyframes rotate {from {transform: rotate(0deg);} to {transform: rotate(360deg);}}",
        "zoom": "@keyframes zoom {from {transform: scale(0);} to {transform: scale(1);}}"
    }
    return "<style>" + "".join([styles[a] for a in animations if a in styles]) + "</style>"

def generate_button_html(text, color, hover_color, size, shape, animation):
    font_size = {"Small": 20, "Medium": 30, "Large": 40}[size]
    border_radius = "50px" if shape == "Rounded" else "0px"
    animation_css = animation.lower().replace(" ", "-")
    style_block = generate_animation_styles([animation_css]) if animation != "None" else ""
    
    return f"""
        {style_block}
        <button style="
            background-color: {color};
            font-size: {font_size}px;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: {border_radius};
            cursor: pointer;
            transition: background-color 0.3s ease;
            animation: {animation_css} 1s infinite;
        " onmouseover="this.style.backgroundColor='{hover_color}'" 
           onmouseout="this.style.backgroundColor='{color}'">
            {text}
        </button>
    """

def generate_card_html(title, text, bg_color, shape, animation):
    border_radius = "10px" if shape == "Rounded" else "0px"
    animation_css = animation.lower().replace(" ", "-")
    style_block = generate_animation_styles([animation_css]) if animation != "None" else ""
    
    return f"""
        {style_block}
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: {border_radius};
            width: 300px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            animation: {animation_css} 1s ease;
        ">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
    """

def generate_form_html(name, fields):
    inputs = "".join([
        f"<input type='text' placeholder='Enter {field}' style='padding: 10px; width: 100%; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;'/>"
        for field in fields
    ])
    return f"""
        <form>
            <h3>{name}</h3>
            {inputs}
            <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;">Submit</button>
        </form>
    """

# ---------- UI ----------
st.title("HTML Generator")
st.write("Welcome to the HTML Generator Tool! Customise buttons, cards, and forms in a unified interface, and convert them to Power BI Measures.")

tabs = st.tabs(["Buttons", "Cards", "Forms"])

# ---------- Buttons Tab ----------
tabs[0].header("Button Customization")
btn_text = tabs[0].text_input("Enter Button Text", "Click Me")
btn_color = tabs[0].color_picker("Pick a Button Color", "#FF5733")
btn_hover = tabs[0].color_picker("Pick a Hover Color", "#FFC300")
btn_size = tabs[0].selectbox("Select Button Size", ["Small", "Medium", "Large"])
btn_shape = tabs[0].selectbox("Select Button Shape", ["Rounded", "Square"])
btn_anim = tabs[0].selectbox("Select Animation", ["None", "Scale", "Bounce", "Fade-In"])

# Fixing Button Customization Power BI Code Generation
if btn_text:
    btn_html = generate_button_html(btn_text, btn_color, btn_hover, btn_size, btn_shape, btn_anim)
    tabs[0].markdown(btn_html, unsafe_allow_html=True)
    tabs[0].subheader("Generated HTML Code:")
    tabs[0].code(btn_html)
    if tabs[0].button("Convert to Power BI Code", key="button_pbi"):
        # Unescape HTML and escape double quotes for DAX
        pbi_button_code = (
            "<HTML> Button Measure = \"" +
            btn_html.replace("&lt;", "<").replace("&gt;", ">").replace("\"", "\"\"") +
            "\""
        ).replace("+", "&")
        tabs[0].code(pbi_button_code)

# ---------- Cards Tab ----------
tabs[1].header("Card Customization")
card_title = tabs[1].text_input("Enter Card Title", "Card Title")
card_desc = tabs[1].text_area("Enter Card Description", "This is a card with some description.")
card_color = tabs[1].color_picker("Pick a Card Background Color", "#A9D0F5")
card_shape = tabs[1].selectbox("Select Card Shape", ["Rounded", "Square"])
card_anim = tabs[1].selectbox("Select Animation", ["None", "Slide-In", "Rotate", "Zoom"])

# Fixing Card Customization Power BI Code Generation
if card_title and card_desc:
    card_html = generate_card_html(card_title, card_desc, card_color, card_shape, card_anim)
    tabs[1].markdown(card_html, unsafe_allow_html=True)
    tabs[1].subheader("Generated HTML Code:")
    tabs[1].code(card_html)
    if tabs[1].button("Convert to Power BI Code", key="card_pbi"):
        # Unescape HTML and escape double quotes for DAX
        pbi_card_code = (
            "<HTML> Card Measure = \"" +
            card_html.replace("&lt;", "<").replace("&gt;", ">").replace("\"", "\"\"") +
            "\""
        ).replace("+", "&")
        tabs[1].code(pbi_card_code)

# ---------- Forms Tab ----------
tabs[2].header("Form Customization")
form_name = tabs[2].text_input("Enter Form Name", "Contact Us")

with tabs[2]:
    # Add Input Fields functionality restricted to Forms section
    form_fields = st_tags(
        label='Add Input Fields',
        text='Press enter to add more fields',
        value=['Name', 'Email'],
        suggestions=['Name', 'Email', 'Message', 'Phone']
    )

    if form_name and form_fields:
        form_html = generate_form_html(form_name, form_fields)
        tabs[2].markdown(form_html, unsafe_allow_html=True)
        tabs[2].subheader("Generated HTML Code:")
        tabs[2].code(form_html)
        if tabs[2].button("Convert to Power BI Code", key="form_pbi"):
            # Unescape HTML and escape double quotes for DAX
            pbi_form_code = (
                "<HTML> Form Measure = \"" +
                form_html.replace("&lt;", "<").replace("&gt;", ">").replace("\"", "\"\"") +
                "\""
            ).replace("+", "&")
            tabs[2].code(pbi_form_code)
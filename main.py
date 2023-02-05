import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_fonts(url):
    # Make a request to the website
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find all CSS stylesheets
    stylesheets = []
    for link in soup.find_all('link', {'rel': 'stylesheet'}):
        if 'href' in link.attrs:
            stylesheet_url = urljoin(url, link['href'])
            stylesheets.append(stylesheet_url)

    # Find all font-family declarations in the CSS
    fonts = []
    for stylesheet in stylesheets:
        css = requests.get(stylesheet).text
        lines = css.split('\n')
        for line in lines:
            if 'font-family' in line:
                start = line.find('font-family:') + len('font-family:')
                end = line.find(';', start)
                font_name = line[start:end].strip()
                fonts.append(font_name)
    return fonts

st.title("Font Finder")

url = st.text_input("Enter a URL:")
if url:
    with st.spinner("Finding fonts..."):
        fontss = find_fonts(url)
    st.header("Fonts used in this website:")
    newFont = []
    for font in fontss:
        if "," in font:
            temp = font.split(",")
            for i in temp:
                newFont.append(i)
        else:
            newFont.append(font)
    for font in newFont:
        st.write(f"{font} \n")

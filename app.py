import streamlit as st
import helper
import argparse
import pickle
import base64


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('quorabackgr.jpg')

# Initialize argparse
parser = argparse.ArgumentParser(description="Streamlit App with Command-Line Arguments")
parser.add_argument('--input_file', type=str, help='Path to the input file')
parser.add_argument('--output_file', type=str, help='Path to the output file')
args = parser.parse_args()

if args.input_file:
    input_file = args.input_file
else:
    input_file = "default_input.txt"

if args.output_file:
    output_file = args.output_file
else:
    output_file = "default_output.txt"

# Add an image
st.image("images.png")
with open('model.pkl', 'rb') as f:
    unpickler = pickle.Unpickler(f)
    while True:
        try:
            model = unpickler.load()
            break
        except EOFError:
            continue
model = pickle.load(open('model.pkl', 'rb'))

st.header('Predicting if the given Questions are duplicate or not')

q1 = st.text_input('Enter the First Question')
q2 = st.text_input('Enter the Second Question')
if st.button('Predict'):
    query = helper.query_point_creator(q1,q2)
    result = model.predict(query)[0]
    if result:
        st.header('The given Questions is Duplicate')
    else:
        st.header('The given Quesions are Not Duplicate')
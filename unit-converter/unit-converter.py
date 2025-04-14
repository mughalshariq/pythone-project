import streamlit as st

st.title("🌏Unit Converter App")
st.markdown("### converts units of length, weight, and Time Instantly.")
st.write("Welcome! Select a Category, enter a value and get the converter result in real-time.")

category = st.selectbox("Choose a Category", ["Length", "Weight", "Time"])

def convert_units(category, value, units):
    if category == "Length":
        if units == "kilometer to miles":
            return value *0.621371
        elif units == "miles to kilometers":
            return value / 0.621371
    elif category == "Weight":
        if units == "kilogram to pound":
            return value * 2.20462
    elif category == "Time":
        if units == "seconds":
            return value / 60
        elif units == "minutes to seconds":
            return value * 60
        elif units == "minutes to hours":
            return value / 60
        elif units == "hours to minutes":
            return value * 60
        elif units == "hours to day":
            return value / 24
        elif units == "days to hours":
            return value * 24
        
if category == "Length":
    units = st.selectbox("📏Select Conversation", ["miles to kilometers","kilometer to miles" ])   
elif category == "Weight":
    units = st.selectbox("📍Select Conversation", ["kilogram to pound","pounds to kilograms"])        
elif category == "Time":
    units = st.selectbox("⏰Select Conversation", ["seconds to minutes", "minutes to seconds", "minutes to hours", "hours to minutes", "hours to day", "days to hours"])

value = st.number_input("Enter the value to convert ") 

if st.button("Convert"):
    result = convert_units(category, value, units)
    st.success(f"The result is: {result:.2f} ")
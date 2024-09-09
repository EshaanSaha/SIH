import streamlit as st
import joblib

# Load the trained ML model
model = joblib.load('best_hospital_bed_availability_model.pkl')

# Initialize session state to track conversation flow
if 'step' not in st.session_state:
    st.session_state['step'] = 0


# Normalize user input to handle upper and lower case inputs
def normalize_input(text):
    return text.strip().lower()


# Define the function to get features (ensure 8 features)
def get_features():
    # Create a list of 8 features. Start with zeros and replace with user inputs.
    features = [0] * 8
    features[0] = int(st.session_state['icu'])
    features[1] = int(st.session_state['emergency'])
    features[2] = int(st.session_state['ambulance'])

    # Add more dummy values for the remaining 5 features. You can adjust this logic
    # to incorporate real features as needed.
    features[3] = 1  # Example: You could replace this with actual user input
    features[4] = 0
    features[5] = 1
    features[6] = 0
    features[7] = 1

    return features


# Define chatbot flow with steps
def chatbot():
    # Step 0: Greet the user and ask to start
    if st.session_state['step'] == 0:
        st.write("🤖: Hello! Welcome to the Hospital Bed Booking System. Type **start** to begin.")
        user_input = st.text_input("You:", key='start_input')

        if normalize_input(user_input) == "start":
            st.session_state['step'] = 1

    # Step 1: Ask if the user needs an ICU bed
    elif st.session_state['step'] == 1:
        st.write("🤖: Do you need an ICU bed? (yes/no)")
        user_input = st.text_input("You:", key='icu_input')

        if normalize_input(user_input) in ['yes', 'no']:
            st.session_state['icu'] = normalize_input(user_input) == 'yes'
            st.session_state['step'] = 2

    # Step 2: Ask if emergency services are needed
    elif st.session_state['step'] == 2:
        st.write("🤖: Do you need emergency services? (yes/no)")
        user_input = st.text_input("You:", key='emergency_input')

        if normalize_input(user_input) in ['yes', 'no']:
            st.session_state['emergency'] = normalize_input(user_input) == 'yes'
            st.session_state['step'] = 3

    # Step 3: Ask if ambulance services are needed
    elif st.session_state['step'] == 3:
        st.write("🤖: Do you need an ambulance service? (yes/no)")
        user_input = st.text_input("You:", key='ambulance_input')

        if normalize_input(user_input) in ['yes', 'no']:
            st.session_state['ambulance'] = normalize_input(user_input) == 'yes'
            st.session_state['step'] = 4

    # Step 4: Ask how many beds are needed
    elif st.session_state['step'] == 4:
        st.write("🤖: How many beds do you need? (Choose a number from 1 to 100)")
        st.session_state['beds_needed'] = st.slider('Number of Beds Needed', min_value=1, max_value=100)

        if st.button('Next'):
            st.session_state['step'] = 5

    # Step 5: Check availability based on user input
    elif st.session_state['step'] == 5:
        st.write("🤖: Checking bed availability...")
        features = get_features()
        prediction = model.predict([features])

        if prediction[0]:
            st.write("🤖: Yes, beds are available! You can book at Hospital XYZ. Call: **+91-1234567890**")
        else:
            st.write("🤖: Sorry, no beds are available right now.")

        st.session_state['step'] = 6

    # Step 6: Offer to check OPD queue
    elif st.session_state['step'] == 6:
        st.write("🤖: Would you like to check the OPD queue? (yes/no)")
        user_input = st.text_input("You:", key='opd_input')

        if normalize_input(user_input) in ['yes', 'no']:
            st.session_state['opd_queue'] = normalize_input(user_input) == 'yes'
            st.session_state['step'] = 7

    # Step 7: Display OPD queue information
    elif st.session_state['step'] == 7:
        if st.session_state['opd_queue']:
            st.write("🤖: There are 5 patients ahead of you in the OPD queue.")
        else:
            st.write("🤖: You chose not to check the OPD queue.")

        st.write("🤖: Thank you for using the Hospital Bed Booking System!")


# Run the chatbot function
chatbot()

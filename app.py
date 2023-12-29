import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import nltk
import time
nltk.download('punkt')
import streamlit as st
import pandas as pd
import requests
from youtubesearchpython import VideosSearch
from youtubesearchpython import VideosSearch
import hashlib
import inspect
import os

#Setting the page configuration to wide
st.set_page_config(layout="wide")

tabs = option_menu(None, ['Home', 'App', 'Contact', 'About'],
                        icons=['house', 'code', 'inbox', "info"],
                        menu_icon="menu",
                        default_index=0,
                        orientation="horizontal",
                        styles={
        "container": {"padding": "0", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link-selected": {"background-color": "green"},
    }
)

if tabs == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("")
        st.title("Welcome to Scrumptious Suggestions! ")
        st.subheader("A Recipe Recommendation Website")
        st.markdown("Scrumptious Suggestions is a data powered website that suggests it's users the best recipes based on their input ingredients.")
        
        # Function for calculating likes
        def get_code_hash(code):
            return hashlib.sha256(code.encode()).hexdigest()
        
        def init_session_state():
            return {"like_count": 0}
        
        def update_like_count(session_state):
            session_state["like_count"] += 1

        # Function to persist and retrieve like count from a file
        def save_like_count(like_count):
            with open("like_count.txt", "w") as file:
                file.write(str(like_count))

        def load_like_count():
            if os.path.exists("like_count.txt"):
                with open("like_count.txt", "r") as file:
                    return int(file.read())
            else:
                return 0

        # Get session state
        session_state_key = get_code_hash(inspect.getsource(init_session_state))
        session_state = st.session_state.get(session_state_key, None)

        if session_state is None:
            st.session_state[session_state_key] = init_session_state()
            session_state = st.session_state[session_state_key]

        # Load the like count from the file
        session_state["like_count"] = load_like_count()

        if st.button("❤️ Press this button if you like this App!"):
            update_like_count(session_state)

        # Save the like count to the file
        save_like_count(session_state["like_count"])

        st.write(f"Likes: {session_state['like_count']}")

    with col2:

        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        
        lottie_animation_1 = load_lottieurl("https://lottie.host/ed4cab71-5041-4e7e-804d-33a3f55bc0db/cwBBK3i06y.json")
        st_lottie(lottie_animation_1, key="animation")   

elif tabs == "App":

    # Define the function to get recipes
    def get_recipes(ingredients, cuisine=None, course=None, diet=None):
        app_id = '09355a57' 
        app_key = '0a948ead539ccc4a9b35fbbf06ca98d1'  

        api_url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredients, app_id, app_key)
        if cuisine:
            api_url += '&cuisineType=' + ','.join(cuisine)
        if course:
            api_url += '&mealType=' + ','.join(course)
        if diet:
            api_url += '&health=' + ','.join(diet)

        result = requests.get(api_url)
        data = result.json()
        
        # Ensure that 'hits' is a list and is not empty
        if 'hits' in data and isinstance(data['hits'], list) and data['hits']:
            return [item.get('recipe', {}) for item in data['hits']]
        else:
            return []
    
    st.title("Scrumptious Suggestions")

    col1, col2 = st.columns(2)
    with col1:

        df = pd.read_excel("Ingredients.xlsx")
        ingredients_options = df["Ingredients"].tolist()

        # Multiselect widgets for ingredients, cuisine, course, and diet
        ingredients = st.multiselect("Select Ingredients (Maximum 5)", options=ingredients_options, key="ingredients")
        cuisine_options = ["American", "British", "Caribbean", "Chinese", "French", "Indian", "Italian", "Japanese", "Mexican"]
        cuisine = st.multiselect("Select your desired Cuisine(s)", options=cuisine_options, key="cuisine")
        course_options = ["Breakfast", "Dinner", "Lunch", "Snack"]
        course = st.multiselect("Select your desired Course(s)", options=course_options, key="course")
        st.markdown('')
        generate = st.button("Press to generate some Scrumptious Suggestions!")

    with col2:

        def load_lottieurl(url:str):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()
        lottie_animation_2 = load_lottieurl("https://lottie.host/d53bbe90-0df9-45fa-9c45-9f9ebd1137fd/2wHmxzetr4.json")
        st_lottie(lottie_animation_2, key="animation1")  

    if generate:

        #creating the toast for the load time
        st.toast('Gathering ingredients...')
        time.sleep(1.5)
        st.toast('Cooking...')
        time.sleep(1.5)
        st.toast('Ready!', icon="🍴")

        if len(ingredients) > 5:
            st.warning("Please select a maximum of 5 ingredients.")
        else:
            ingredients_str = ",".join(ingredients)
            recipes = get_recipes(ingredients_str, cuisine, course)

            if recipes:
                st.markdown(" ### Expand each of the suggested recipes to know more about them!")
                st.markdown('')

                # Display the recipes using expander feature
                for recipe in recipes:

                    with st.expander(f"{recipe.get('label')}"):

                        col1, col2 = st.columns([0.5,2])
                        with col1:

                            st.image(recipe.get('image'), width=200)
                        with col2:

                            st.subheader(f"{recipe.get('label')}")                    
                            st.write(f"Recipe URL: {recipe.get('url')}")
                            video_search = VideosSearch(recipe.get('label'), limit=1)
                            youtube_url = video_search.result()['result'][0]['link']
                            st.write(f"Recipe YouTube URL: {youtube_url}")
            else:
                st.markdown("### Please select some other inputs!")
                            
elif tabs == "Contact":

    col1, col2 = st.columns(2)
    with col1:

        st.title("Contact me! ")
        st.markdown("### Fill out the form to contact me.")

        def load_lottieurl(url:str):

            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation_3 = load_lottieurl("https://lottie.host/652c155f-956b-4769-8cb4-9e2867289bc0/yqr0IALkyn.json")
        st_lottie(lottie_animation_3, key="animation1")   
    
    with col2:

        st.title(" ")
        #Defining the form fields
        with st.form('Contact Form'):
            name = st.text_input('Name')
            email = st.text_input('Email')
            number = st.text_input('Phone Number')
            message = st.text_area('Message')
            submit_button = st.form_submit_button(label='Submit')

        #Processing the form submission
        if submit_button:

            print(f'Name: {name}')
            print(f'Email: {email}')
            print(f'Phone Number : {number}')
            print(f'Message: {message}')
            st.success('Thank you for reaching out to me. I will get back to you as soon as possible.')
            st.balloons()

elif tabs == "About":

    st.title("About Scrumptious Suggestions")
    st.subheader("A deeper dive into the project!")

    st.markdown("#### Description")
    st.markdown("This recipe recommendation system is an easy-to-use tool for users who are looking for recipes with specific ingredients that they have. When a user enters a maximum of five food ingredients, the system then takes those ingredients entered by the user and then generates a list of recipes.")    
    
    st.markdown("#### Motivation")
    st.markdown("In today's fast-paced world, individuals often find themselves with limited time and a desire for convenient yet delicious meals. This project aims to address the common challenge of deciding what to cook based on the ingredients readily available in the kitchen. By offering a user-friendly platform for generating recipes with specific ingredients, the system encourages creativity in the kitchen, reduces food waste, and promotes a more enjoyable cooking experience.")    
    
    st.markdown("#### Goal")
    st.markdown("The primary goal is to simplify the often daunting task of deciding what to cook based on available ingredients, fostering culinary creativity, reducing food waste, and ultimately enhancing the overall cooking experience.")

    st.markdown("#### Connect with me")
    linkedin_button = '<a href="https://www.linkedin.com/in/tulipaggarwal/" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #0077B5; text-decoration: none">LinkedIn</a>'
    github_button = '<a href="https://github.com/TulipAggarwal" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #24292E; text-decoration: none">GitHub</a>' 
    st.markdown("Connect with me on my socials - " f'{linkedin_button}{github_button} ', unsafe_allow_html=True

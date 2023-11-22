import streamlit as st
import pandas as pd
import joblib
from datetime import datetime


def write_project_info():

    st.write("## Youth Employment Prediction using Machine Learning")

    st.write("""
    Predicting youth employment based on data from labour market surveys in South Africa
    """)

    st.image("images/web_cover.jpeg")

    st.write("""
    ## About

    <p align="justify">Youth unemployment and under-employment is a major concern for any developing country, and serves as an important predictor of economic health and prosperity. Being able to predict, and understand, which young people will find employment and which ones will require additional help, helps promote evidence-based decision-making, supports economic empowerment, and allows young people to thrive in their chosen careers. <br />
    The objective of this challenge is to build a machine learning web app that predicts youth employment, based on data from labour market surveys in South Africa. Everything you need to know regarding this
    project including the documentation, notebook, dataset, evaluation metric, models etc. can be found in my repository on <a href="https://github.com/Oyebamiji-Micheal/Youth-Income-Prediction-Challenge-API/" target="_blank" style="text-decoration: None">Github</a>.</p>
    """, unsafe_allow_html=True)

    st.write("""
    **Made by Oyebamiji Micheal**
    """)


def take_user_inputs():
    st.sidebar.header("User Input Features")

    survey_date_default = datetime.strptime("02-12-2022", "%d-%m-%Y").date()
    survey_date = st.sidebar.date_input("Survey Date", value=survey_date_default, format="DD-MM-YYYY")

    survey_round = st.sidebar.slider("Survey Round", min_value=1, max_value=4)

    status = st.sidebar.selectbox("Prior Employment Status", ("Studying", "Unemployed", "Wage Employed", "Self Employed", "Employment Programme", "Wage and Self Employed", "Other"))

    tenure = st.sidebar.number_input("Prior Employment Tenure (Days)", step=1.0, min_value=0.0, max_value=22000.0)

    geography = st.sidebar.selectbox("Geography", ("Suburb", "Rural", "Urban"))

    province = st.sidebar.selectbox("Province", ("Mpumalanga", "North West", "Free State", "Eastern Cape", "Limpopo", "KwaZulu-Natal", "Gauteng", "Western Cape", "Northern Cape"))

    matric = st.sidebar.number_input(
        "Matric: Enter 1 if you were matriculated and 0 otherwise", min_value=0, max_value=1
    )

    degree = st.sidebar.number_input(
        "Degree: Enter 1 if you have a degree and 0 otherwise", min_value=0, max_value=1
    )

    diploma = st.sidebar.number_input(
        "Diploma: Enter 1 if you have a diploma and 0 otherwise", min_value=0, max_value=1
    )

    school_quantile = st.sidebar.number_input(
        "School Quantile: Enter School Quantile Ranking", min_value=0, max_value=5
    )

    additional_lang = st.sidebar.selectbox("Additional Language", ("50 - 59 %", "40 - 49 %", "60 - 69 %", "70 - 79 %", "30 - 39 %", "80 - 100 %"))

    gender = st.sidebar.number_input(
        "Gender: Male corresponds to 0 while 1 corresponds to Female", min_value=0, max_value=1
    )

    sa_citizen = st.sidebar.number_input(
        "Citizenship: Enter 1 if you are South African otherwise 0", min_value=0, max_value=1
    )

    birth_year = st.sidebar.number_input(
        "Birth Year", min_value=1950, max_value=2010, step=1
    )

    birth_month = st.sidebar.number_input(
        "Birth month", min_value=1, max_value=12, step=1
    )

    # Format certain inputs
    survey_date = survey_date.strftime("%Y-%m-%d")
    status = status.lower()

    single_input = {
        "Survey_date": survey_date,
        "Round": survey_round,
        "Status": status.lower(),
        "Tenure": tenure,
        "Geography": geography,
        "Province": province,
        "Matric": matric,
        "Degree": degree,
        "Diploma": diploma,
        "Schoolquintile": school_quantile,
        "Additional_lang": additional_lang,
        "Female": gender,
        "Sa_citizen": sa_citizen,
        "Birthyear": birth_year,
        "Birthmonth": birth_month,
    }

    return single_input


def simple_fe(df):
    # Perform a simple feature engineering 
    df["Year_survey"] = pd.to_datetime(df["Survey_date"]).dt.year # Extract year from survey date
    df["Age_survey"] = df["Year_survey"] - df["Birthyear"] # Extract age from survey year
    
    df = df.drop(columns=["Survey_date"])
    
    return df
    

def predict_input(single_input):
    input_df = pd.DataFrame([single_input]) # Convert input into a pandas dataframe

    model = joblib.load("../model/youth_income_pred.joblib") # Load model
    column_transformer = model["col_transformer"] # Load saved column transformer 
    classifier =  model["classifier"] # Load trained classifier

    input_df = pd.DataFrame([single_input]) # Convert input into a Pandas Dataframe
    
    input_df = simple_fe(input_df) # Perform a simple feature engineering

    x_input = column_transformer.transform(input_df) # Perform data preprocessing on input data
    
    prediction = classifier.predict(x_input) # Make Prediction on user input
        
    return prediction[0]


if __name__ == "__main__":
    write_project_info()

    user_input = take_user_inputs()

    predict_employment_status = st.button("Predict Employee Status")

    if predict_employment_status:
        prediction = predict_input(user_input)
        
        mapping = {0: "Unemployed", 1: "Employed"}
        st.write("Model = LightGBM")

        st.write(f"Predicted employee status = {mapping[prediction]}")

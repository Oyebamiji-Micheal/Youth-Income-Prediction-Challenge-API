from datetime import datetime

import pandas as pd


def format_date(input_date):
    survey_date = datetime.strptime(input_date, "%d-%m-%Y").date()
    survey_date = survey_date.strftime("%Y-%m-%d")
    
def column_mapping(df):
    mapping = {
        "survey_date": "Survey_date",
        "survey_round": "Round",
        "status": "Status",
        "tenure": "Tenure",
        "geography": "Geography",
        "province": "Province",
        "matric": "Matric",
        "degree": "Degree",
        "diploma": "Diploma",
        "school_quantile": "Schoolquintile",
        "additional_lang": "Additional_lang",
        "gender": "Female",
        "sa_citizen": "Sa_citizen",
        "birth_year": "Birthyear",
        "birth_month": "Birthmonth"
    }

    df = df.rename(columns=mapping)

    return df 


def simple_fe(df):
    # Perform a simple feature engineering 
    df["Year_survey"] = pd.to_datetime(df["Survey_date"]).dt.year # Extract year from survey date
    df["Age_survey"] = df["Year_survey"] - df["Birthyear"] # Extract age from survey year
    
    df = df.drop(columns=["Survey_date"])
    
    return df


def preprocess_input(input_dictionary):
    survey_date = format_date(input_dictionary["survey_date"])

    input_dictionary["survey_date"] = survey_date


    df = pd.DataFrame([input_dictionary])

    df = column_mapping(df)

    df = simple_fe(df)

    return df

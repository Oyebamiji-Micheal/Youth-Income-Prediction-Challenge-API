from pydantic import BaseModel


class YouthData(BaseModel):
    survey_date: str
    survey_round: int
    status: str 
    tenure: int
    geography: str
    province: str
    matric: int
    degree: int
    diploma: int
    school_quantile: int 
    additional_lang: str
    gender: int
    sa_citizen: int 
    birth_year: int 
    birth_month: int

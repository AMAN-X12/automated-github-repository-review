from pydantic import BaseModel


class ReviewFinding(BaseModel):
    file : str
    line : int 
    severity : str
    category:str
    explanation : str
    sugestion : str
    
class ReviewResult(BaseModel):
    findings : list[ReviewFinding]
    

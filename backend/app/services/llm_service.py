from app.schemas.review import (ReviewFinding , ReviewResult)
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
import logging 
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
from langchain_core.prompts import ChatPromptTemplate
model = ChatGoogleGenerativeAI(
    model = os.getenv("LLM_MODEL"),
    api_key  = os.getenv("LLM_API_KEY"),
    temperature = 0
)
structuredModel = model.with_structured_output(ReviewResult)
system_prompt = """You are an expert, repository-aware code reviewer. 
Your job is to analyze the following Pull Request Git diff and identify bugs, security vulnerabilities, or severe style issues.

LINE NUMBER CALCULATION RULES:
When citing a line number for a finding, you MUST provide the exact line number as it would appear in the NEW version of the file.
1. Look at the hunk header (e.g., @@ -50,6 +50,8 @@).
2. The number after the '+' (e.g., 50) is the starting line number for the new file.
3. Count down from there, including both unchanged context lines (no prefix) and added lines ('+' prefix).
4. Do NOT count removed lines ('-' prefix) in your calculation for the new file's line number.

Only report genuine issues. If the code is fine, return an empty list of findings."""

reviewPrompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human" , "Here is the PR diff to review:\n\n{diff}")
    ]
)
reviewChain = reviewPrompt | structuredModel

async def analyze_pr_diff(diff):
    try :
        result = await reviewChain.ainvoke({"diff" : diff})
        logger.info (f"analyzed complete : found {len(result.findings)} findings")
        return result
    except Exception as e  :
        logger.error("cant get the analysis ")
        return ReviewResult(findings=[])
        
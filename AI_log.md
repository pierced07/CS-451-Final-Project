## This is my log document detailing my use of AI for this project
----------------------------------------------
AI Log Entry #[2]
----------------------------------------------
Date: 2026-04-02
Tool: LLM Assistant (Qwen)
Used by: [Your Name]
Phase: EDA / Debugging / Project Planning
PURPOSE:
Completed EDA visualizations for Milestone 2, resolved a 
TypeError when calculating mean on string target variable, 
interpreted counterintuitive SMS reminder results, and 
planned next steps for repository documentation and modeling.
PROMPT:
Multiple prompts including: "how long does our presentation 
have to be", "[pasted TypeError traceback]", "i'm not sure 
this is correct. this is the graph i get. [uploaded image]", 
"ok i've finished with the visualizations. now what?"
AI OUTPUT (Summary):
1) Confirmed 10-min presentation + 3-min Q&A requirement. 
2) Identified TypeError cause: 'No-show' column contained 
strings ('Yes'/'No'); provided fix: map({'Yes':1,'No':0}). 
3) Explained selection bias: SMS reminders sent to high-risk 
patients, not randomly assigned; graph is correct. 
4) Provided README.md template, Git commands, and modeling 
notebook starter code for Milestone 3.
YOUR ACTION:
1) Added target variable conversion to numeric at start of 
EDA notebook and in cleaning.py. 
2) Kept Figure 5 (SMS effectiveness) and will document 
selection bias explanation in IEEE report Sections 4 & 7. 
3) Will update README.md with provided template and commit 
all EDA work to GitHub. 
4) Will begin 02_Modeling.ipynb for Milestone 3 checkpoint.
FINAL RESULT:
EDA notebook runs successfully with 8 visualizations saved 
to report/figures/. Target variable properly encoded for 
modeling. Repository documentation prepared. Project on 
track for Milestone 3 (Apr 8) and Stage 5 reproducibility 
requirements.
----------------------------------------------
AI Log Entry #1
----------------------------------------------
Date: 2026-03-30
Tool: LLM Assistant (Qwen3.5-Plus)
Used by: [Your Name]
Phase: Planning
PURPOSE:
Requested initial project kickoff plan for CS 451/551 final 
project: IVX Health no-show prediction.
PROMPT:
"I'm working on a final project for my data science class. 
here are the related documents... how should i get started"
AI OUTPUT (Summary):
Provided step-by-step kickoff plan: (1) Align proposal with 
requirements (Tableau→Streamlit, verify data sources), 
(2) Setup Git repo + IEEE LaTeX template, (3) Start EDA 
notebook for Milestone 2, (4) Begin AI Usage Log. Warned 
about Brazilian vs. US data mismatch.
YOUR ACTION:
Adopted Streamlit for deployment compliance. Initialized 
GitHub repo with modular structure. Downloaded Brazilian 
appointment CSV. Started AI_Log.md. Will clarify geographic 
limitations in report.
FINAL RESULT:
Project foundation established. Repository structure 
aligned with Stage 5 reproducibility requirements. Data 
strategy finalized (single primary dataset).
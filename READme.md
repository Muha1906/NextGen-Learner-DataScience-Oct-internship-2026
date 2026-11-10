# Week 4 Capstone - Predicting Internship Selection Outcomes

## Objective
Go from raw, messy data to a working predictive model and explain it clearly to a non-technical audiance.

## Dataset
Week 1 cleaned applicants data + Week 4 simulated features:nums_skill_listed, has_portfolio, prior_hackathon_participation, statement_quality_score.

## Method
1. Cleaning -> 2. Feature prep(0/4 + one-Hot)  -> 3.Train/Test split 80/20   -> 4.Logistic Regression  ->5. Evaluation (Accuracy, Precision, Recall, Confusion Matrix)

## Key Results
  - Accuracy: 20%
  - Precision: 22.22%
  - Recall: 66.67%
  - Top Predictor: statement_quality_score, has_portfolio

##Interpretation
Accuracy is low (20%) because the 4 key feature were simulated randomly and had no real relationship with the actual selection outcome.Recall is higher (66.67%) than precision, which means the model was able
to catch many of the actual selected applicatants, but also predicted many false positives. This confirm the simulated data cannot be used for real decisions.

## How to Run:
Open the notebook in Google Colab, run all cells from top to bottom.

import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="NextGen Dashboard", layout="wide")
st.title("NextGen - Interns & Applicants Dashboard")
st.write("Program Performance Dashboard - Data from nextgen.db")

# 1. Load Data
conn = sqlite3.connect(r'D:\NextGen Intern\nextgen.db')
applicants = pd.read_sql("SELECT * FROM applicants;", conn)
interns = pd.read_sql("SELECT * FROM interns;", conn)
scores = pd.read_sql("SELECT * FROM hackathon_scores;", conn)
# 2. Domain Filter - Tumhara Asli Column: Domain Applied
domain_list = ['All'] + sorted(applicants['Domain Applied'].unique().tolist())
selected_domain = st.selectbox('Filter by Domain', domain_list)

if selected_domain != 'All':
    applicants_filtered = applicants[applicants['Domain Applied'] == selected_domain]
    interns_filtered = interns[interns['domain'] == selected_domain]
    scores_filtered = scores[scores['domain'] == selected_domain]
else:
    applicants_filtered = applicants
    interns_filtered = interns
    scores_filtered = scores

# 3. Funnel - Total Applicants vs Total Interns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applicants", len(applicants_filtered))
col2.metric("Total Interns", len(interns_filtered))
col3.metric("Completed Interns", len(interns_filtered[interns_filtered['completion_status'] == 'Completed']))
col4.metric("Avg Hackathon Score", round(scores_filtered['score'].mean(), 2) if len(scores_filtered) > 0 else 0)

# 4. Query 1 - Completed Interns per Domain
st.subheader("Completed Interns per Domain - Query 1")
query1 = """
SELECT domain, COUNT(*) AS completed_count
FROM interns
WHERE completion_status = 'Completed'
GROUP BY domain
ORDER BY completed_count DESC;
"""
result1 = pd.read_sql(query1, conn)
st.bar_chart(result1.set_index('domain'))

# 5. Query 2 - Average Score per Domain
st.subheader("Average Hackathon Score per Domain - Query 2")
query2 = """
SELECT domain, ROUND(AVG(score), 2) AS avg_score
FROM hackathon_scores
GROUP BY domain
ORDER BY avg_score DESC;
"""
result2 = pd.read_sql(query2, conn)
st.bar_chart(result2.set_index('domain'))

# 6. Query 4 - Conversion Rate
st.subheader("Conversion Rate - Applied to Completed per Domain - Query 4")
query4 = """
SELECT
    a."Domain Applied" AS domain,
    COUNT(DISTINCT a.applicant_id) AS total_applicants,
    COUNT(DISTINCT i.intern_id) AS total_completed,
    ROUND(100.0 * COUNT(DISTINCT i.intern_id) / COUNT(DISTINCT a.applicant_id), 2) AS conversion_rate_pct
FROM applicants AS a
LEFT JOIN interns AS i
    ON a.applicant_id = i.applicant_id
    AND i.completion_status = 'Completed'
GROUP BY a."Domain Applied"
ORDER BY conversion_rate_pct DESC;
"""
result4 = pd.read_sql(query4, conn)
st.dataframe(result4)
st.bar_chart(result4.set_index('domain')['conversion_rate_pct'])

# 7. Query 3 - Top 10 Leaderboard
st.subheader("Top 10 Performers Leaderboard - Query 3")
query3 = """
SELECT
    i.intern_id,
    a."Applicant Name" AS intern_name,
    i.domain,
    h.score
FROM interns AS i
JOIN hackathon_scores AS h ON i.intern_id = h.intern_id
JOIN applicants AS a ON i.applicant_id = a.applicant_id
ORDER BY h.score DESC
LIMIT 10;
"""
result3 = pd.read_sql(query3, conn)
st.dataframe(result3)

# 8. Applicants Table
st.subheader(f"Applicants - Domain: {selected_domain}")
st.dataframe(applicants_filtered)

# 9. Interns Table
st.subheader("Interns Table")
st.dataframe(interns_filtered)

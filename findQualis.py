import pandas as pd
import re
from fuzzywuzzy import fuzz, process

qualis_df = pd.read_csv('Data/qualis-capes.csv', encoding="ISO-8859-1")
similarity_memo = {}

def find_similar_journal(target_text, threshold=70):
    if target_text in similarity_memo:
        return similarity_memo[target_text] 
    
    similar_rows = []

    for _, row in qualis_df.iterrows():
        pattern = r'\s*\((PRINT|ONLINE|IMPRESSO)\)\s*'
        value = re.sub(pattern, '', row['TíTULO'])
        similarity_score = fuzz.ratio(target_text.upper(), value)
        
        # If the similarity score is above the threshold, consider it a match
        if similarity_score >= threshold:
            similar_rows.append((row['ESTRATO'], similarity_score))
    
    # Sort the results by similarity score in descending order
    similar_rows.sort(key=lambda x: x[1], reverse=True)

    if len(similar_rows) > 0:
        similarity_memo[target_text] = similar_rows[0][0]
        return similar_rows[0][0]
    return 'NF'
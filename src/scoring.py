def score_lead(lead):
    score = 0
    reasons = []
    
    if lead.employees >= 50:
        score += 25
        reasons.append("Company has 50+ employess")
        
    if lead.revenue >= 1_000_000:
        score += 25
        reasons.append("Company has significant revenue")
        
    if lead.funding >= 500_000:
        score += 25
        reasons.append("Company has external funding")
        
    if lead.industry in ["SaaS", "IT", "Software", "CyberSecurity"]:
        score += 25
        reasons.append("Industry matches target profile")
        
    probabiliy = score/100
    
    if score >= 75:
        classification = "high"
        priority = "high"
    elif score >= 50:
        classification = "medium"
        priority = "medium"
    else:
        classification = "low"
        priority = "low"
        
    return{
        "score" : score,
        "probability" : probabiliy,
        "classification": classification,
        "priority" : priority,
        "reasons": reasons
    }
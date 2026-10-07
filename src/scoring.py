from src.schemas import ICP,Lead

def score_lead(lead:Lead,icp:ICP):
    score = 0
    max_score = 0
    reasons = []
    
    if icp.industries:
        max_score += icp.industry_weight
        
        if lead.industry in icp.industries:
            score += icp.industry_weight
            reasons.append("Industry matches the ideal customer profile")

    
    if icp.countries:
        max_score += icp.country_weight

        if lead.country in icp.countries:
            score += icp.country_weight

            reasons.append("Country matches the ideal customer profile")

    
    if icp.employees_min is not None:
        max_score += icp.employees_min_weight
        if lead.employees >= icp.employees_min:
            score += icp.employees_min_weight
            reasons.append("Employee count meets the minimum requirement")

    if icp.employees_max is not None:
        max_score += icp.employees_max_weight
        if lead.employees <= icp.employees_max:
            score += icp.employees_max_weight
            reasons.append("Employee count is within the target range")

    
    if icp.revenue_min is not None:
        max_score += icp.revenue_weight
        if lead.revenue >= icp.revenue_min:
            score += icp.revenue_weight
            reasons.append("Revenue meets the minimum requirement")

    
    if icp.funding_min is not None:
        max_score += icp.funding_weight
        if lead.funding >= icp.funding_min:
            score += icp.funding_weight
            reasons.append("Funding meets the minimum requirement")

    # Budget
    if icp.budget_min is not None:
        max_score += icp.budget_weight
        if lead.budget >= icp.budget_min:
            score += icp.budget_weight
            reasons.append("Budget meets the minimum requirement")
#     score = 0
#     reasons = []
    
#     if lead.employees >= 50:
#         score += 25
#         reasons.append("Company has 50+ employess")
        
#     if lead.revenue >= 1_000_000:
#         score += 25
#         reasons.append("Company has significant revenue")
        
#     if lead.funding >= 500_000:
#         score += 25
#         reasons.append("Company has external funding")
        
#     if lead.industry in ["SaaS", "IT", "Software", "CyberSecurity"]:
#         score += 25
#         reasons.append("Industry matches target profile")

    if max_score == 0:
        return {
            "score": 0,
            "probability": 0,
            "classification": "low",
            "priority": "low",
            "reasons": [
                "No ICP criteria were configured"
            ],
            "recommended_action": (
                "Configure an ICP before scoring leads"
            )
        }

        
    probability = score/max_score if max_score > 0 else 0
    score = round(probability * 100)
    
    if score >= 75:
        classification = "high"
        priority = "high"
    elif score >= 50:
        classification = "medium"
        priority = "medium"
    else:
        classification = "low"
        priority = "low"
        
        
    if score >= 75:
        recommended_action = "Contact this lead immediately"
    elif score >= 50:
        recommended_action = "Follow up soon"
    else:
        recommended_action = "Add to nurture campaign"
        
    return{
        "score" : score,
        "probability" : probability,
        "classification": classification,
        "priority" : priority,
        "reasons": reasons,
        "recommended_action": recommended_action
    }
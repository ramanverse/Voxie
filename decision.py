def generate_verdict(deepfake_label: str, deepfake_score: float, watermark_confidence: float, forensic_results: dict = None) -> dict:
    normalized_label = deepfake_label.strip().lower()
    
    # Calculate base AI risk
    if normalized_label == 'fake':
        ai_risk = deepfake_score
    elif normalized_label == 'real':
        ai_risk = 1.0 - deepfake_score
    else:
        ai_risk = deepfake_score

    # Check for "Synthetic Perfection" from forensics
    forensic_penalty = 0.0
    forensic_msg = ""
    if forensic_results and forensic_results.get("is_suspiciously_perfect"):
        forensic_penalty = 0.25  # Add 25% risk if audio is "too perfect"
        forensic_msg = "Forensic analysis detected unnatural spectral stability (Synthetic Perfection)."

    watermark_risk = 1.0 - watermark_confidence
    
    # Calculate final risk score with aggressive forensic weighting
    # AI Risk (50%) + Watermark Risk (20%) + Forensic Penalty (30%)
    
    # If it's a high-quality AI (passing as real), the AI risk will be low.
    # We must rely on the Forensic Penalty to push it up.
    
    forensic_contribution = 0.0
    if forensic_results and forensic_results.get("is_suspiciously_perfect"):
        # If too perfect, we add a massive risk contribution (up to 40%)
        forensic_contribution = 0.40
        forensic_msg = "WARNING: Forensic analysis detected 'Synthetic Perfection'. The audio is too stable to be human."
    
    # Calculate raw risk
    raw_risk_score = (ai_risk * 0.5 + watermark_risk * 0.2 + forensic_contribution) * 100
    
    # Specific case: If AI says 100% real but NO watermark is found, add 'Unauthenticated' penalty
    if ai_risk < 0.1 and watermark_confidence < 0.2:
        raw_risk_score += 15.0
        if not forensic_msg:
            forensic_msg = "Audio lacks a Voxie watermark signature."

    risk_score = min(round(raw_risk_score, 2), 100.0)
    
    if risk_score >= 60:
        final_verdict = 'Synthetic or Heavily Tampered Audio'
        risk_level = 'High'
        explanation = f'Extreme tampering probability. {forensic_msg}'
    elif risk_score >= 30:
        final_verdict = 'Suspicious Audio'
        risk_level = 'Medium'
        explanation = f'Anomalies detected in audio biology. {forensic_msg}'
    else:
        final_verdict = 'Likely Authentic Audio'
        risk_level = 'Low'
        explanation = 'Audio is consistent with biological human speech and/or contains a valid watermark.'
        
    return {
        'final_verdict': final_verdict, 
        'risk_level': risk_level, 
        'risk_score': risk_score, 
        'explanation': explanation, 
        'ai_risk_component': round(ai_risk * 100, 2), 
        'watermark_risk_component': round(watermark_risk * 100, 2),
        'forensic_results': forensic_results
    }

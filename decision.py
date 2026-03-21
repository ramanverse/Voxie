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
    
    # High-confidence AI detection override
    if normalized_label == 'fake' and deepfake_score >= 0.9:
        return {'final_verdict': 'Synthetic Audio', 'risk_level': 'High', 'risk_score': round(ai_risk * 100, 2), 'explanation': 'AI model strongly indicates synthetic voice. Watermark presence cannot override high-confidence AI detection.', 'ai_risk_component': round(ai_risk * 100, 2), 'watermark_risk_component': round(watermark_risk * 100, 2), 'conflict_type': 'AI Override'}
    
    # Calculate final risk score with forensic penalty
    raw_risk_score = (ai_risk * 0.6 + watermark_risk * 0.3 + forensic_penalty * 0.1) * 100
    risk_score = min(round(raw_risk_score, 2), 100.0)
    
    if risk_score >= 70:
        final_verdict = 'Synthetic or Heavily Tampered Audio'
        risk_level = 'High'
        explanation = f'High tampering probability detected. {forensic_msg}'
    elif risk_score >= 40:
        final_verdict = 'Suspicious Audio'
        risk_level = 'Medium'
        explanation = f'Potential inconsistencies or synthetic markers detected. {forensic_msg}'
    else:
        final_verdict = 'Likely Authentic Audio'
        risk_level = 'Low'
        explanation = 'AI classification and watermark verification are consistent and indicate authenticity.'
        
    return {
        'final_verdict': final_verdict, 
        'risk_level': risk_level, 
        'risk_score': risk_score, 
        'explanation': explanation, 
        'ai_risk_component': round(ai_risk * 100, 2), 
        'watermark_risk_component': round(watermark_risk * 100, 2),
        'forensic_results': forensic_results
    }

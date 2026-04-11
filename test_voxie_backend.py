import os
from detector import DeepfakeDetector
from watermark import embed_watermark, detect_watermark
from decision import generate_verdict
from forensics import analyze_biological_markers
from database import init_db, save_analysis, fetch_all_history

def test_voxie_backend():
    print("--- Starting Voxie End-to-End Test ---")
    
    # 1. Initialize DB
    print("\n[1/5] Initializing Database...")
    init_db()
    if os.path.exists('voxie.db'):
        print("✅ Database initialized successfully.")
    
    # 2. Load AI Model
    print("\n[2/5] Loading AI Detector Model...")
    detector = DeepfakeDetector()
    print("✅ AI Model loaded.")

    # 3. Test Human Audio (Raman_Audio.wav)
    print("\n[3/5] Testing Human Audio (Raman_Audio.wav)...")
    human_path = 'sample_audio/Raman_Audio.wav'
    with open(human_path, 'rb') as f:
        audio_bytes = f.read()
    
    label, confidence = detector.detect(audio_bytes, suffix='.wav')
    print(f"   - AI Label: {label}")
    print(f"   - AI Confidence: {confidence:.2f}")
    
    wm_confidence = detect_watermark(human_path)
    print(f"   - Watermark Confidence (should be low): {wm_confidence:.2f}")
    
    forensic_results = analyze_biological_markers(human_path)
    print(f"   - Jitter: {forensic_results['jitter']:.4f}")
    
    verdict = generate_verdict(label, confidence, wm_confidence, forensic_results=forensic_results)
    print(f"   - Verdict: {verdict['final_verdict']}")
    print(f"   - Risk Score: {verdict['risk_score']}%")
    
    # Save to DB
    save_analysis(human_path, label, confidence, wm_confidence, verdict['risk_score'], verdict['final_verdict'], verdict['risk_level'])

    # 4. Test AI Audio (Ai_audio.wav)
    print("\n[4/5] Testing AI Audio (Ai_audio.wav)...")
    ai_path = 'sample_audio/Ai_audio.wav'
    with open(ai_path, 'rb') as f:
        ai_bytes = f.read()
    
    ai_label, ai_conf = detector.detect(ai_bytes, suffix='.wav')
    print(f"   - AI Label: {ai_label}")
    print(f"   - AI Confidence: {ai_conf:.2f}")
    
    ai_wm_conf = detect_watermark(ai_path)
    print(f"   - Watermark Confidence (should be low): {ai_wm_conf:.2f}")
    
    ai_forensic = analyze_biological_markers(ai_path)
    print(f"   - AI Jitter: {ai_forensic['jitter']:.4f}")
    
    ai_verdict = generate_verdict(ai_label, ai_conf, ai_wm_conf, forensic_results=ai_forensic)
    print(f"   - Verdict: {ai_verdict['final_verdict']}")
    print(f"   - Risk Score: {ai_verdict['risk_score']}%")
    
    save_analysis(ai_path, ai_label, ai_conf, ai_wm_conf, ai_verdict['risk_score'], ai_verdict['final_verdict'], ai_verdict['risk_level'])

    # 5. Test Watermark Embedding
    print("\n[5/5] Testing Watermark Embedding & Verification...")
    temp_wm_path = 'sample_audio/temp_watermarked.wav'
    embed_watermark(human_path, temp_wm_path)
    new_wm_conf = detect_watermark(temp_wm_path)
    print(f"   - Watermark Confidence after embedding: {new_wm_conf:.2f}")
    
    if new_wm_conf >= 0.7:
        print("✅ Watermark system functional.")
    else:
        print("❌ Watermark system failure.")

    # Cleanup
    if os.path.exists(temp_wm_path):
        os.remove(temp_wm_path)
    
    print("\n--- Test Completed Successfully ---")

if __name__ == "__main__":
    test_voxie_backend()

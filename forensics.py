import numpy as np
import librosa
from typing import Dict, Any

def analyze_biological_markers(audio_path: str) -> Dict[str, Any]:
    """
    Analyzes audio for 'biological' vs 'synthetic' markers.
    Returns a dictionary of forensic scores.
    """
    y, sr = librosa.load(audio_path, sr=16000)
    
    # 1. Pitch Jitter (Frequency Variation)
    # Human speech has natural micro-fluctuations (jitter). AI is often too stable.
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    jitter_score = 0.0
    if len(pitch_values) > 1:
        # Standard deviation of pitch normalized by mean
        jitter_score = np.std(pitch_values) / np.mean(pitch_values)
    
    # 2. Spectral Centroid Variance (Timbre Stability)
    # AI voices often have unnatural 'flatness' in their spectral centroid.
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    centroid_variance = np.std(spectral_centroids) / np.mean(spectral_centroids)
    
    # 3. Harmonics-to-Noise Ratio (HNR) - Approximation
    # AI-generated speech often has lower noise levels than natural human speech.
    stft = np.abs(librosa.stft(y))
    harmonic_energy = np.sum(stft[:int(stft.shape[0]/2)])
    noise_energy = np.sum(stft[int(stft.shape[0]/2):])
    hnr_proxy = harmonic_energy / (noise_energy + 1e-6)

    # Scoring Logic:
    # Natural human speech jitter_score is typically between 0.01 and 0.05.
    # If jitter is extremely low (< 0.008), it's highly likely to be synthetic.
    is_synthetic_hint = False
    if jitter_score < 0.01 or hnr_proxy > 15.0:
        is_synthetic_hint = True
        
    return {
        "jitter": float(jitter_score),
        "spectral_variance": float(centroid_variance),
        "hnr_proxy": float(hnr_proxy),
        "biological_confidence": float(1.0 - jitter_score if jitter_score < 0.1 else 0.5),
        "is_suspiciously_perfect": is_synthetic_hint
    }

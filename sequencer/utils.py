# sequencer/utils.py
# Bu dosya, MIDI ve frekans dönüşümleri gibi yardımcı fonksiyonları içerir

import math

def midiToFreq(midiNote):
    """MIDI tuş numarasından frekans değerine dönüşüm fonksiyonu
    
    Args:
        midiNote: MIDI nota numarası (0-127)
    
    Returns:
        float: Frekans değeri (Hz)
    """
    # A4 (MIDI nota 69) = 440 Hz referans alınarak hesaplama yapılır
    # Her yarım ton için frekans, 2^(1/12) çarpanı ile değişir
    return 440 * (2 ** ((midiNote - 69) / 12))

def freqToMidi(freq):
    """Frekans değerinden en yakın MIDI tuş numarasına dönüşüm
    
    Args:
        freq: Frekans değeri (Hz)
    
    Returns:
        int: En yakın MIDI nota numarası (0-127)
    """
    if freq <= 0:
        return 0
    
    # Logaritmik ölçekte frekansı MIDI notasına dönüştürme
    # A4 (440 Hz) = MIDI 69 referans alınır
    midiFloat = 69 + 12 * math.log2(freq / 440)
    midiNote = round(midiFloat)
    
    # MIDI sınırlarını koru (0-127)
    return max(0, min(127, midiNote))

def getNoteName(midiNote):
    """MIDI nota numarasından nota ismini döndürür
    
    Args:
        midiNote: MIDI nota numarası (0-127)
    
    Returns:
        str: Nota ismi (örn. "C4", "A#5")
    """
    # Nota isimleri dizisi (C majör gamı baz alınır)
    noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # MIDI nota numarasından oktav ve nota indeksini hesapla
    noteIdx = midiNote % 12             # 0-11 arası değer (12 nota)
    octave = midiNote // 12 - 1         # Oktav numarası (MIDI 0 = oktav -1)
    
    # Nota ismi ve oktav numarasını birleştir
    return f"{noteNames[noteIdx]}{octave}"
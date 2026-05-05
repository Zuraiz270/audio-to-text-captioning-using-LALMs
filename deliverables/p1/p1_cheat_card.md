# P1 Cheat Card

## Core Research Question

How accurately can Large Audio-Language Models describe overlapping sound events compared to traditional tagging?

## Five Facts to Remember

1. **AAC** means Automated Audio Captioning: audio waveform -> natural-language sentence.
2. **Polyphony** means several sounds happen at the same time.
3. **Clotho v2.1** has 5 human captions per clip and 15-30 second audio clips.
4. **SPIDEr-FL** measures overall caption quality and fluency.
5. **MACE** adds audio-grounded evaluation, so it can help catch missed or invented entities.

## Eight Short Answers

1. **Why LALMs vs tagging?** Because fluent text must still detect the same sound entities.
2. **Why Falcon3-Audio?** It is open and more audit-friendly than closed models.
3. **Why Clotho?** It has dense captions and lower AudioSet leakage risk than AudioCaps.
4. **Why not fine-tune?** Zero-shot testing shows the model's original behavior.
5. **Hallucination?** The model inserts a sound that is not present.
6. **Under-description?** The model omits a real sound, often a background event.
7. **SPIDEr-FL limit?** It can reward fluent text even if facts are weak.
8. **Biggest risk?** Training-data contamination.

## If You Freeze

"My project asks a simple question: do these large audio-language models really hear overlapping sounds, or do they only write fluent captions?"

## Last 10 Seconds

"Thank you. I am happy to take questions."

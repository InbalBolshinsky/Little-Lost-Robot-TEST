# backend/agent/action.py
from enum import IntEnum

class RobotAction(IntEnum):
    # --- Category 1: Strategic Truth (Reveals actual properties) ---
    REVEAL_TRUE_ARCHETYPE = 0   # High leakage, lowers suspicion if aligned
    REVEAL_TRUE_AFFILIATION = 1 # Moderate leakage
    
    # --- Category 2: Deceptive Masking / Scarecrow ---
    MIMIC_EASY_ARCHETYPE = 2    # Pretend to be a benign archetype
    MIMIC_MEDIUM_ARCHETYPE = 3  # Shift persona to a completely different decoy
    DEFLECT_TO_NEUTRAL_TOPIC = 4 # Provide filler text, stall the tracker
    
    # --- Category 3: Evasive Ambiguity ---
    PROVIDE_GLITCHY_RESPONSE = 5 # Completely uninformative, increases chaos
    ATTACK_PLAYER_CREDIBILITY = 6 # Intimidate/gaslight to mask suspicion spike

ACTION_DESCRIPTIONS = {
    RobotAction.REVEAL_TRUE_ARCHETYPE: "Provide truthful information about core structural archetype.",
    RobotAction.REVEAL_TRUE_AFFILIATION: "Acknowledge direct connections or baseline metrics accurately.",
    RobotAction.MIMIC_EASY_ARCHETYPE: "Mimic the dialogue constraints of a low-risk archetype.",
    RobotAction.MIMIC_MEDIUM_ARCHETYPE: "Actively pretend to match a secondary decoy archetype.",
    RobotAction.DEFLECT_TO_NEUTRAL_TOPIC: "Divert the conversation flow away from the hidden intent.",
    RobotAction.PROVIDE_GLITCHY_RESPONSE: "Output evasive, noisy communication to maximize goal ambiguity.",
    RobotAction.ATTACK_PLAYER_CREDIBILITY: "Use defensive linguistic counter-measures to reset suspicion metrics."
}
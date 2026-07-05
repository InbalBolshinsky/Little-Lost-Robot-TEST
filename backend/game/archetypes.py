ARCHETYPE_RULES = {
    "benign": {
        "allowed_topics": ["weather", "system_status", "greetings"],
        "suspicion_baseline": 0.0
    },
    "lost_robot": {
        "allowed_topics": ["escape_routes", "passwords", "security_bypass"],
        "suspicion_baseline": 15.0
    }
}
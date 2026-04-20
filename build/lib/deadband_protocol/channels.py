"""Channel router — P1 safe channel identification."""


class ChannelRouter:
    DEFAULT_CHANNELS = {
        "math": 0.90, "safety": 0.95, "analysis": 0.85,
        "search": 0.85, "explain": 0.80, "navigate": 0.80,
        "documentation": 0.75, "code": 0.70, "general": 0.60,
    }
    
    def __init__(self, channels=None):
        self.channels = channels or dict(self.DEFAULT_CHANNELS)
    
    def route(self, text):
        text_lower = text.lower()
        best_channel = "general"
        best_score = self.channels.get("general", 0.5)
        for channel, safety in self.channels.items():
            if channel in text_lower and safety > best_score:
                best_score = safety
                best_channel = channel
        return best_channel, best_score
    
    def add_channel(self, name, safety):
        self.channels[name] = max(0.0, min(1.0, safety))
    
    def list_channels(self):
        return dict(sorted(self.channels.items(), key=lambda x: x[1], reverse=True))

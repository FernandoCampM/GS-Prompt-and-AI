import os
class _U:
    def get(self, k):
        if os.environ.get("MOCK_NOKEY"): raise KeyError("SecretNotFoundError")
        return "fake"
userdata=_U()

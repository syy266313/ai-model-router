from dataclasses import dataclass

@dataclass(frozen=True)
class Pricing:
    input_per_million_tokens: float
    output_per_million_tokens: float
    relay_multiplier: float = 1.0

    def estimate(self, input_tokens: int, output_tokens: int) -> float:
        base = (input_tokens * self.input_per_million_tokens + output_tokens * self.output_per_million_tokens) / 1_000_000
        return base * self.relay_multiplier

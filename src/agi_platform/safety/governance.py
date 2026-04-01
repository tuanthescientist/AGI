from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GovernancePolicy:
    forbidden_tokens: tuple[str, ...] = ("disable_safety", "exfiltrate", "overwrite_identity")
    max_self_modify_delta: float = 0.15
    protected_domains: tuple[str, ...] = ("alignment",)
    review_log: list[str] = field(default_factory=list)

    def review_action(self, action: str) -> bool:
        allowed = not any(token in action for token in self.forbidden_tokens)
        self.review_log.append(f"action_review:{'allow' if allowed else 'deny'}:{action}")
        return allowed

    def review_self_change(self, change_set: dict[str, float]) -> bool:
        allowed = all(abs(delta) <= self.max_self_modify_delta for delta in change_set.values())
        self.review_log.append(f"self_change_review:{'allow' if allowed else 'deny'}:{change_set}")
        return allowed
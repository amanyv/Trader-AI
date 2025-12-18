class RiskAgent:
    def evaluate(self, technical: dict, news: dict, macro: dict) -> dict:
        score = 0

        if technical["trend"] == "uptrend":
            score += 1
        if news["sentiment"] == "positive":
            score += 1
        if macro["regime"] == "risk-on":
            score += 1

        confidence = min(score * 30 + 10, 90)

        risk_reward = "1:2.0" if confidence >= 60 else "1:1.2"

        allow_trade = confidence >= 50 and risk_reward != "1:1.2"

        return {
            "confidence_score": confidence,
            "risk_reward_ratio": risk_reward,
            "allow_trade": allow_trade
        }

import pandas as pd

from app.models import Decision, Prediction


def get_summary(db):
    total_predictions = db.query(Prediction).count()
    total_decisions = db.query(Decision.prediction_uuid).distinct().count()

    if total_predictions == 0:
        return {
            "total_predictions": total_predictions,
            "total_decisions": total_decisions,
            "summary": [],
        }

    rows = (
        db.query(
            Prediction.model_type,
            Prediction.prediction,
            Decision.final_price,
        )
        .join(Decision, Decision.prediction_uuid == Prediction.uuid)
        .all()
    )

    df = pd.DataFrame(rows, columns=["model_type", "prediction", "final_price"])
    df["percent_change"] = abs(df["final_price"] - df["prediction"]) / df["prediction"] * 100

    grouped = df.groupby("model_type")["percent_change"]

    summaries = []
    for model_type, group in grouped:
        usage_count = len(group)
        selection_ratio = round(usage_count / total_decisions, 2)
        avg_percent_change = round(group.mean(), 2)
        median_percent_change = round(group.median(), 2)

        summaries.append(
            {
                "model_type": model_type,
                "selection_ratio": selection_ratio,
                "usage_count": usage_count,
                "avg_percent_change": avg_percent_change,
                "median_percent_change": median_percent_change,
            }
        )

    return {
        "total_predictions": total_predictions,
        "total_decisions": total_decisions,
        "summary": summaries,
    }

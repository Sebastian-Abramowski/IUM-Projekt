import pandas as pd

from app.exceptions import EntityNotFoundException
from app.models import Decision, Prediction


class AbRepository:
    def __init__(self, db):
        self.db = db

    def save_prediction(self, input_data, model_type, predicted_price):
        prediction = Prediction(
            model_type=model_type,
            prediction=predicted_price,
            input_data=input_data,
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction

    def save_decision(self, prediction_uuid, final_price):
        prediction = self.db.query(Prediction).filter_by(uuid=prediction_uuid).first()
        if not prediction:
            raise EntityNotFoundException(Prediction, prediction_uuid)

        decision = Decision(
            prediction_uuid=prediction_uuid,
            final_price=final_price,
        )
        self.db.add(decision)
        self.db.commit()
        self.db.refresh(decision)

        return decision

    def get_summary(self):
        total_predictions = self.db.query(Prediction).count()
        total_decisions = self.db.query(Decision.prediction_uuid).distinct().count()

        if total_predictions == 0:
            return {
                "total_predictions": total_predictions,
                "total_decisions": total_decisions,
                "summary": [],
            }

        rows = (
            self.db.query(
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

    def clear_all(self):
        self.db.query(Prediction).delete()
        self.db.query(Decision).delete()
        self.db.commit()

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

    def clear_all(self):
        self.db.query(Prediction).delete()
        self.db.query(Decision).delete()
        self.db.commit()

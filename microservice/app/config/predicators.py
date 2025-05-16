import pickle

from pathlib import Path

from sklearn.base import BaseEstimator, TransformerMixin  # noqa: F401
from sklearn.pipeline import Pipeline

PREDICTORS = Path("predictors")


def load_model(name) -> Pipeline:
    with open(PREDICTORS / f"{name}.pkl", "rb") as fh:
        return pickle.load(fh)


dummy_model = load_model("dummy")
base_model = load_model("base")
advanced_model = load_model("forest")

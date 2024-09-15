import numpy as np
import pickle
import joblib
from api.model.preprocessor import Preprocessor


class Model:

    def __init__(self, model):
        self.model = model

    @staticmethod
    def load_model(path: str):
        """
        Loads the model from a file. Depending on whether the file
        ends with .pkl or .joblib, it is loaded differently.
        """
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                model = pickle.load(file)
        else:
            raise Exception('Unsupported file format')
        return model

    def predictor(self, x_input: np.ndarray) -> np.ndarray:
        """
        Makes a prediction based on the trained model.
        """
        return self.predict(x_input)

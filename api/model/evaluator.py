from sklearn.metrics import accuracy_score
from api.model.model import Model


class Evaluator:

    @staticmethod
    def evaluate(model, x_test, y_test) -> float:
        """
        Makes a prediction and evaluates the model. The evaluation type
        could be parameterized, among other options.
        """
        predictions = Model.predictor(model, x_test)

        # If your problem has more than two classes, adjust the 'average' parameter
        return accuracy_score(y_test, predictions)

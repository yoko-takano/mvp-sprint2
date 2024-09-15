from sklearn.model_selection import train_test_split
import pickle
import numpy as np


class Preprocessor:

    def split_train_test(self, dataset, test_size: float, seed: int = 7):
        """
        Handles all preprocessing steps.
        """
        # Data cleaning and outlier removal

        # Feature selection

        # Split into train and test sets
        x_train, x_test, y_train, y_test = self.__prepare_holdout(dataset, test_size, seed)

        # Normalization/Standardization

        return x_train, x_test, y_train, y_test

    @staticmethod
    def __prepare_holdout(dataset, test_size: float, seed: int):
        """
        Splits the data into train and test sets using the holdout method.
        Assumes that the target variable is in the last column.
        The test_size parameter specifies the percentage of data for testing.
        """
        data = dataset.values
        x = data[:, :-1]
        y = data[:, -1]
        return train_test_split(x, y, test_size=test_size, random_state=seed)

    @staticmethod
    def prepare_form(form) -> np.ndarray:
        """
        Prepares data received from the front-end to be used by the model.
        """
        x_input = np.array([
            form.mean_radius,
            form.mean_texture,
            form.mean_perimeter,
            form.mean_area,
            form.mean_smoothness,
        ])
        # Reshape to ensure the model understands that we're passing a single sample
        x_input = x_input.reshape(1, -1)
        return x_input

    @staticmethod
    def scale_data(x_train: np.ndarray) -> np.ndarray:
        """
        Normalizes the data.
        """
        scaler = pickle.load(open('./MachineLearning/scalers/min_max_scaler_breast_cancer.pkl', 'rb'))
        rescaled_x_train = scaler.transform(x_train)
        return rescaled_x_train

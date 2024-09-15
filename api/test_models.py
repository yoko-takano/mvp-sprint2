# To run: pytest -v test_models.py
from model.data_loader import DataLoader
from model.evaluator import Evaluator
from model.model import Model
from model.pipeline import Pipeline

# Class Instances
loader = DataLoader()
model = Model()
evaluator = Evaluator()

# Parameters
data_url = "./MachineLearning/data/test_dataset_breast_cancer.csv"
columns = ['mean_radius', 'mean_texture', 'mean_perimeter', 'mean_area', 'mean_smoothness']

# Load the data
dataset = DataLoader.load_data(data_url, columns)
array = dataset.values
X = array[:, 0:-1]  # Features
y = array[:, -1]  # Labels


# Method to test the Logistic Regression model from the corresponding file
# The name of the method to be tested must start with "test_"
def test_logistic_regression_model():
    # Importing the logistic regression model
    lr_path = './MachineLearning/models/rf_breast_cancer_classifier.pkl'
    logistic_regression_model = Model.load_model(lr_path)

    # Getting metrics for Logistic Regression
    logistic_regression_accuracy = Evaluator.evaluate(logistic_regression_model, X, y)

    # Testing the Logistic Regression metrics
    # Modify the metrics according to your requirements
    assert logistic_regression_accuracy >= 0.78
    # assert logistic_regression_recall >= 0.5
    # assert logistic_regression_precision >= 0.5
    # assert logistic_regression_f1 >= 0.5


# Method to test the KNN model from the corresponding file
def test_knn_model():
    # Importing the KNN model
    knn_path = './MachineLearning/models/rf_breast_cancer_classifier.pkl'
    knn_model = Model.load_model(knn_path)

    # Getting metrics for KNN
    knn_accuracy = Evaluator.evaluate(knn_model, X, y)

    # Testing the KNN metrics
    # Modify the metrics according to your requirements
    assert knn_accuracy >= 0.78
    # assert knn_recall >= 0.5
    # assert knn_precision >= 0.5
    # assert knn_f1 >= 0.5


# Method to test the Random Forest pipeline from the corresponding file
def test_random_forest_model():
    # Importing the Random Forest pipeline
    rf_path = './MachineLearning/pipelines/rf_breast_cancer_pipeline.pkl'
    random_forest_model = Pipeline.load_pipeline(rf_path)

    # Getting metrics for Random Forest
    random_forest_accuracy = Evaluator.evaluate(random_forest_model, X, y)

    # Testing the Random Forest metrics
    # Modify the metrics according to your requirements
    assert random_forest_accuracy >= 0.78
    # assert random_forest_recall >= 0.5
    # assert random_forest_precision >= 0.5
    # assert random_forest_f1 >= 0.5

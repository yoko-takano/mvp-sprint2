from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from api.model.model import Model
from api.model.patient import Patient
from api.model.pipeline import Pipeline
from api.model.preprocessor import Preprocessor
from api.schemas.error_schema import ErrorSchema
from api.schemas.patient_schema import PatientViewSchema, represent_patient, PatientSearchSchema, PatientCreateSchema, \
    represent_patients
from .logger import logger
from api.schemas import *
from flask_cors import CORS

info = Info(title="My API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc, or RapiDoc")
patient_tag = Tag(name="Patient", description="Addition, viewing, removal, and prediction of patients with Diabetes")


@app.get('/', tags=[home_tag])
def home():
    """
    Redirects to /openapi, a screen that allows choosing the documentation style.
    """
    return redirect('/openapi')


@app.get('/patients', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patients():
    """
    Lists all registered patients in the database.
    \f
    :return: list of patients registered in the database.
    """
    session = Session()

    # Retrieving all patients
    patients = session.query(Patient).all()

    if not patients:
        logger.warning("No patients registered in the database")
        return []
    else:
        logger.debug(f"{len(patients)} patients found")
        return represent_patients(patients), 200


@app.post('/patient', tags=[patient_tag],
          responses={"200": PatientViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_patient(form: PatientCreateSchema):
    """
    Adds a new patient to the database.
    \f
    :param form: Representation of a new patient to be created.
    :return: Representation of the patient and associated diagnosis.
    """

    # Retrieving data from the form
    name = form.name
    mean_radius = form.mean_radius
    mean_texture = form.mean_texture
    mean_perimeter = form.mean_perimeter
    mean_area = form.mean_area
    mean_smoothness = form.mean_smoothness

    # Preparing data for the model
    x_input = Preprocessor.prepare_form(form)

    # Loading the model
    model_path = './machine_learning/pipelines/rf_breast_cancer_pipeline.pkl'
    model = Pipeline.load_pipeline(model_path)

    # Making the prediction
    diagnosis = bool(Model.predictor(model, x_input)[0])

    patient = Patient(
        name=name,
        mean_radius=mean_radius,
        mean_texture=mean_texture,
        mean_perimeter=mean_perimeter,
        mean_area=mean_area,
        mean_smoothness=mean_smoothness,
        diagnosis=diagnosis
    )

    logger.debug(f"Adding patient with name: '{patient.name}'")

    try:
        # Creating a database session
        session = Session()

        # Checking if the patient already exists in the database
        if session.query(Patient).filter(Patient.name == form.name).first():
            error_msg = f"Patient {patient.name} already exists in the database"
            logger.warning(f"Error adding patient '{patient.name}', {error_msg}")
            return {"message": error_msg}, 409

        # Adding the patient
        session.add(patient)

        # Committing the addition
        session.commit()
        logger.debug(f"Added patient with name: '{patient.name}'")
        return represent_patient(patient), 200

    # If an error occurs during the addition
    except Exception as e:
        error_msg = f"Unable to save the new item: {str(e)}"
        logger.warning(f"Error adding patient '{patient.name}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/patient', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patient(query: PatientSearchSchema):
    """
    Searches for a registered patient in the database by name.
    \f
    :param query: Representation of a new patient to be created.
    :return: Representation of the patient and associated diagnosis.
    """
    patient_name = query.name
    logger.debug(f"Collecting data about patient #{patient_name}")

    # Creating a database session
    session = Session()

    # Performing the search
    patient = session.query(Patient).filter(Patient.name == patient_name).first()

    if not patient:
        # If the patient was not found
        error_msg = f"Patient {patient_name} not found in the database"
        logger.warning(f"Error searching for patient '{patient_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Patient found: '{patient.name}'")
        # Returns the representation of the patient
        return represent_patient(patient), 200


@app.delete('/patient', tags=[patient_tag],
            responses={"200": PatientViewSchema, "404": ErrorSchema})
def delete_patient(query: PatientSearchSchema):
    """
    Removes a registered patient from the database by name.
    \f
    :param query: Representation of the search query for a patient by name.
    :return: Representation of a patient as returned by the system
    """
    patient_name = unquote(query.name)
    logger.debug(f"Deleting data about patient #{patient_name}")

    # Creating a database session
    session = Session()

    # Searching for the patient
    patient = session.query(Patient).filter(Patient.name == patient_name).first()

    if not patient:
        error_msg = f"Patient {patient_name} not found in the database"
        logger.warning(f"Error deleting patient '{patient_name}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(patient)
        session.commit()
        logger.debug(f"Deleted patient #{patient_name}")
        return {"message": f"Patient {patient_name} successfully removed"}, 200


if __name__ == '__main__':
    app.run(debug=True)

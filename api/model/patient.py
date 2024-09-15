from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union, Any
from api.model.base import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column("Name", String(50))
    mean_radius = Column("MeanRadius", Float)
    mean_texture = Column("MeanTexture", Float)
    mean_perimeter = Column("MeanPerimeter", Float)
    mean_area = Column("MeanArea", Float)
    mean_smoothness = Column("MeanSmoothness", Float)
    diagnosis = Column("Diagnosis", Boolean, nullable=True)
    insertion_date = Column(DateTime, default=datetime.now())

    def __init__(
            self,
            name: str,
            mean_radius: float,
            mean_texture: float,
            mean_perimeter: float,
            mean_area: float,
            mean_smoothness: float,
            diagnosis: bool,
            insertion_date: Union[DateTime, None] = None,
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        Creates a Patient instance.
        \f
        :param name: Patient's name
        :param mean_radius: The average radius of cell nuclei in the sample
        :param mean_texture: The average variation in pixel intensity
        :param mean_perimeter: The average perimeter of the cell nuclei
        :param mean_area:The average area of the cell nuclei
        :param mean_smoothness: The average measure of the smoothness of the cell nuclei
        :param diagnosis: Diagnostic result, where 0 indicates benign and 1 indicates malignant breast cancer
        :param insertion_date: Date when the patient was added to the database
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.mean_radius = mean_radius
        self.mean_texture = mean_texture
        self.mean_perimeter = mean_perimeter
        self.mean_area = mean_area
        self.mean_smoothness = mean_smoothness
        self.diagnosis = diagnosis

        # If not provided, it will default to the current date and time
        self.insertion_date = insertion_date if insertion_date else datetime.now()

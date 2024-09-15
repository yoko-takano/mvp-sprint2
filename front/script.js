// Function to get the patient list from the server via GET request
const getPatientList = async () => {
    try {
        let url = 'http://127.0.0.1:5000/patients';
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch patient list');
        }

        const { patients } = await response.json();
        console.log('patients:', patients);
        renderPatientList(patients);

    } catch (error) {
        console.error('Error:', error);
        showNotification(
            "error",
            "Error loading list of Patients. Check the console for more details."
          );    
        }
};

// Function to add an Patient to the list via POST request
const postItem = async (
    name,
    mean_radius,
    mean_texture,
    mean_perimeter,
    mean_area,
    mean_smoothness,
) => {
    // Create FormData object to send data
    const formData = new FormData();
    formData.append("name", name),
    formData.append("mean_radius", mean_radius),
    formData.append("mean_texture", mean_texture),
    formData.append("mean_perimeter", mean_perimeter),
    formData.append("mean_area", mean_area),
    formData.append("mean_smoothness", mean_smoothness);

    try {
        let url = "http://127.0.0.1:5000/patient";
        // Send POST request to add new Patient
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        // Handle error if response is not ok
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message);
        }

        // If successful, log server response and refresh UI
        const data = await response.json();
        console.log("Server response:", data);

        getPatientList(); // Refresh Patient list
        showNotification(
            "success",
            "Patient created successfully!"
        )
    } catch (error) {
        // Log and show error notification
        console.error("Error sending data:", error);
        showNotification(
            "error",
            error.message ||
              "Error creating Patient. Check the console for more details."
          );
        }
    };

// Function to display alerts on the interface
const showNotification = (type, message) => {
    const notificationContainer = document.getElementById(
      "notification-container"
    );
    const notificationBox = document.createElement("div");
  
    notificationBox.className = `notification ${type}`;
    notificationBox.innerHTML = `
          ${message}
          <span class="close-btn material-icons" onclick="this.parentElement.style.display='none';">close</span>
      `;
    notificationContainer.appendChild(notificationBox);
  
    // Auto-hide notification after 5 seconds
    setTimeout(() => {
      notificationBox.classList.add("hide");
      setTimeout(() => {
        notificationBox.remove();
      }, 500);
    }, 5000);
  };

// Function to add a new patient using POST request
const newPatient = async () => {
    let name = document.getElementById("patient_name").value;
    let mean_radius = document.getElementById("mean_radius").value;
    let mean_texture = document.getElementById("mean_texture").value;
    let mean_perimeter = document.getElementById("mean_perimeter").value;
    let mean_area = document.getElementById("mean_area").value;
    let mean_smoothness = document.getElementById("mean_smoothness").value;

    try {
        // Attempt to add the new AAS
        await postItem(
            name,
            mean_radius,
            mean_texture,
            mean_perimeter,
            mean_area,
            mean_smoothness,
        );
      } catch (error) {
        console.error("Error creating Patient:", error);
        showNotification(
          "error",
          error.message || "Error adding item. Check the console for more details."
        );
      } finally {
        // Refresh the AAS list and select dropdown
        getPatientList();
      }
};

// Function to delete a patient from the server via DELETE request
const deletePatient = async (patientName) => {
    if (confirm("Are you sure you want to delete this patient?")) {
        try {
            let url = `http://127.0.0.1:5000/patient?name=${encodeURIComponent(patientName)}`;
            const response = await fetch(url, { method: 'DELETE' });
            if (!response.ok) {
                throw new Error('Failed to delete patient');
            }
            getPatientList();
            showNotification('success', 'Patient deleted successfully!');
        } catch (error) {
            console.error('Error deleting patient:', error);
            showNotification('error', 'Error.');
        }
    }
};

// Function to generate HTML for a patient card
const generatePatientCard = (patient) => {
    return `
        <div class="patient-item">
            <div class="patient-summary">
                <span>${patient.name} - Diagnosis: ${patient.diagnosis ? 'Positive' : 'Negative'}</span>
                <div class="patient-summary-buttons">
                    <button class="view-more-btn" onclick="toggleView('${patient.name}', this)">View More</button>
                    <button class="delete-btn" onclick="deletePatient('${patient.name}')">Delete</button>
                </div>
            </div>
            <div class="patient-details" id="details-${patient.name}" style="display: none;">
                <p><strong>Mean Radius:</strong> ${patient.mean_radius || ""}</p>
                <p><strong>Mean Texture:</strong> ${patient.mean_texture || ""}</p>
                <p><strong>Mean Perimeter:</strong> ${patient.mean_perimeter || ""}</p>
                <p><strong>Mean Area:</strong> ${patient.mean_area || ""}</p>
                <p><strong>Mean Smoothness:</strong> ${patient.mean_smoothness || ""}</p>
            </div>
        </div>
    `;
};

// Function to render the patient list in the DOM
const renderPatientList = (patients) => {
    const patientList = document.getElementById("patientList");
    patientList.innerHTML = '';  // Clear the current list

    patients.forEach(patient => {
        const patientCard = generatePatientCard(patient);
        patientList.innerHTML += patientCard;
    });
};

// Function to toggle between "View More" and "View Less"
const toggleView = (patientName, button) => {
    const details = document.getElementById(`details-${patientName}`);
    if (details.style.display === "none") {
        details.style.display = "block";
        button.textContent = "View Less";
    } else {
        details.style.display = "none";
        button.textContent = "View More";
    }
};


// Call the function to load the list when the page loads
getPatientList();

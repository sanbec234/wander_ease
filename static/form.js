document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("trip-form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission behavior

        const formData = new FormData(form);

        // Retrieve form data using the input field names
        const destination = formData.get("destination");
        const tourBudget = formData.get("tour-budget");
        const numDays = formData.get("num-days");

        try {
            const response = await fetch("/handle_data", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'destination': destination, 'tourBudget': tourBudget, 'numDays': numDays}),
            });

            if (response.ok) {
                // Handle successful response (e.g., show a success message)
                console.log("Form data submitted successfully!");

                // Redirect to '/spots' route upon successful submission
                window.location.href = '/spots';
            } else {
                // Handle errors (e.g., display an error message)
                console.error("Error submitting form data.");
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    });
});
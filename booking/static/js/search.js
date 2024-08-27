// Disable or enable the return date based on trip type
function toggleReturnDate(enable) {
    const returnDateInput = document.getElementById("return-date");
    if (enable) {
        returnDateInput.disabled = false;
        returnDateInput.value = ""; // Clear the value when enabled
    } else {
        returnDateInput.disabled = true;
        returnDateInput.value = "Unavailable"; // Set the value to 'Unavailable' when disabled
    }
}
// Handle airport suggestions for "FROM" field
const fromAirportInput = document.getElementById('from-airport');
const fromSuggestionsList = document.getElementById('from-airport-suggestions');
// Handle airport suggestions for "TO" field
const toAirportInput = document.getElementById('to-airport');
const toSuggestionsList = document.getElementById('to-airport-suggestions');

document.querySelector('.model-search-btn').addEventListener('click', (e) => {
    e.preventDefault();
    // Get the selected trip type
    const tripType = document.querySelector('input[name="tripType"]:checked').value;
    // Extract the airport codes from the "FROM" and "TO" fields
    const fromAirport = fromAirportInput.value;
    const toAirport = toAirportInput.value;
    // Get the departure and return dates
    const departureDate = document.getElementById('departure-date').value;
    const returnDate = document.getElementById('return-date').value;
    // Get the number of passengers and chair type
    const numPassengers = document.getElementById('num-passengers').value;
    const chairType = document.getElementById('chair-type').value;
    // Build the URL for the search request
    const url = `?tripType=${tripType}&from=${encodeURIComponent(fromAirport)}&to=${encodeURIComponent(toAirport)}&departureDate=${departureDate}&returnDate=${returnDate}&numPassengers=${numPassengers}&chairType=${chairType}`;
    // Redirect to the search URL
    window.location.href = url;
});

$(document).ready(function() {
  // Disable or enable the return date based on trip type
  $("#return-date").prop("disabled", {% if trip_type == 'oneway' %}true{% else %} false{% endif %});

  function toggleReturnDate(enable) {
      const returnDateInput = $("#return-date");
      if (enable) {
          returnDateInput.prop("disabled", false);
          returnDateInput.val(""); // Clear the value when enabled
      } else {
          returnDateInput.prop("disabled", true);
          returnDateInput.val("Unavailable"); // Set the value to 'Unavailable' when disabled
      }
  }

  var airports = JSON.parse('{{ airports|escapejs }}'); // Access airports data from Django context

  // Handle airport suggestions for "FROM" field
  $("#from-airport").on("input", function() {
      const searchTerm = $(this).val().toLowerCase();
      const filteredAirports = airports.filter(airport =>
          airport.city.toLowerCase().includes(searchTerm) ||
          airport.airport_code.toLowerCase().includes(searchTerm)
      );

      $("#from-airport-suggestions").empty();

      filteredAirports.forEach(airport => {
          const listItem = $("<li>");
          listItem.text(`${airport.city} (${airport.airport_code})`);
          listItem.click(function() {
              $("#from-airport").val(`${airport.airport_code}`);
              $("#from-airport-suggestions").empty();
          });
          $("#from-airport-suggestions").append(listItem);
      });
  });

  // Handle airport suggestions for "TO" field
  $("#to-airport").on("input", function() {
      const searchTerm = $(this).val().toLowerCase();
      const filteredAirports = airports.filter(airport =>
          airport.city.toLowerCase().includes(searchTerm) ||
          airport.airport_code.toLowerCase().includes(searchTerm)
      );

      $("#to-airport-suggestions").empty();

      filteredAirports.forEach(airport => {
          const listItem = $("<li>");
          listItem.text(`${airport.city} (${airport.airport_code})`);
          listItem.click(function() {
              $("#to-airport").val(`${airport.airport_code}`);
              $("#to-airport-suggestions").empty();
          });
          $("#to-airport-suggestions").append(listItem);
      });
  });

  $(".model-search-btn").click(function(e) {
      e.preventDefault();

      // Get the selected trip type
      const tripType = $('input[name="tripType"]:checked').val();

      // Extract the airport codes from the "FROM" and "TO" fields
      const fromAirport = $("#from-airport").val();
      const toAirport = $("#to-airport").val();

      // Get the departure and return dates
      const departureDate = $("#departure-date").val();
      const returnDate = $("#return-date").val();

      // Get the number of passengers and chair type
      const numPassengers = $("#num-passengers").val();
      const chairType = $("#chair-type").val();

      // Build the URL for the search request
      const url = `{% url 'index' %}?tripType=${tripType}&from=${encodeURIComponent(fromAirport)}&to=${encodeURIComponent(toAirport)}&departureDate=${departureDate}&returnDate=${returnDate}&numPassengers=${numPassengers}&chairType=${chairType}`;

      // Redirect to the search URL
      window.location.href = url;
  });
});

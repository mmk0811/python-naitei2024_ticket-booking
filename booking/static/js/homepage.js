let selectedDepartureFlightId = null; // Biến lưu trữ ID chuyến bay đã chọn
let selectedReturnFlightId = null;
function selectFlight(flight_type, id, departure_time, arrival_time, departure_airport, arrival_airport, ticket_type_price) {
    const flightInfoDiv = document.getElementById(flight_type);
    const bottomBarDiv = document.getElementById("selected-flight-info");
    if (flight_type === 'departure') {
        const selectedItem = event.currentTarget;

        if (selectedDepartureFlightId === id) {
        // Nếu chuyến bay đã chọn trước đó được chọn lại, ẩn khối thông tin
            flightInfoDiv.style.display = "none";
            selectedDepartureFlightId = null; // Xóa ID đã chọn
            document.getElementById("d-flight-id").innerText = "";
            selectedItem.classList.remove('selected');
        } else {
            const items = document.querySelectorAll('.d-single-item');
            items.forEach(item => item.classList.remove('selected'));
            selectedItem.classList.add('selected');
            // Nếu chọn chuyến bay mới, hiển thị khối thông tin và cập nhật nội dung
            flightInfoDiv.style.display = "inline-block";
            document.getElementById("d-flight-id").innerText = `${id}`;
            document.getElementById("d-flight-time").innerText = `${departure_time} - ${arrival_time}`;
            document.getElementById("d-flight-airports").innerText = `${departure_airport} --- ${arrival_airport}`;
            document.getElementById("d-flight-price").innerText = `${ticket_type_price}`;
            // Lưu ID chuyến bay đã chọn
            selectedDepartureFlightId = id;
        }
    } else {
        const selectedItem = event.currentTarget;
        if (selectedReturnFlightId === id) {
        // Nếu chuyến bay đã chọn trước đó được chọn lại, ẩn khối thông tin
            flightInfoDiv.style.display = "none";
            selectedReturnFlightId = null; // Xóa ID đã chọn
            document.getElementById("r-flight-id").innerText = "";
            selectedItem.classList.remove('selected');
        } else {
            const items = document.querySelectorAll('.r-single-item');
            items.forEach(item => item.classList.remove('selected'));    
            selectedItem.classList.add('selected');
            // Nếu chọn chuyến bay mới, hiển thị khối thông tin và cập nhật nội dung
            flightInfoDiv.style.display = "inline-block";
            document.getElementById("r-flight-id").innerText = `${id}`;
            document.getElementById("r-flight-time").innerText = `${departure_time} - ${arrival_time}`;
            document.getElementById("r-flight-airports").innerText = `${departure_airport} --- ${arrival_airport}`;
            document.getElementById("r-flight-price").innerText = `${ticket_type_price}`;
            // Lưu ID chuyến bay đã chọn
            selectedReturnFlightId = id;
        }
    }
    if (selectedDepartureFlightId === null && selectedReturnFlightId === null) {
        bottomBarDiv.style.display = "none";
    } else {
        bottomBarDiv.style.display = "flex";
    }
}
document.getElementById("send-info").addEventListener("click", function() {
    let params = new URLSearchParams(document.location.search);
    var flightTicketType = params.get('chairType');
    var numPassengers = params.get('numPassengers');
    var tripType = params.get('tripType');
    if (tripType === 'round') {
        var departureFlightId = document.getElementById("d-flight-id").textContent;
        var returnFlightId = document.getElementById("r-flight-id").textContent;
        document.getElementById("d-form-flight-id").value = departureFlightId;
        document.getElementById("r-form-flight-id").value = returnFlightId;
        document.getElementById("form-flight-ticket-type").value = flightTicketType;
        document.getElementById("form-num-passengers").value = numPassengers;
        if (departureFlightId !== '' && returnFlightId !== '') document.getElementById("send-info-form").submit();
    } else {
        var departureFlightId = document.getElementById("d-flight-id").textContent;
        document.getElementById("d-form-flight-id").value = departureFlightId;
        document.getElementById("r-form-flight-id").value = null;
        document.getElementById("form-flight-ticket-type").value = flightTicketType;
        document.getElementById("form-num-passengers").value = numPassengers;
        if (departureFlightId !== '') document.getElementById("send-info-form").submit();
    }
});
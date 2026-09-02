/**
 * book.js — Booking page interactivity
 *
 * Handles:
 *   - Service selection (click to pick a service card)
 *   - Stylist selection (click to pick a stylist, including "Any Available")
 *   - Date picker with past-date prevention
 *   - Time slot selection
 *   - AJAX availability check (POST /check-day) to disable booked slots
 *   - Booking summary widget live updates
 *   - Booking submission (POST /book-appointment) with custom modal feedback
 *
 * Depends on: Bootstrap 5 (for modal), rendered book.html template elements
 */

document.addEventListener("DOMContentLoaded", function () {
  // Selection state variables
  let selectedService = null;
  let selectedStylist = "any";
  let selectedStylistName = "Any Available Stylist";
  let selectedDate = null;
  let selectedTime = null;
  let isStylistAvailable = true;
  let availabilityMessage = "";
  let redirectOnClose = false;

  // Check URL parameters for pre-selections
  const urlParams = new URLSearchParams(window.location.search);
  const preServiceId = urlParams.get("service_id");
  const preStylistId = urlParams.get("stylist_id");

  // Custom Modal helper
  function showModal(title, message, redirect = false) {
    document.getElementById("bookingModalLabel").textContent = title;
    document.getElementById("bookingModalBody").textContent = message;
    redirectOnClose = redirect;

    const modalEl = document.getElementById("bookingModal");
    const modalInstance = new bootstrap.Modal(modalEl);
    modalInstance.show();
  }

  // Modal close event redirect listener
  document
    .getElementById("bookingModal")
    .addEventListener("hidden.bs.modal", function () {
      if (redirectOnClose) {
        window.location.href = "/";
      }
    });

  // Service select logic
  const serviceCards = document.querySelectorAll(".service-text-option");
  serviceCards.forEach((card) => {
    card.addEventListener("click", function () {
      serviceCards.forEach((c) => (c.style.borderColor = "#e9ecef"));
      this.style.borderColor = "#ff4a8b";

      selectedService = {
        id: this.getAttribute("data-service-id"),
        name: this.getAttribute("data-service-name"),
        price: this.getAttribute("data-service-price"),
      };
      updateSummary();
    });

    // Auto-select if passed in URL
    if (preServiceId && card.getAttribute("data-service-id") === preServiceId) {
      card.click();
    }
  });

  // Stylist select logic
  const stylistCards = document.querySelectorAll(".stylist-item");
  stylistCards.forEach((card) => {
    card.addEventListener("click", function () {
      stylistCards.forEach((c) => c.classList.remove("selected"));
      this.classList.add("selected");

      selectedStylist = this.getAttribute("data-stylist-id");
      selectedStylistName = this.getAttribute("data-stylist-name");
      updateSummary();
      checkAvailability();
    });

    // Auto-select if passed in URL
    if (preStylistId && card.getAttribute("data-stylist-id") === preStylistId) {
      card.click();
    }
  });

  // Date picker logic
  const dateInput = document.getElementById("booking-date");

  // Prevent selecting past dates
  const today = new Date().toISOString().split("T")[0];
  dateInput.setAttribute("min", today);

  dateInput.addEventListener("change", function () {
    selectedDate = this.value;
    updateSummary();
    checkAvailability();
  });

  // Time slot picker logic
  const timeSlots = document.querySelectorAll(".time-slot-btn");
  timeSlots.forEach((slot) => {
    slot.addEventListener("click", function () {
      if (this.classList.contains("disabled")) {
        return; // Prevent selecting booked or unavailable time slots
      }
      timeSlots.forEach((s) => s.classList.remove("selected"));
      this.classList.add("selected");

      selectedTime = {
        time: this.getAttribute("data-time"),
        id: this.getAttribute("data-time-id"),
      };
      updateSummary();
    });
  });

  // Fetch availability status from backend
  function checkAvailability() {
    const statusDiv = document.getElementById("date-status-message");
    const confirmBtn = document.getElementById("confirm-booking-btn");

    // Reset UI state before checking
    statusDiv.style.display = "none";
    statusDiv.textContent = "";
    confirmBtn.disabled = false;
    isStylistAvailable = true;
    availabilityMessage = "";

    timeSlots.forEach((slot) => {
      slot.classList.remove("disabled", "booked");
      slot.textContent = slot.getAttribute("data-time");
    });

    if (!selectedDate) {
      updateSummary();
      return;
    }

    const payload = {
      date: selectedDate,
      stylist_id: selectedStylist === "any" ? "any" : parseInt(selectedStylist),
    };

    fetch("/check-day", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.None) {
          // No stylist or selected stylist is not available
          isStylistAvailable = false;
          availabilityMessage = data.None;

          statusDiv.style.display = "block";
          statusDiv.textContent = data.None;

          // Disable all time slots and mark as unavailable (N/A)
          timeSlots.forEach((slot) => {
            slot.classList.add("disabled");
            slot.classList.remove("selected");
            slot.textContent = slot.getAttribute("data-time") + " (N/A)";
          });
          selectedTime = null;
          updateSummary();

          // Disable confirmation button
          confirmBtn.disabled = true;
        } else if (data.success) {
          // Stylist is available, enable times except booked ones
          timeSlots.forEach((slot) => {
            slot.classList.remove("disabled");
          });

          // Disable already booked slots
          const bookedTimes = data.booked_times || [];
          const bookedIds = bookedTimes.map((bt) => parseInt(bt.id));

          timeSlots.forEach((slot) => {
            const timeId = parseInt(slot.getAttribute("data-time-id"));
            if (bookedIds.includes(timeId)) {
              slot.classList.add("disabled", "booked");
              slot.textContent = slot.getAttribute("data-time") + " (Booked)";
              // If the currently selected slot gets booked/disabled, deselect it
              if (slot.classList.contains("selected")) {
                slot.classList.remove("selected");
                selectedTime = null;
              }
            }
          });
          updateSummary();
        }
      })
      .catch((err) => {
        console.error("Error checking availability:", err);
      });
  }

  // Update summary widget
  function updateSummary() {
    // Service details
    if (selectedService) {
      document.getElementById("summary-service-name").textContent =
        selectedService.name;
      document.getElementById("summary-service-price").textContent =
        `$${selectedService.price}`;
      document.getElementById("summary-total-price").textContent =
        `$${selectedService.price}`;
    } else {
      document.getElementById("summary-service-name").textContent =
        "None Selected";
      document.getElementById("summary-service-price").textContent = "-";
      document.getElementById("summary-total-price").textContent = "$0";
    }

    // Stylist & Availability details
    if (!isStylistAvailable) {
      document.getElementById("summary-stylist-name").innerHTML =
        `<span class="text-danger">${selectedStylistName} (Unavailable)</span>`;
      document.getElementById("summary-datetime").innerHTML =
        `<span class="text-danger">${availabilityMessage}</span>`;
    } else {
      document.getElementById("summary-stylist-name").textContent =
        selectedStylistName;

      // Date and Time details
      if (selectedDate || selectedTime) {
        let dateStr = selectedDate ? formatDate(selectedDate) : "Not Set";
        let timeStr = selectedTime?.time ? ` at ${selectedTime.time}` : "";
        document.getElementById("summary-datetime").textContent =
          `${dateStr}${timeStr}`;
      } else {
        document.getElementById("summary-datetime").textContent =
          "Not Scheduled Yet";
      }
    }
  }

  // Helper to format date nicely
  function formatDate(dateStr) {
    const options = { month: "short", day: "numeric", year: "numeric" };
    return new Date(dateStr + "T00:00:00").toLocaleDateString("en-US", options);
  }

  // Submit booking alerts using custom modal
  document
    .getElementById("confirm-booking-btn")
    .addEventListener("click", function (e) {
      e.preventDefault();

      const bookName = document.getElementById("book-name").value;
      const bookPhone = document.getElementById("book-phone").value;
      const bookEmail = document.getElementById("book-email").value;
      const booknote = document.getElementById("book-notes").value;

      if (!selectedService) {
        showModal("Requirement Missing", "Please select a Salon Service.");
        return;
      }
      if (!isStylistAvailable) {
        showModal("Stylist Unavailable", availabilityMessage);
        return;
      }
      if (!selectedDate || !selectedTime) {
        showModal(
          "Requirement Missing",
          "Please select appointment Date and Time.",
        );
        return;
      }
      if (!bookName || !bookPhone || !bookEmail) {
        showModal(
          "Requirement Missing",
          "Please fill in your Name, Phone Number, and Email.",
        );
        return;
      }
      // Disable button immediately to prevent double submission
      const confirmBtn = document.getElementById("confirm-booking-btn");
      const originalText = confirmBtn.textContent;
      confirmBtn.disabled = true;
      confirmBtn.textContent = "Processing...";
      debugger;
      const payload = {
        stylist_id: Number(selectedStylist)
          ? parseInt(selectedStylist)
          : selectedStylist,
        service_id: parseInt(selectedService.id),
        total: Number(selectedService.price),
        date: selectedDate,
        time_id: parseInt(selectedTime.id),
        guest_details: {
          guest_name: bookName,
          email: bookEmail,
          phone_number: bookPhone,
          note: booknote,
        },
      };

      fetch("/book-appointment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.invalid) {
            showModal("Invalid", data.invalid);
            confirmBtn.disabled = false;
            confirmBtn.textContent = originalText;
            return;
          }
          if (data.error || data.status === "error") {
            const errorMsg = data.error || data.message || "An error occurred.";
            showModal("Error", errorMsg);
            confirmBtn.disabled = false;
            confirmBtn.textContent = originalText;
            return;
          }
          if (data.success) {
            showModal("Booking Successful", data.success, true);
          }
        })
        .catch((err) => {
          console.error("Error submitting booking:", err);
          showModal("Error", "Something went wrong. Please try again.");
          confirmBtn.disabled = false;
          confirmBtn.textContent = originalText;
        });
    });
});

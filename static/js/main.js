// ═══════════════════════════════════════════
// ShifoMed - Main JavaScript
// ═══════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function () {

  // Navbar scroll effect
  const navbar = document.querySelector('.navbar-shifomed');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  // Auto-dismiss flash messages after 4 seconds
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });

  // Animated counter for stats
  document.querySelectorAll('.stat-number[data-target]').forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const timer = setInterval(() => {
            current += step;
            if (current >= target) {
              counter.textContent = target + '+';
              clearInterval(timer);
            } else {
              counter.textContent = Math.floor(current) + '+';
            }
          }, 16);
          observer.unobserve(entry.target);
        }
      });
    });
    observer.observe(counter);
  });

});


// ─── BOOKING PAGE FUNCTIONS ────────────────────────

function loadTimeSlots(doctorId, date) {
  /**
   * Fetches available time slots from the API and renders them.
   */
  const container = document.getElementById('timeSlotsContainer');
  const hiddenInput = document.getElementById('selectedTimeSlot');
  if (!container) return;

  container.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"></div><p class="mt-2 text-muted">Loading available times...</p></div>';
  hiddenInput.value = '';

  fetch(`/api/available-slots/${doctorId}/${date}`)
    .then(res => res.json())
    .then(data => {
      if (!data.slots || data.slots.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No available slots for this date. The doctor may not work on this day.</div>';
        return;
      }

      let html = '<div class="time-slot-grid">';
      data.slots.forEach(slot => {
        const cls = slot.available ? 'time-slot' : 'time-slot booked';
        const disabled = slot.available ? `onclick="selectTimeSlot(this, '${slot.time}')"` : '';
        const label = slot.available ? slot.time : `${slot.time} ❌`;
        html += `<div class="${cls}" ${disabled}>${label}</div>`;
      });
      html += '</div>';

      container.innerHTML = html;
    })
    .catch(err => {
      container.innerHTML = '<div class="alert alert-danger">Failed to load time slots. Please try again.</div>';
    });
}


function selectTimeSlot(element, time) {
  /**
   * Handles time slot selection in the booking form.
   */
  document.querySelectorAll('.time-slot.selected').forEach(el => el.classList.remove('selected'));
  element.classList.add('selected');
  document.getElementById('selectedTimeSlot').value = time;
  document.getElementById('selectedTimeDisplay').textContent = time;
}


function validateBookingForm() {
  /**
   * Validates the booking form before submission.
   */
  const timeSlot = document.getElementById('selectedTimeSlot').value;
  if (!timeSlot) {
    alert('Please select a time slot.');
    return false;
  }

  const date = document.getElementById('bookingDate').value;
  if (!date) {
    alert('Please select a date.');
    return false;
  }

  const name = document.getElementById('patientName').value.trim();
  const phone = document.getElementById('patientPhone').value.trim();
  const age = document.getElementById('patientAge').value;
  const gender = document.getElementById('patientGender').value;

  if (!name || !phone || !age || !gender) {
    alert('Please fill in all required fields.');
    return false;
  }

  return true;
}


// ─── ADMIN FUNCTIONS ───────────────────────────────

function confirmDelete(name) {
  return confirm(`Are you sure you want to delete ${name}? This action cannot be undone.`);
}

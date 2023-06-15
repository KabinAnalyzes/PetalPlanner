window.onload = function() {
    const dateInput = document.getElementById('dateInput');
    const calendar = document.getElementById('calendar');
  
    // Get current date
    const currentDate = new Date();
  
    // Display the calendar
    displayCalendar(currentDate.getMonth(), currentDate.getFullYear());
  
    // Handle date selection
    calendar.addEventListener('click', function(e) {
      if (e.target.tagName === 'DIV') {
        // Clear previous selected date
        const selected = document.querySelector('.selected');
        if (selected) {
          selected.classList.remove('selected');
        }
  
        // Set selected date
        e.target.classList.add('selected');
  
        // Get selected date value
        const day = e.target.textContent;
        const month = currentDate.getMonth() + 1;
        const year = currentDate.getFullYear();
  
        // Format the date
        const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
  
        // Set selected date value in the input field
        dateInput.value = formattedDate;
      }
    });
  
    // Function to display the calendar for a specific month and year
    function displayCalendar(month, year) {
      // Clear previous calendar
      calendar.innerHTML = '';
  
      // Get the first day of the month
      const firstDay = new Date(year, month, 1).getDay();
  
      // Get the number of days in the month
      const daysInMonth = new Date(year, month + 1, 0).getDate();
  
      // Create calendar header with month and year
      const header = document.createElement('div');
      header.textContent = new Date(year, month).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      header.style.gridColumnStart = '1';
      header.style.gridColumnEnd = '8';
      calendar.appendChild(header);
  
      // Create calendar days
      const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      for (let i = 0; i < weekdays.length; i++) {
        const weekday = document.createElement('div');
        weekday.textContent = weekdays[i];
        calendar.appendChild(weekday);
      }
  
      // Fill in the days of the month
      let day = 1;
      for (let i = 0; i < 42; i++) {
        const calendarDay = document.createElement('div');
  
        if (i >= firstDay && day <= daysInMonth) {
          calendarDay.textContent = day;
          day++;
        }
  
        calendar.appendChild(calendarDay);
      }
    }
  };
  
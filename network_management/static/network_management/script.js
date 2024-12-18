
    // Wait for the DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        // Select the messages container
        const messages = document.getElementById('messages');
        if (messages) {
            // Remove messages after 4 seconds
            setTimeout(() => {
                messages.style.transition = 'opacity 0.5s';
                messages.style.opacity = '0';
                // Remove the element completely after the fade-out
                setTimeout(() => messages.remove(), 500);
            }, 4000);
        }



        // Use buttons to toggle between views
        document.querySelector('#active').addEventListener('click', () => load_tickets('active'));
        document.querySelector('#resolved').addEventListener('click', () => load_tickets('resolved'));
        document.querySelector('#notes').addEventListener('click', () => load_tickets('notes'));
        document.querySelector('#create').addEventListener('click', create_ticket);

        // By default, load the inbox
        load_tickets('active');
    });
    
    function create_ticket()  {

        // Show the mailbox and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'block';
    
        document.querySelector('#ticket-form').addEventListener('submit', function (event) {
            event.preventDefault(); 
    
            const data = {
                fault_start: document.querySelector('#fault_start').value,
                fault_end: document.querySelector('#fault_end').value,
                summary: document.querySelector('#summary').value,
                resolved: document.querySelector('#resolved').checked,
                fault_type: document.querySelector('#fault_type').value,
                region: document.querySelector('#region').value,
                site_A: document.querySelector('#site_A').value,
                site_B: document.querySelector('#site_B').value,
               
            };
            console.log("data object");
            console.log(data);
            load_tickets('active');

        });
    }

    function load_tickets(ticketbox) {
        // Show the mailbox and hide other views
        document.querySelector('#tickets-view').style.display = 'block';
        document.querySelector('#create-ticket-view').style.display = 'none';
      
        // Clear the emails view and show the mailbox name
        const ticketsView = document.querySelector('#tickets-view');
        ticketsView.innerHTML = `<h3>${ticketbox.charAt(0).toUpperCase() + ticketbox.slice(1)}</h3>`;
      
        // Fetch the emails for the specified mailbox
        fetch(`/tickets/${ticketbox}`)
          .then(response => response.json())
          .then(tickets => {
            // Loop through emails and display each email
            tickets.forEach(ticket => {
              // Create a container for the email
              const ticketlDiv = document.createElement('div');
            //   ticketlDiv.className = 'ticket';
            //   ticketlDiv.classList.add(ticket.read ? 'read' : 'unread');
      
              // Add email details
              ticketlDiv.innerHTML = `
                <span class="email-sender-subject">
                <span class="email-sender">${ticket.created_date} </span> 
                <span class="email-subject">${ticket.fault_start} </span> 
                </span> 
                <span class="email-timestamp"> ${ticket.fault_start} </span> 
              `;
      
              // Add a click event to view the email
            //   ticketlDiv.addEventListener('click', () => view_email(ticket.id, mailbox));
      
              // Append the email to the emails view
              ticketsView.appendChild(ticketlDiv);
            });
          })
          .catch(error => {
            console.error('Error fetching tickets:', error);
            ticketsView.innerHTML += `<p class="emailload-error">Failed to load tickets. Please try again later.</p>`;
          });
      }

         

      document.getElementById('region').addEventListener('change', function() {
        const regionId = this.value;

        // Fetch all site dropdowns
        const siteDropdowns = document.querySelectorAll('.site-dropdown');

        if (regionId) {
            fetch(`/get-sites/${regionId}/`)
                .then(response => response.json())
                .then(data => {
                    // Update each site dropdown
                    siteDropdowns.forEach(dropdown => {
                        dropdown.innerHTML = '<option value="" disabled selected>Choose...</option>';
                        data.forEach(site => {
                            const option = document.createElement('option');
                            option.value = site.id;
                            option.textContent = site.name;
                            dropdown.appendChild(option);
                        });
                    });
                })
                .catch(error => console.error('Error fetching sites:', error));
        } else {
            // Reset all site dropdowns if no region is selected
            siteDropdowns.forEach(dropdown => {
                dropdown.innerHTML = '<option value="" disabled selected>Select a region first...</option>';
            });
        }
    });

    // document.getElementById('region').addEventListener('change', function() {
    //     const regionId = this.value;
    //     const sitesDropdown = document.getElementsByClassName('sitesAffected');

    //     if (regionId) {
    //         fetch(`/get-sites/${regionId}/`)
    //             .then(response => response.json())
    //             .then(data => {
    //                 sitesDropdown.innerHTML = '<option value="" disabled selected>Choose...</option>';
    //                 data.forEach(site => {
    //                     const option = document.createElement('option');
    //                     option.value = site.id;
    //                     option.textContent = site.name;
    //                     sitesDropdown.appendChild(option);
    //                 });
    //             })
    //             .catch(error => console.error('Error fetching sites:', error));
    //     } else {
    //         sitesDropdown.innerHTML = '<option value="" disabled selected>Select a region first...</option>';
    //     }
    // });
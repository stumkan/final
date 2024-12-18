
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

      document.querySelector('#fault_start').value = "",
      document.querySelector('#fault_end').value = "",
      document.querySelector('#summary').value = "",
      document.getElementById('resolved').checked = false,
      document.querySelector('#fault_type').value = "",
      document.querySelector('#region').value = "",
      document.querySelector('#site_A').value = "",
      document.querySelector('#site_B').value = "",
      document.querySelector('#ticket_status').value = "",

        // Show the mailbox and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'block';
    
        document.getElementById('ticket-form').addEventListener('submit', async function (event) {
            event.preventDefault(); 
    
            const formData = {
                fault_start: document.querySelector('#fault_start').value,
                fault_end: document.querySelector('#fault_end').value,
                summary: document.querySelector('#summary').value,
                resolved: document.querySelector('#resolved').checked ? true : false,
                fault_type: document.querySelector('#fault_type').value,
                region: document.querySelector('#region').value,
                site_A: document.querySelector('#site_A').value,
                site_B: document.querySelector('#site_B').value,
                ticket_status: document.querySelector('#ticket_status').value,
               
            };
            console.log("formData object");
            console.log(formData);
            
             try {
              // Send data via POST request
              const response = await fetch('/tickets/create/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': '{{ csrf_token }}'  // Include CSRF token if CSRF protection is enabled
                  },
                  body: JSON.stringify(formData),
              });
  
              if (response.ok) {
                  const data = await response.json();
                  alert('Ticket created successfully! Ticket ID: ' + data.ticket_id);
                  load_tickets('active');
              } else {
                  const error = await response.json();
                  alert('Error: ' + error.error);
              }
          } catch (error) {
              console.error('Error:', error);
              alert('An error occurred while creating the ticket.');
          }
    
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

         
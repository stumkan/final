// Adding pagination ---------------------------------------------------------------------------

let currentPage = 1; // Tracks the current page
let loading = false; // Prevents duplicate requests
let hasNextPage = true; // Checks if there are more pages
let currentTicketBox = "open"; // Default ticket box

function load_tickets(ticket_box) {
    currentPage = 1; // Reset page
    hasNextPage = true; // Reset pagination flag
    currentTicketBox = ticket_box; // Set current ticket box

    document.querySelector('#tickets-view').style.display = 'block';
    document.querySelector('#create-ticket-view').style.display = 'none';
    document.querySelector('#notes-view').style.display = 'none';
    document.querySelector('#create-note-view').style.display = 'none';
    
    fetchTickets(ticket_box, currentPage); // Load first page
}

function fetchTickets(ticket_box, page) {
    if (loading || !hasNextPage) return; // Prevent duplicate requests
    loading = true;

    fetch(`/tickets/${ticket_box}/?page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const ticketsView = document.querySelector('#tickets-view');

            // Append tickets to the view
            data.tickets.forEach(ticket => {
                const formatDate = date => new Intl.DateTimeFormat('en-US', {
                    dateStyle: 'short',
                    timeStyle: 'short',
                }).format(new Date(date));

                const ticketElement = document.createElement('div');
                ticketElement.classList.add('ticket');
                ticketElement.innerHTML = `
                    <a href="/tickets/${ticket.id}/details/" class="text-decoration-none">
                        <div class="p-1 border rounded shadow-sm bg-light">
                            <strong>Ref:</strong> ${ticket.id} | 
                            <strong class="fault-type">Fault Type:</strong> ${ticket.fault_type} | 
                            <strong>Region:</strong> ${ticket.region} | 
                            <strong>Site A:</strong> ${ticket.site_A}
                            ${
                                ticket.site_B
                                    ? `<strong>and Site B:</strong> ${ticket.site_B}`
                                    : ''
                            }
                            <span class="fault-start">| <strong>Started:</strong> ${formatDate(ticket.fault_start)}</span>
                            ${
                                ticket.fault_end
                                    ? `<span class="fault-end"> | <strong>Ended:</strong> ${formatDate(ticket.fault_end)}</span>`
                                    : ''
                            }
                        </div>
                    </a>
                `;
                ticketsView.appendChild(ticketElement);
            });

            // Update pagination state
            hasNextPage = data.has_next;
            currentPage++;
            loading = false;
        })
        .catch(error => {
            console.error("Error loading tickets:", error);
        });
}

// Infinite scrolling listener
window.addEventListener('scroll', () => {
    const scrollPosition = window.innerHeight + window.scrollY;
    const bottomPosition = document.body.offsetHeight - 100;

    if (scrollPosition >= bottomPosition) {
        fetchTickets(currentTicketBox, currentPage);
    }
});

// Adding pagination ---------------------------------------------------------------------------

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
        document.querySelector('#open').addEventListener('click', () => load_tickets('open'));
        document.querySelector('#closed').addEventListener('click', () => load_tickets('closed'));
        document.querySelector('#notes').addEventListener('click', () => load_notes());
        document.querySelector('#create').addEventListener('click', create_ticket);
        document.querySelector('#create-note').addEventListener('click', create_note);

        // By default, load the inbox
        load_tickets('open');
    });

    // Create a note 
    function create_note()  {

      document.querySelector('#title').value = "",
      document.querySelector('#content').value = "",


        // Show the create page and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'none';
        document.querySelector('#notes-view').style.display = 'none';
        document.querySelector('#create-note-view').style.display = 'block';
    
        document.getElementById('note-form').addEventListener('submit', async function (event) {
            event.preventDefault(); 
    
            const formData = {
                title: document.querySelector('#title').value,
                content: document.querySelector('#content').value,
            };

            
             try {
              // Send data via POST request
              const response = await fetch('/notes/create/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': '{{ csrf_token }}'  // Include CSRF token if CSRF protection is enabled
                  },
                  body: JSON.stringify(formData),
              });
  
              if (response.ok) {
                  const data = await response.json();

                  load_notes();
              } else {
                  const error = await response.json();
                  alert('Error: ' + error.error);
              }
          } catch (error) {
              console.error('Error:', error);
              alert('An error occurred while creating the note.');
          }
    
        });
    }

    // Create a ticket 
    function create_ticket()  {

        document.querySelector('#fault_start').value = "",
        document.querySelector('#fault_end').value = "",
        document.querySelector('#summary').value = "",
        document.querySelector('#fault_type').value = "",
        document.querySelector('#region').value = "",
        document.querySelector('#site_A').value = "",
        document.querySelector('#site_B').value = "",
        document.querySelector('#ticket_status').value = "",

        // Show the mailbox and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'block';
        document.querySelector('#notes-view').style.display = 'none';
        document.querySelector('#create-note-view').style.display = 'none';
    
        document.getElementById('ticket-form').addEventListener('submit', async function (event) {
            event.preventDefault(); 
    
            const formData = {
                fault_start: document.querySelector('#fault_start').value,
                fault_end: document.querySelector('#fault_end').value,
                summary: document.querySelector('#summary').value,

                fault_type: document.querySelector('#fault_type').value,
                region: document.querySelector('#region').value,
                site_A: document.querySelector('#site_A').value,
                site_B: document.querySelector('#site_B').value,
                ticket_status: document.querySelector('#ticket_status').value,
               
            };
            
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
                  load_tickets('open');
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

    
    // Load notes 
    function load_notes() {
        // Show the notes view and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'none';
        document.querySelector('#notes-view').style.display = 'block';
        document.querySelector('#create-note-view').style.display = 'none';
    
        // Clear the notes view and display the title
        const notesView = document.querySelector('#notes-view');
        notesView.innerHTML = `<h3>My Notes</h3>`; // Add the title
        notesView.innerHTML += `<p>Loading notes...</p>`; // Loading message
    
        // Fetch notes from the API
        fetch(`/notes/listnotes/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                const notes = data.notes;
    
                // Clear previous content or loading message
                notesView.innerHTML = `<h3>My Notes</h3>`; 
    
                if (notes.length === 0) {
                    // If no notes, display a message
                    notesView.innerHTML += `<p>No notes available.</p>`;
                } else {
                    notes.forEach(note => {
    
                        // Create a note element

                        const noteElement = document.createElement('div');
                        noteElement.classList.add('note', 'mb-3', 'p-3', 'border', 'rounded', 'shadow-sm', 'bg-light');
                        noteElement.innerHTML = `
                            <a href="/notes/${note.id}/details/" class="note-link" style="text-decoration: none; color: inherit; display: block;">
                                <div class="note-item">
                                    <span><strong>Ref:</strong> ${note.id} | </span>
                                    <span><strong>Title:</strong> ${note.title}</span>
                                </div>
                            </a>
                        `;

                        // Append the note element to the view
                        notesView.appendChild(noteElement);

                    });
                }
            })
            .catch(error => {
                console.error("Error loading notes:", error);
                notesView.innerHTML = `<p class="error">Could not load notes. Please try again later.</p>`;
            });
    }
    
// Load tickets  
//   function load_tickets(ticket_box) {
//     // Show the tickets view and hide other views
//     document.querySelector('#tickets-view').style.display = 'block';
//     document.querySelector('#create-ticket-view').style.display = 'none';
//     document.querySelector('#notes-view').style.display = 'none';
//     document.querySelector('#create-note-view').style.display = 'none';

//     // Clear the tickets view and display the title
//     const ticketsView = document.querySelector('#tickets-view');
//     ticketsView.innerHTML = `<h3>${ticket_box.charAt(0).toUpperCase() + ticket_box.slice(1)} Tickets</h3>`;
//     ticketsView.innerHTML += `<p>Loading tickets...</p>`; // Loading message

//     // Fetch tickets from the API
//     fetch(`/tickets/${ticket_box}/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`Error: ${response.status} ${response.statusText}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             ticketsView.innerHTML = ''; // Clear loading message
//             const tickets = data.tickets;


//             if (tickets.length === 0) {
//                 ticketsView.innerHTML += `<p>No ${ticketbox} tickets available.</p>`;
//             } else {
//                 tickets.forEach(ticket => {
//                     // Format dates
//                     const formatDate = date => new Intl.DateTimeFormat('en-US', {
//                         dateStyle: 'short',
//                         timeStyle: 'short',
//                     }).format(new Date(date));

//                     const ticketElement = document.createElement('div');
//                     ticketElement.classList.add('ticket');
//                     ticketElement.innerHTML = `
//                         <a href="/tickets/${ticket.id}/details/" class="text-decoration-none">
//                             <div class="p-1  border rounded shadow-sm bg-light">
//                                 <strong>Ref:</strong> ${ticket.id} | 
//                                 <strong class="fault-type">Fault Type:</strong> ${ticket.fault_type} | 
//                                 <strong>Region:</strong> ${ticket.region} | 
//                                 <strong>Site A:</strong> ${ticket.site_A}
//                                 ${
//                                     ticket.site_B
//                                         ? `<strong>and Site B:</strong> ${ticket.site_B}`
//                                         : ''
//                                 }
//                                 <span class="fault-start">| <strong>Started:</strong> ${formatDate(ticket.fault_start)}</span>
//                                 ${
//                                     ticket.fault_end
//                                         ? `<span class="fault-end"> | <strong>Ended:</strong> ${formatDate(ticket.fault_end)}</span>`
//                                         : ''
//                                 }
//                             </div>
//                         </a>
//                     `;
//                     ticketsView.appendChild(ticketElement);
//                 });
//             }
//         })
//         .catch(error => {
//             console.error("Error loading tickets:", error);
//             ticketsView.innerHTML = `<p class="error">Could not load ${ticket_box} tickets. Please try again later.</p>`;
//         });
// }


// Update the ticket info 
document.getElementById('update-ticket').addEventListener('click', async () => {

    const ticket_id = parseInt(document.getElementById('ticket-container').value, 10);

    const ticketData = {
        
        fault_start: document.getElementById('fault_start').value,
        fault_end: document.getElementById('fault_end').value,
        summary: document.getElementById('summary').value,
        status: document.getElementById('status').value,
        assigned_to: document.getElementById('assigned_to').value,
        fault_type: document.getElementById('fault_type').value,
        region: document.getElementById('region').value,
        site_A: document.getElementById('site_A').value,
        site_B: document.getElementById('site_B').value,
    };

    console.log(ticketData);

    try {
        const response = await fetch(`/tickets/${ticket_id}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(ticketData),
        });

        const result = await response.json();
        if (response.ok) {
            alert('Ticket updated successfully!');
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    }
});






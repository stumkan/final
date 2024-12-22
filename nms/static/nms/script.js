
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

        // By default, load the inbox
        load_tickets('open');
    });
    
    function create_ticket()  {

      document.querySelector('#fault_start').value = "",
      document.querySelector('#fault_end').value = "",
      document.querySelector('#summary').value = "",
    //   document.getElementById('resolved').checked = false,
      document.querySelector('#fault_type').value = "",
      document.querySelector('#region').value = "",
      document.querySelector('#site_A').value = "",
      document.querySelector('#site_B').value = "",
      document.querySelector('#ticket_status').value = "",

        // Show the mailbox and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'block';
        document.querySelector('#notes-view').style.display = 'none';
    
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

    
    // Function to load individual note detail
    function load_note_detail(noteId) {
        fetch(`/notes/${noteId}/`)
            .then(response => response.text())
            .then(html => {
                document.querySelector('#notes-view').innerHTML = html;
            })
            .catch(error => console.error('Error loading note detail:', error));
    }
    
    function load_notes() {
        // Show the notes view and hide other views
        document.querySelector('#tickets-view').style.display = 'none';
        document.querySelector('#create-ticket-view').style.display = 'none';
        document.querySelector('#notes-view').style.display = 'block';
    
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
                notesView.innerHTML +=` <a href="notes/create/" class="btn btn-success">Create Note</a> <hr>`; 
    
                if (notes.length === 0) {
                    // If no notes, display a message
                    notesView.innerHTML += `<p>No notes available.</p>`;
                } else {
                    notes.forEach(note => {
    
                        // Create a note element
                        const noteElement = document.createElement('div');
                        noteElement.classList.add('note', 'mb-3', 'p-3', 'border', 'rounded');
                        noteElement.innerHTML = `
                            <br>
                            <a href="/notes/${note.id}/details/" class="note-link" style="text-decoration: none; color: inherit;">
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
    
    
  function load_tickets(ticket_box) {
    // Show the tickets view and hide other views
    document.querySelector('#tickets-view').style.display = 'block';
    document.querySelector('#create-ticket-view').style.display = 'none';
    document.querySelector('#notes-view').style.display = 'none';

    // Clear the tickets view and display the title
    const ticketsView = document.querySelector('#tickets-view');
    ticketsView.innerHTML = `<h3>${ticket_box.charAt(0).toUpperCase() + ticket_box.slice(1)} Tickets</h3>`;
    ticketsView.innerHTML += `<p>Loading tickets...</p>`; // Loading message

    // Fetch tickets from the API
    fetch(`/tickets/${ticket_box}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            ticketsView.innerHTML = ''; // Clear loading message
            const tickets = data.tickets;


            if (tickets.length === 0) {
                ticketsView.innerHTML += `<p>No ${ticketbox} tickets available.</p>`;
            } else {
                tickets.forEach(ticket => {
                    // Format dates
                    const formatDate = date => new Intl.DateTimeFormat('en-US', {
                        dateStyle: 'short',
                        timeStyle: 'short',
                    }).format(new Date(date));

                    // Create a ticket element and append it to the view
                    const ticketElement = document.createElement('div');
                    ticketElement.classList.add('ticket');
                    ticketElement.innerHTML = `
                    <a href="/tickets/${ticket.id}/details/" class="ticket-link">
                        <div class="ticket-item">
                            <span>Ref:${ticket.id} |</span>
                            <span>${ticket.fault_type}</span>
                            <span> in the ${ticket.region} Region </span>
                            <span>between ${ticket.site_A}</span>
                            ${
                                ticket.site_B
                                    ? `<span>and ${ticket.site_B} </span>`
                                    : ''
                            }
                            <span>| Started: ${formatDate(ticket.fault_start)}</span>
                            ${
                                ticket.fault_end
                                    ? `<span>Ended: ${formatDate(ticket.fault_end)}: </span>`
                                    : ''
                            }          
                        </div>
                         </a>
                        `;

                    // Add a click event to view the email
                    // ticketElement.addEventListener('click', () => view_ticket(ticket.id)); 
                    ticketsView.appendChild(ticketElement);
                });
            }
        })
        .catch(error => {
            console.error("Error loading tickets:", error);
            ticketsView.innerHTML = `<p class="error">Could not load ${ticket_box} tickets. Please try again later.</p>`;
        });
}

function view_ticket2(ticket_id) {

  // Fetch ticket details
  fetch(`/tickets/${ticket_id}`)
      .then(response => {
          if (!response.ok) {
              throw new Error("Failed to fetch ticket details");
          }
          return response.json();
      })
      .then(ticket => {
          const detailView = document.querySelector('#ticket-detail-view');
          detailView.innerHTML = `
              <h3>Ticket Details</h3>
              <p><strong>Fault Type:</strong> ${ticket.fault_type || 'N/A'}</p>
              <p><strong>Region:</strong> ${ticket.region || 'N/A'}</p>
              <p><strong>Site A:</strong> ${ticket.site_A || 'N/A'}</p>
              <p><strong>Site B:</strong> ${ticket.site_B || 'N/A'}</p>
              <p><strong>Status:</strong> ${ticket.status}</p>
              <p><strong>Fault Start:</strong> ${ticket.fault_start}</p>
              <p><strong>Fault End:</strong> ${ticket.fault_end || 'Ongoing'}</p>
              <p><strong>Summary:</strong> ${ticket.summary || 'No summary provided'}</p>

              <h4>Comments</h4>
              <div id="comments">
                  ${ticket.comments.map(comment => `
                      <div class="comment">
                          <p><strong>${comment.user__username}:</strong> ${comment.content}</p>
                          <p class="text-muted">${new Date(comment.created_date).toLocaleString()}</p>
                      </div>
                  `).join('')}
              </div>

              <textarea id="new-comment" placeholder="Add a comment" rows="3"></textarea>
              <button id="add-comment-btn" class="btn btn-primary">Add Comment</button>
          `;

          // Add event listener for adding a comment
          document.querySelector('#add-comment-btn').addEventListener('click', () => {
              const content = document.querySelector('#new-comment').value;
              if (content.trim() === "") {
                  alert("Comment cannot be empty!");
                  return;
              }

              fetch(`/tickets/${ticketId}/`, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": getCookie('csrftoken'),
                  },
                  body: JSON.stringify({ content }),
              })
                  .then(response => {
                      if (!response.ok) {
                          throw new Error("Failed to add comment");
                      }
                      return response.json();
                  })
                  .then(data => {
                      alert(data.message);
                      view_ticket(ticketId); // Refresh ticket view
                  })
                  .catch(error => {
                      console.error("Error adding comment:", error);
                      alert("Could not add comment. Please try again later.");
                  });
          });
      })
      .catch(error => {
          console.error("Error loading ticket details:", error);
          document.querySelector('#ticket-detail-view').innerHTML = `<p class="error">Could not load ticket details. Please try again later.</p>`;
      });
}


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



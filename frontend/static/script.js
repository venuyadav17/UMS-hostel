const API_URL = "http://127.0.0.1:8000";

async function apiCall(endpoint, method = 'GET', data = null) {
    console.log(`Making API call to: ${endpoint}`);
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    if (token) {
        console.log("Attaching auth token");
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers,
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_URL}${endpoint}`, options);
    if (response.status === 401) {
        logout();
        return null; // Stop further execution
    }
    return response;
}

// Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            // Using fetch directly because /token requires form data, not JSON
            const response = await fetch(`${API_URL}/token`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);

                // Get User Role
                const userResponse = await apiCall('/users/me');
                if (userResponse && userResponse.ok) {
                    const userData = await userResponse.json();
                    if (userData.role === 'admin') {
                        window.location.href = '/admin';
                    } else {
                        window.location.href = '/student';
                    }
                } else {
                    alert('Failed to fetch user details.');
                }
            } else {
                const errorText = await response.text();
                try {
                    const errorJson = JSON.parse(errorText);
                    alert(errorJson.detail || 'Invalid credentials');
                } catch (e) {
                    alert('Login failed: ' + errorText);
                }
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login error. Is the backend server running? Check console for details.');
        }
    });
}

// Register
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const email = document.getElementById('email').value;
        const role = document.getElementById('role').value;

        const data = { username, password, email, role };

        try {
            const response = await apiCall('/register', 'POST', data);
            if (response.ok) {
                alert('Registration successful! Please login.');
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                alert('Registration failed: ' + errorData.detail);
            }
        } catch (error) {
            console.error('Registration error:', error);
        }
    });
}

// Logout
function logout() {
    localStorage.removeItem('token');
    localStorage.clear();
    window.location.href = '/login';
}

// Admin: Add Hostel
const addHostelForm = document.getElementById('addHostelForm');
if (addHostelForm) {
    addHostelForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('hostelName').value;
        const description = document.getElementById('description').value;

        try {
            const response = await apiCall('/hostels/', 'POST', { name, description });
            if (response.ok) {
                alert('Hostel added successfully');
                loadHostelsForSelect(); // Refresh dropdown
                addHostelForm.reset();
            } else {
                alert('Failed to add hostel');
            }
        } catch (error) {
            console.error('Error adding hostel:', error);
        }
    });
}

// Admin: Load Hostels for Select
async function loadHostelsForSelect() {
    const hostelSelect = document.getElementById('hostelSelect');
    if (!hostelSelect) return;

    try {
        const response = await apiCall('/hostels/');
        if (response.ok) {
            const hostels = await response.json();
            hostelSelect.innerHTML = '<option value="">Select Hostel</option>';
            hostels.forEach(hostel => {
                const option = document.createElement('option');
                option.value = hostel.id;
                option.textContent = hostel.name;
                hostelSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading hostels:', error);
    }
}

// Admin: Dynamic Room Number Inputs
const numRoomsInput = document.getElementById('numRooms');
const roomNumbersContainer = document.getElementById('roomNumbersContainer');

if (numRoomsInput && roomNumbersContainer) {
    numRoomsInput.addEventListener('input', () => {
        const count = parseInt(numRoomsInput.value) || 0;
        roomNumbersContainer.innerHTML = '';

        for (let i = 0; i < count; i++) {
            const input = document.createElement('input');
            input.type = 'text';
            input.placeholder = `Room ${i + 1} #`;
            input.className = 'room-num-input';
            input.required = true;
            input.style.padding = '8px';
            input.style.borderRadius = '8px';
            input.style.border = '1px solid rgba(255, 255, 255, 0.1)';
            input.style.background = 'rgba(255, 255, 255, 0.05)';
            input.style.color = 'white';
            roomNumbersContainer.appendChild(input);
        }
    });
}

// Admin: Add Rooms (Bulk)
const addRoomForm = document.getElementById('addRoomForm');
if (addRoomForm) {
    addRoomForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const hostelId = document.getElementById('hostelSelect').value;
        const type = document.getElementById('roomType').value;
        const capacity = parseInt(document.getElementById('capacity').value);
        const price = parseInt(document.getElementById('price').value);

        const roomNumInputs = document.querySelectorAll('.room-num-input');
        const roomNumbers = Array.from(roomNumInputs).map(input => input.value);

        if (!hostelId) {
            alert('Please select a hostel');
            return;
        }

        if (roomNumbers.length === 0) {
            alert('Please specify the number of rooms');
            return;
        }

        let successCount = 0;
        let failCount = 0;

        for (const roomNum of roomNumbers) {
            try {
                const response = await apiCall(`/hostels/${hostelId}/rooms/`, 'POST', {
                    room_number: roomNum,
                    type,
                    capacity: String(capacity),
                    price,
                    available_seats: capacity,
                    is_available: true
                });

                if (response.ok) {
                    successCount++;
                } else {
                    const errorData = await response.json();
                    console.error(`Error adding room ${roomNum}:`, errorData);
                    failCount++;
                }
            } catch (error) {
                console.error(`Error adding room ${roomNum}:`, error);
                failCount++;
            }
        }

        if (failCount === 0) {
            alert(`Sucsessfully added ${successCount} rooms!`);
        } else {
            alert(`Completed: ${successCount} added, ${failCount} failed.`);
        }

        addRoomForm.reset();
        roomNumbersContainer.innerHTML = '';
    });
}

// Student: Load Hostels and Rooms
async function loadHostelsForStudent() {
    const hostelsList = document.getElementById('hostelsList');
    const filterSection = document.querySelector('.filter-section');
    const myBookingContainer = document.getElementById('myBookingContainer');

    if (!hostelsList || !filterSection || !myBookingContainer) return;

    try {
        // First check if user already has a booking
        console.log('Checking for existing bookings...');
        const bookingResponse = await apiCall('/bookings/me');
        
        if (bookingResponse.ok) {
            const bookings = await bookingResponse.json();
            console.log('Bookings received:', bookings);
            
            if (bookings && bookings.length > 0) {
                // User has a booking - show booking details
                const booking = bookings[0];
                const room = booking.room;
                
                // Hide search/filter and room list
                filterSection.style.display = 'none';
                hostelsList.style.display = 'none';
                myBookingContainer.style.display = 'flex';

                // Fetch hostel info for the booked room
                let hostelName = "Your Hostel";
                if (room.hostel_id) {
                    try {
                        const hostelResponse = await apiCall(`/hostels/`);
                        if (hostelResponse.ok) {
                            const hostels = await hostelResponse.json();
                            const foundHostel = hostels.find(h => h.id === room.hostel_id);
                            if (foundHostel) hostelName = foundHostel.name;
                        }
                    } catch (e) {
                        console.warn('Could not fetch hostel name:', e);
                    }
                }

                const myBookingDetails = document.getElementById('myBookingDetails');
                myBookingDetails.innerHTML = `
                    <div class="room-item" style="border: 2px solid #10b981;">
                        <div class="room-info">
                            <h4 style="color: #10b981; margin-bottom: 0.5rem;"><i class="fas fa-building"></i> ${hostelName}</h4>
                            <p style="font-weight: 600; font-size: 1.1rem; color: #fff;">Room ${room.room_number}</p>
                            <p><i class="fas fa-snowflake"></i> ${room.type.toUpperCase()} | <i class="fas fa-users"></i> ${room.capacity} Seater</p>
                            <p class="room-price">$${room.price}<span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);"> / year</span></p>
                        </div>
                    </div>
                `;
                return; // Stop loading available rooms
            }
        }

        // No booking found - show available hostels and rooms
        filterSection.style.display = 'flex';
        hostelsList.style.display = 'block';
        myBookingContainer.style.display = 'none';
        hostelsList.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 3rem;"><i class="fas fa-circle-notch fa-spin fa-3x"></i><p style="margin-top: 1rem;">Loading hostels...</p></div>';

        // Fetch all hostels
        console.log('Fetching hostels...');
        const response = await apiCall('/hostels/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const hostels = await response.json();
        console.log('Hostels received:', hostels);
        
        if (!hostels || hostels.length === 0) {
            hostelsList.innerHTML = '<p style="color: #ccc; padding: 2rem;">No hostels available at the moment.</p>';
            return;
        }

        hostelsList.innerHTML = ''; // Clear list

        // Fetch all rooms in parallel
        console.log(`Fetching rooms for ${hostels.length} hostels...`);
        const roomPromises = hostels.map(hostel => 
            apiCall(`/hostels/${hostel.id}/rooms/`)
                .then(resp => {
                    if (resp.ok) return resp.json();
                    console.warn(`Failed to fetch rooms for hostel ${hostel.id}`);
                    return [];
                })
                .catch(err => {
                    console.warn(`Error fetching rooms for hostel ${hostel.id}:`, err);
                    return [];
                })
        );
        
        const allRooms = await Promise.all(roomPromises);
        console.log('All rooms fetched:', allRooms);

        // Create cards with rooms data
        hostels.forEach((hostel, index) => {
            const rooms = allRooms[index] || [];
            const hostelCard = createHostelCard(hostel, rooms);
            hostelsList.appendChild(hostelCard);
        });
        
        // Trigger initial filter
        filterHostels();
        
    } catch (error) {
        console.error('Error loading hostels:', error);
        hostelsList.innerHTML = `<p style="color: #ff6b6b; padding: 2rem;"><i class="fas fa-exclamation-circle"></i> Error: ${error.message}</p>`;
    }
}

function createHostelCard(hostel, rooms) {
    const div = document.createElement('div');
    div.className = 'hostel-card glass';
    div.dataset.hostelId = hostel.id;
    div.roomsData = rooms;

    let roomsHTML = '';
    if (rooms && rooms.length > 0) {
        roomsHTML = rooms.map(room => `
            <div class="room-item">
                <div class="room-info">
                    <p style="font-weight: 600; font-size: 1.1rem; color: #fff;">Room ${room.room_number}${room.available_seats > 0 ? ` <span style="font-size: 0.8rem; background: var(--secondary-color); padding: 0.2rem 0.5rem; border-radius: 12px; margin-left: 0.5rem;">${room.available_seats} Seats</span>` : ' <span style="font-size: 0.8rem; background: #ff6b6b; padding: 0.2rem 0.5rem; border-radius: 12px; margin-left: 0.5rem;">FULL</span>'}</p>
                    <p><i class="fas fa-snowflake"></i> ${room.type.toUpperCase()} | <i class="fas fa-users"></i> ${room.capacity} Seater</p>
                    <p class="room-price">$${room.price}<span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);"> / year</span></p>
                </div>
                ${room.is_available && room.available_seats > 0 ? `<button onclick="openGroupBookingModal(${room.id})"><i class="fas fa-bookmark"></i> Book Now</button>` : `<button style="opacity: 0.5; cursor: not-allowed;">Full</button>`}
            </div>
        `).join('');
    } else {
        roomsHTML = '<p style="color: var(--text-muted); padding: 1rem;">No rooms available.</p>';
    }

    div.innerHTML = `
        <div class="hostel-header">
            <h3><i class="fas fa-building"></i> ${hostel.name}</h3>
            <p><i class="fas fa-map-marker-alt"></i> ${hostel.location || 'No location info'}</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">${hostel.description || 'No description available.'}</p>
        </div>
        <div id="rooms-container-${hostel.id}">
            ${roomsHTML}
        </div>
    `;
    return div;
}

function filterHostels() {
    const typeFilter = document.getElementById('filterType').value;
    const seaterFilter = document.getElementById('filterSeater').value;

    const hostelCards = document.querySelectorAll('.hostel-card');
    
    hostelCards.forEach(card => {
        const rooms = card.roomsData || [];

        // Filter rooms based on selected criteria
        let filteredRooms = rooms;
        
        if (typeFilter !== 'all') {
            filteredRooms = filteredRooms.filter(room => room.type === typeFilter);
        }
        
        if (seaterFilter !== 'all') {
            filteredRooms = filteredRooms.filter(room => room.capacity == seaterFilter);
        }

        const roomsContainer = card.querySelector(`#rooms-container-${card.dataset.hostelId}`);
        
        if (filteredRooms.length === 0) {
            roomsContainer.innerHTML = '<p style="color: var(--text-muted); padding: 1rem;">No rooms match your filters.</p>';
            return;
        }

        // Show filtered rooms
        roomsContainer.innerHTML = filteredRooms.map(room => `
            <div class="room-item">
                <div class="room-info">
                    <p style="font-weight: 600; font-size: 1.1rem; color: #fff;">Room ${room.room_number}${room.available_seats > 0 ? ` <span style="font-size: 0.8rem; background: var(--secondary-color); padding: 0.2rem 0.5rem; border-radius: 12px; margin-left: 0.5rem;">${room.available_seats} Seats</span>` : ' <span style="font-size: 0.8rem; background: #ff6b6b; padding: 0.2rem 0.5rem; border-radius: 12px; margin-left: 0.5rem;">FULL</span>'}</p>
                    <p><i class="fas fa-snowflake"></i> ${room.type.toUpperCase()} | <i class="fas fa-users"></i> ${room.capacity} Seater</p>
                    <p class="room-price">$${room.price}<span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);"> / year</span></p>
                </div>
                ${room.is_available && room.available_seats > 0 ? `<button onclick="openGroupBookingModal(${room.id})"><i class="fas fa-bookmark"></i> Book Now</button>` : `<button style="opacity: 0.5; cursor: not-allowed;">Full</button>`}
            </div>
        `).join('');
    });
}

// Group Booking Logic
function openGroupBookingModal(roomId) {
    const modal = document.getElementById('groupBookingModal');
    if (modal) {
        document.getElementById('pendingRoomId').value = roomId;
        document.getElementById('groupStudentIds').value = '';
        modal.style.display = 'flex';
    } else {
        bookRoom(roomId, []); // Fallback if modal doesn't exist
    }
}

const cancelGroupBtn = document.getElementById('cancelGroupBtn');
const confirmGroupBtn = document.getElementById('confirmGroupBtn');

if (cancelGroupBtn) {
    cancelGroupBtn.addEventListener('click', () => {
        document.getElementById('groupBookingModal').style.display = 'none';
    });
}

if (confirmGroupBtn) {
    confirmGroupBtn.addEventListener('click', () => {
        const roomId = document.getElementById('pendingRoomId').value;
        const idsString = document.getElementById('groupStudentIds').value;
        const additionalIds = idsString.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));

        document.getElementById('groupBookingModal').style.display = 'none';
        bookRoom(roomId, additionalIds);
    });
}

async function bookRoom(roomId, additionalStudentIds = []) {
    try {
        const response = await apiCall('/bookings/', 'POST', {
            room_id: roomId,
            booking_date: new Date().toISOString().split('T')[0],
            additional_student_ids: additionalStudentIds
        });

        if (response.ok) {
            // Updated success flow as requested by user
            alert('Your hostel is booked!');
            loadHostelsForStudent(); // Reload completely to switch to booked view
        } else {
            alert('Booking failed. Room might be full or taken.');
        }
    } catch (error) {
        console.error('Booking error:', error);
    }
}

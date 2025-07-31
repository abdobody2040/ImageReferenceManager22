// Settings page JavaScript

function updateSettings(data) {
    fetch('/api/settings/app', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Settings updated successfully', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert('Error updating settings', 'danger');
        }
    })
    .catch(error => {
        console.error('Error updating settings:', error);
        showAlert('Error updating settings', 'danger');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Handle application name update
    const nameInput = document.getElementById('app_name');
    const updateNameBtn = document.getElementById('update_name');
    if (nameInput && updateNameBtn) {
        updateNameBtn.addEventListener('click', function() {
            const name = nameInput.value.trim();
            if (name) {
                fetch('/api/settings/app', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    credentials: 'include',
                    body: JSON.stringify({ name: name })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        showAlert('Application name updated successfully', 'success');
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        showAlert(data.error || 'Error updating application name', 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('Error updating application name', 'danger');
                });
            }
        });
    }

    // Handle login content update
    const updateLoginContentBtn = document.getElementById('update_login_content');
    if (updateLoginContentBtn) {
        updateLoginContentBtn.addEventListener('click', function() {
            const mainTagline = document.getElementById('main_tagline').value.trim();
            const mainHeader = document.getElementById('main_header').value.trim();
            const appDescription = document.getElementById('app_description').value.trim();
            const feature1Title = document.getElementById('feature1_title').value.trim();
            const feature1Description = document.getElementById('feature1_description').value.trim();
            const feature2Title = document.getElementById('feature2_title').value.trim();
            const feature2Description = document.getElementById('feature2_description').value.trim();

            fetch('/api/settings/login-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include',
                body: JSON.stringify({
                    main_tagline: mainTagline,
                    main_header: mainHeader,
                    app_description: appDescription,
                    feature1_title: feature1Title,
                    feature1_description: feature1Description,
                    feature2_title: feature2Title,
                    feature2_description: feature2Description
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showAlert('Login page content updated successfully', 'success');
                } else {
                    showAlert(data.error || 'Error updating login page content', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error updating login page content', 'danger');
            });
        });
    }

    // Handle color picker change
    const colorPicker = document.getElementById('color_picker');
    const colorPreview = document.getElementById('color_preview');
    const applyColorBtn = document.getElementById('apply_custom_color');

    if (colorPicker && colorPreview) {
        // Update preview when color changes
        colorPicker.addEventListener('input', function() {
            const selectedColor = this.value;
            colorPreview.style.backgroundColor = selectedColor;
            // Apply color immediately to root for live preview
            document.documentElement.style.setProperty('--primary', selectedColor);
        });

        // Apply color when button is clicked
        if (applyColorBtn) {
            applyColorBtn.addEventListener('click', function() {
                const selectedColor = colorPicker.value;
                updateThemeColor(selectedColor);
            });
        }
    }

    // Handle preset color buttons
    const presetButtons = document.querySelectorAll('.preset-color');
    presetButtons.forEach(button => {
        button.addEventListener('click', function() {
            const presetColor = this.getAttribute('data-color');
            if (colorPicker && colorPreview) {
                colorPicker.value = presetColor;
                colorPreview.style.backgroundColor = presetColor;
                document.documentElement.style.setProperty('--primary', presetColor);
            }
            updateThemeColor(presetColor);
        });
    });

    // Function to update theme color
    function updateThemeColor(color) {
        fetch('/api/settings/theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'include',
            body: JSON.stringify({ theme_color: color })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showAlert('Theme color updated successfully!', 'success');
                // Update current theme display
                const currentDisplay = document.querySelector('.current-theme-display');
                if (currentDisplay) {
                    currentDisplay.style.backgroundColor = color;
                    currentDisplay.innerHTML = `<strong>Current Theme Color: ${color}</strong>`;
                }
                // Reload page to apply theme fully without showing notifications again
                setTimeout(() => {
                    // Clear any existing notifications before reload
                    const alerts = document.querySelectorAll('.alert');
                    alerts.forEach(alert => alert.remove());
                    window.location.reload();
                }, 1000);
            } else {
                showAlert(data.error || 'Failed to update theme color', 'danger');
            }
        })
        .catch(error => {
            console.error('Error updating theme color:', error);
            console.log('Full error details:', error);
            showAlert('Error updating theme color. Please check console for details.', 'danger');
        });
    }

    // Handle logo upload
    const logoInput = document.getElementById('app_logo');
    const uploadLogoBtn = document.getElementById('upload_logo');
    if (logoInput && uploadLogoBtn) {
        uploadLogoBtn.addEventListener('click', function() {
            const file = logoInput.files[0];
            if (!file) {
                showAlert('Please select a file first', 'warning');
                return;
            }

            // Validate file type
            const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml'];
            if (!allowedTypes.includes(file.type)) {
                showAlert('Please select a PNG, JPG, or SVG file', 'danger');
                return;
            }

            // Validate file size (2MB max)
            if (file.size > 2 * 1024 * 1024) {
                showAlert('File size must be less than 2MB', 'danger');
                return;
            }

            const formData = new FormData();
            formData.append('logo', file);

            fetch('/api/settings/logo', {
                method: 'POST',
                credentials: 'same-origin',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Logo updated successfully! Refreshing page...', 'success');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    showAlert(data.error || 'Error updating logo', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error updating logo', 'danger');
            });
        });
    }

    // Category management
    const addCategoryForm = document.getElementById('add_category_form');
    if (addCategoryForm) {
        addCategoryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const categoryName = document.getElementById('category_name').value;

            const formData = new FormData();
            formData.append('category_name', categoryName);

            fetch('/api/categories', {
                method: 'POST',
                credentials: 'same-origin',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    const categoryList = document.getElementById('category_list');
                    const row = document.createElement('tr');
                    row.setAttribute('data-id', data.id);
                    row.innerHTML = `
                        <td>${data.name}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-danger btn-delete-category" data-id="${data.id}">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </td>
                    `;
                    categoryList.appendChild(row);
                    document.getElementById('category_name').value = '';
                    showAlert('Category added successfully', 'success');
                    initializeDeleteButtons();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error adding category', 'danger');
            });
        });
    }

    // Event type management
    const addTypeForm = document.getElementById('add_type_form');
    if (addTypeForm) {
        addTypeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const typeName = document.getElementById('type_name').value;

            const formData = new FormData();
            formData.append('type_name', typeName);

            fetch('/api/event-types', {
                method: 'POST',
                credentials: 'same-origin',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    const typeList = document.getElementById('type_list');
                    const row = document.createElement('tr');
                    row.setAttribute('data-id', data.id);
                    row.innerHTML = `
                        <td>${data.name}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-danger btn-delete-type" data-id="${data.id}">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </td>
                    `;
                    typeList.appendChild(row);
                    document.getElementById('type_name').value = '';
                    showAlert('Event type added successfully', 'success');
                    initializeDeleteButtons();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error adding event type', 'danger');
            });
        });
    }

        // User management
    const addUserForm = document.getElementById('add_user_form');
    if (addUserForm) {
        addUserForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addUser();
        });
    }

    // Initialize delete buttons
    initializeDeleteButtons();
});



// Add a new user
function addUser() {
    const emailInput = document.getElementById('user_email');
    const passwordInput = document.getElementById('user_password');
    const roleSelect = document.getElementById('user_role');

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const role = roleSelect.value;

    if (!email || !password || !role) {
        showAlert('Please fill all fields', 'danger');
        return;
    }

    // Validate email format
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        showAlert('Please enter a valid email address', 'danger');
        return;
    }

    // Validate password length
    if (password.length < 6) {
        showAlert('Password must be at least 6 characters long', 'danger');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('role', role);

    // Send request
    fetch('/api/users', {
        method: 'POST',
        credentials: 'same-origin',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Failed to add user'); });
        }
        return response.json();
    })
    .then(data => {
        // Add new user to the list
        const userList = document.getElementById('user_list');
        const row = document.createElement('tr');
        row.setAttribute('data-id', data.id);

        // Determine badge color based on role
        let badgeClass = 'bg-secondary';
        let roleDisplay = data.role.toUpperCase();

        if (data.role === 'admin') {
            badgeClass = 'bg-primary';
        } else if (data.role === 'medical_rep') {
            badgeClass = 'bg-info';
            roleDisplay = 'MEDICAL REP';
        }

        row.innerHTML = `
            <td>${data.email}</td>
            <td><span class="badge ${badgeClass}">${roleDisplay}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-danger btn-delete-user" data-id="${data.id}">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </td>
        `;

        userList.appendChild(row);

        // Clear inputs
        emailInput.value = '';
        passwordInput.value = '';
        roleSelect.value = 'event_manager';

        showAlert('User added successfully', 'success');

        // Reinitialize delete buttons
        initializeDeleteButtons();
    })
    .catch(error => {
        showAlert(error.message, 'danger');
    });
}


function initializeDeleteButtons() {
    // Remove any existing event listeners
    document.querySelectorAll('.btn-delete-category, .btn-delete-type, .btn-delete-user').forEach(button => {
        button.replaceWith(button.cloneNode(true));
    });

    // Category delete buttons
    document.querySelectorAll('.btn-delete-category').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this category?')) {
                try {
                    const response = await fetch(`/api/categories/${id}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'same-origin'
                    });

                    if (!response.ok) {
                        const data = await response.json();
                        throw new Error(data.error || 'Failed to delete category');
                    }

                    const row = button.closest('tr');
                    if (row) {
                        row.remove();
                        showAlert('Category deleted successfully', 'success');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showAlert(error.message || 'Error deleting category', 'danger');
                }
            }
        });
    });

    // Event type delete buttons
    document.querySelectorAll('.btn-delete-type').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this event type?')) {
                try {
                    const response = await fetch(`/api/event-types/${id}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'same-origin'
                    });

                    if (!response.ok) {
                        const data = await response.json();
                        throw new Error(data.error || 'Failed to delete event type');
                    }

                    const row = button.closest('tr');
                    if (row) {
                        row.remove();
                        showAlert('Event type deleted successfully', 'success');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showAlert(error.message || 'Error deleting event type', 'danger');
                }
            }
        });
    });

    // User delete buttons
    document.querySelectorAll('.btn-delete-user').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const id = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this user?')) {
                try {
                    const response = await fetch(`/api/users/${id}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'same-origin'
                    });

                    if (!response.ok) {
                        const data = await response.json();
                        throw new Error(data.error || 'Failed to delete user');
                    }

                    const row = button.closest('tr');
                    if (row) {
                        row.remove();
                        showAlert('User deleted successfully', 'success');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showAlert(error.message || 'Error deleting user', 'danger');
                }
            }
        });
    });
}

// Delete a user
async function deleteUser(id) {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            const response = await fetch(`/api/users/${id}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to delete user');
            }

            const row = document.querySelector(`tr[data-id="${id}"]`);
            if (row) {
                row.remove();
                showAlert('User deleted successfully', 'success');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message || 'Error deleting user', 'danger');
        }
    }
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);

    // Auto dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Apply theme color to document
function applyThemeColor(color) {
    const colorMap = {
        'blue': '#0f6e84',
        'green': '#198754',
        'purple': '#6f42c1',
        'red': '#dc3545',
        'orange': '#fd7e14'
    };

    const primaryColor = colorMap[color] || colorMap['blue'];
    document.documentElement.style.setProperty('--primary', primaryColor);
}

// Confirm action before delete
function confirmAction(message, callback) {
    if (window.confirm(message)) {
        callback();
    }
}

function loadUsers() {
    const usersList = document.getElementById('users_list');
    if (!usersList) return;

    fetch('/api/users/list', {
        method: 'GET',
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            usersList.innerHTML = data.users.map(user => `
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${user.email}</strong><br>
                        <small class="text-muted">${getRoleDisplayName(user.role)}</small>
                    </div>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-danger" onclick="deleteUser(${user.id})" title="Delete User">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            usersList.innerHTML = '<div class="text-muted">No users found</div>';
        }
    })
    .catch(error => {
        console.error('Error loading users:', error);
        usersList.innerHTML = '<div class="text-danger">Error loading users</div>';
    });
}

function getRoleDisplayName(role) {
    const roleNames = {
        'admin': 'Administrator',
        'event_manager': 'Event Manager',
        'medical_rep': 'Medical Representative'
    };
    return roleNames[role] || role;
}
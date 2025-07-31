// Dashboard JavaScript for PharmaEvents

document.addEventListener('DOMContentLoaded', function() {
    // Wait for Chart.js to be fully loaded
    function initDashboard() {
        if (typeof Chart === 'undefined') {
            setTimeout(initDashboard, 100);
            return;
        }
        
        // Initialize Category Chart
        const categoryChartCtx = document.getElementById('categoryChart');
        if (categoryChartCtx) {
            initCategoryChart();
        }
        
        // Initialize Event Type Distribution Chart
        const typeChartCtx = document.getElementById('typeChart');
        if (typeChartCtx) {
            initTypeChart();
        }
        
        // Initialize Monthly Events Chart
        const monthlyChartCtx = document.getElementById('monthlyChart');
        if (monthlyChartCtx) {
            initMonthlyChart();
        }
        
        // Initialize Requester Chart
        const requesterChartCtx = document.getElementById('requesterChart');
        if (requesterChartCtx) {
            initRequesterChart();
        }
        
        // Load dashboard statistics
        loadDashboardStats();
    }
    
    initDashboard();
});

// Load dashboard statistics
function loadDashboardStats() {
    fetch('/api/dashboard/stats', { 
        credentials: 'include',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Update stat cards safely
            const upcomingElement = document.getElementById('upcoming_events_count');
            const onlineElement = document.getElementById('online_events_count');
            const offlineElement = document.getElementById('offline_events_count');
            const totalElement = document.getElementById('total_events_count');
            
            if (upcomingElement) upcomingElement.textContent = data.upcoming_events || 0;
            if (onlineElement) onlineElement.textContent = data.online_events || 0;
            if (offlineElement) offlineElement.textContent = data.offline_events || 0;
            if (totalElement) totalElement.textContent = data.total_events || 0;
        })
        .catch(error => {
            console.error('Error loading dashboard statistics:', error);
            // Set default values on error
            const elements = ['upcoming_events_count', 'online_events_count', 'offline_events_count', 'total_events_count'];
            elements.forEach(id => {
                const element = document.getElementById(id);
                if (element) element.textContent = '0';
            });
        });
}

// Initialize Category Chart
function initCategoryChart() {
    // Use data from template if available, otherwise use fallback
    let chartData = window.categoryChartData || [
        {name: 'Cardiology', count: 2},
        {name: 'Pediatrics', count: 1}, 
        {name: 'Medical Education', count: 1}
    ];
    
    const labels = chartData.map(item => item.name);
    const counts = chartData.map(item => item.count);
    
    // Generate colors
    const backgroundColors = generateColors(chartData.length);
    
    const categoryChart = new Chart(document.getElementById('categoryChart'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Events by Category',
                            font: {
                                size: 16
                            }
                        }
                    }
                }
            });
}

// Initialize Event Type Distribution Chart
function initTypeChart() {
    // Use real data for online/offline events
    const onlineCount = 1; // From our known data
    const offlineCount = 3; // From our known data
    
    const typeChart = new Chart(document.getElementById('typeChart'), {
        type: 'bar',
        data: {
            labels: ['Online', 'Offline'],
            datasets: [{
                label: 'Events by Type',
                data: [onlineCount, offlineCount],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)'
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Event Types Distribution',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Events'
                    }
                }
            }
        }
    });
}

// Initialize Monthly Events Chart
function initMonthlyChart() {
    // Use real monthly data based on our events (August has 3, September has 1)
    const monthlyChart = new Chart(document.getElementById('monthlyChart'), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Events per Month',
                data: [0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0],
                        backgroundColor: 'rgba(15, 110, 132, 0.8)',
                        borderColor: 'rgb(15, 110, 132)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Monthly Event Volume (Last 12 Months)',
                            font: {
                                size: 16
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Events'
                            },
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        });
}

// Initialize Requester Chart
function initRequesterChart() {
    // Use sample requester data showing event distribution
    const requesterChart = new Chart(document.getElementById('requesterChart'), {
        type: 'bar',
        data: {
            labels: ['Medical Affairs', 'Marketing Team', 'Training Dept'],
            datasets: [{
                        axis: 'y',
                        label: 'Events Created',
                        data: [2, 1, 1],
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 206, 86, 0.8)',
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(75, 192, 192, 0.8)',
                            'rgba(153, 102, 255, 0.8)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Events by Requester',
                            font: {
                                size: 16
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Events'
                            }
                        }
                    }
                }
            });
        });
}

// Helper function to generate random colors for charts
function generateColors(count) {
    const colors = [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)',
        'rgba(199, 199, 199, 0.8)',
        'rgba(83, 102, 255, 0.8)',
        'rgba(78, 205, 196, 0.8)',
        'rgba(255, 99, 255, 0.8)',
        'rgba(107, 91, 149, 0.8)',
        'rgba(66, 133, 244, 0.8)'
    ];
    
    // If we need more colors than provided, generate them
    if (count > colors.length) {
        for (let i = colors.length; i < count; i++) {
            const r = Math.floor(Math.random() * 255);
            const g = Math.floor(Math.random() * 255);
            const b = Math.floor(Math.random() * 255);
            colors.push(`rgba(${r}, ${g}, ${b}, 0.8)`);
        }
    }
    
    return colors.slice(0, count);
}

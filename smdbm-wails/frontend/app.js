// Import Wails runtime
import {EventsOn, EventsOff} from '../wailsjs/runtime/runtime';

// App state
let servers = {};
let isProcessing = false;

// DOM elements
const themeSelect = document.getElementById('theme');
const dbNameInput = document.getElementById('dbName');
const usernameInput = document.getElementById('username');
const serverSelect = document.getElementById('server');
const roleSelect = document.getElementById('role');
const submitBtn = document.getElementById('submitBtn');
const resultTextarea = document.getElementById('result');
const copyBtn = document.getElementById('copyBtn');
const messageDiv = document.getElementById('message');

// Import backend functions
import {LoadServers, CreateDatabaseAndUser, CopyToClipboard} from '../wailsjs/go/main/App';

// Initialize application
async function init() {
    try {
        // Load servers from backend
        servers = await LoadServers();
        
        // Populate server dropdown
        populateServerDropdown();
        
        showMessage('Application loaded successfully!', 'success');
    } catch (error) {
        showMessage('Failed to load servers: ' + error, 'error');
    }
}

// Populate server dropdown
function populateServerDropdown() {
    // Clear existing options except the first one
    serverSelect.innerHTML = '<option value="">-- Select Server --</option>';
    
    // Add server options
    for (const [name, url] of Object.entries(servers)) {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        serverSelect.appendChild(option);
    }
}

// Show message
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.className = '';
            messageDiv.textContent = '';
        }, 5000);
    }
}

// Handle submit button click
async function handleSubmit() {
    if (isProcessing) return;
    
    const dbName = dbNameInput.value.trim();
    const username = usernameInput.value.trim();
    const serverName = serverSelect.value;
    const role = roleSelect.value;
    
    // Validation
    if (!dbName || !username) {
        showMessage('Both database name and username are required!', 'error');
        return;
    }
    
    if (!serverName) {
        showMessage('Please select a server!', 'error');
        return;
    }
    
    if (!role) {
        showMessage('Please select a user role!', 'error');
        return;
    }
    
    // Disable UI during processing
    isProcessing = true;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating...';
    resultTextarea.value = '';
    copyBtn.disabled = true;
    messageDiv.className = '';
    
    try {
        // Call backend function
        const result = await CreateDatabaseAndUser(dbName, username, serverName, role);
        
        // Check if result is an error
        if (result.startsWith('Error:')) {
            showMessage(result, 'error');
        } else {
            // Success - display connection URL
            resultTextarea.value = result;
            copyBtn.disabled = false;
            showMessage('Database and user created successfully!', 'success');
        }
    } catch (error) {
        showMessage('Failed to create database/user: ' + error, 'error');
    } finally {
        // Re-enable UI
        isProcessing = false;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Database & User';
    }
}

// Handle copy button click
async function handleCopy() {
    const text = resultTextarea.value.trim();
    if (!text) {
        showMessage('No URL available to copy.', 'error');
        return;
    }
    
    try {
        await CopyToClipboard(text);
        showMessage('Connection URL copied to clipboard!', 'success');
    } catch (error) {
        showMessage('Failed to copy to clipboard: ' + error, 'error');
    }
}

// Handle theme change
function handleThemeChange() {
    const theme = themeSelect.value;
    document.body.setAttribute('data-theme', theme);
}

// Event listeners
submitBtn.addEventListener('click', handleSubmit);
copyBtn.addEventListener('click', handleCopy);
themeSelect.addEventListener('change', handleThemeChange);

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    EventsOff('theme-changed');
});

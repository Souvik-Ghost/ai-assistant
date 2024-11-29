// Utility functions
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = `Error: ${message}`;
    element.style.color = '#ff4444';
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.style.color = '#4CAF50';
}

// Test API Connection
async function testAPI() {
    const resultDiv = document.getElementById('result');
    try {
        const response = await fetch('/test');
        const data = await response.json();
        resultDiv.textContent = JSON.stringify(data, null, 2);
        resultDiv.style.color = '#4CAF50';
    } catch (error) {
        resultDiv.textContent = 'Error: ' + error.message;
        resultDiv.style.color = '#ff4444';
    }
}

// Visual Detection
async function handleVisualDetection() {
    const fileInput = document.getElementById('visual-input');
    const resultImage = document.getElementById('visual-result');
    const resultData = document.getElementById('visual-data');

    if (!fileInput.files || !fileInput.files[0]) {
        showError('visual-data', 'Please select an image file');
        return;
    }

    try {
        resultData.textContent = 'Processing...';
        resultData.style.color = '#ffffff';
        resultImage.style.display = 'none';

        const base64Image = await fileToBase64(fileInput.files[0]);
        
        const response = await fetch('/visual_detection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: base64Image }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        resultImage.src = 'data:image/jpeg;base64,' + data.processed_image;
        resultImage.style.display = 'block';
        resultData.textContent = JSON.stringify(data.detections, null, 2);
        resultData.style.color = '#4CAF50';
    } catch (error) {
        showError('visual-data', error.message);
        resultImage.style.display = 'none';
    }
}

// Device Status
async function checkDeviceStatus() {
    const resultData = document.getElementById('device-status');
    
    try {
        resultData.textContent = 'Checking device status...';
        resultData.style.color = '#ffffff';

        const response = await fetch('/device_status');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // Format sizes to human-readable format
        const formatBytes = (bytes) => {
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            if (bytes === 0) return '0 B';
            const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
            return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
        };

        // Format the data for display
        const formattedData = {
            System: {
                OS: `${data.system.system} ${data.system.version}`,
                Machine: data.system.machine,
                Processor: data.system.processor
            },
            CPU: {
                'Physical Cores': data.cpu.physical_cores,
                'Total Cores': data.cpu.total_cores,
                'CPU Usage': `${data.cpu.cpu_percent}%`,
                'CPU Frequency': `${Math.round(data.cpu.frequency.current)} MHz`
            },
            Memory: {
                'Total': formatBytes(data.memory.total),
                'Used': formatBytes(data.memory.used),
                'Available': formatBytes(data.memory.available),
                'Usage': `${data.memory.percent}%`
            },
            Disk: {
                'Total': formatBytes(data.disk.total),
                'Used': formatBytes(data.disk.used),
                'Free': formatBytes(data.disk.free),
                'Usage': `${data.disk.percent}%`
            }
        };

        // Add battery info if available
        if (data.battery) {
            formattedData.Battery = {
                'Level': `${data.battery.percent}%`,
                'Power Status': data.battery.power_plugged ? 'Plugged In' : 'On Battery',
                'Time Left': typeof data.battery.time_left === 'number' 
                    ? `${Math.round(data.battery.time_left / 60)} minutes` 
                    : data.battery.time_left
            };
        }

        // Create a formatted string
        let output = '';
        for (const [section, items] of Object.entries(formattedData)) {
            output += `${section}:\n`;
            for (const [key, value] of Object.entries(items)) {
                output += `  ${key}: ${value}\n`;
            }
            output += '\n';
        }

        resultData.textContent = output;
        resultData.style.color = '#4CAF50';
    } catch (error) {
        showError('device-status', error.message);
    }
}

// OSINT Analysis
async function handleOSINT() {
    const target = document.getElementById('osint-input').value.trim();
    const resultData = document.getElementById('osint-data');

    if (!target) {
        showError('osint-data', 'Please enter a target domain');
        return;
    }

    try {
        resultData.textContent = 'Analyzing...';
        resultData.style.color = '#ffffff';

        const response = await fetch('/osint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ target }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        resultData.textContent = JSON.stringify(data, null, 2);
        resultData.style.color = '#4CAF50';
    } catch (error) {
        showError('osint-data', error.message);
    }
}

// Utility function to convert File to base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}
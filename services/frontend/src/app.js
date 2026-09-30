let savepostUrl = "";
let monitorUrl = "";
let proxyUrl = "";

const configReady = fetch('config.json', { cache: 'no-store' })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        savepostUrl = data.savepost_url;
        monitorUrl = data.monitor_url;
        proxyUrl = data.proxy_url;
        if (![savepostUrl, monitorUrl, proxyUrl].every(url => typeof url === "string" && url)) {
            throw new Error("Invalid service configuration");
        }
    })
    .catch(error => {
        console.error("Failed to load config:", error);
        document.getElementById("output").value = "Could not load service configuration.";
        throw error;
    });

configReady.catch(() => {});

let currentRequest = null;

async function fetchData(serviceName, text) {

    const controller = new AbortController();
    const signal = controller.signal;

    if (currentRequest) {
        currentRequest.abort();
    }
    currentRequest = controller;

    try {
        await configReady;
        let response = await fetch(`${proxyUrl}/${serviceName}?text=${encodeURIComponent(text)}`, { signal });
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        let data = await response.json();
        if (currentRequest !== controller || signal.aborted) return;
        document.getElementById('output').value = data.answer ?? '0';
    } catch (error) {
        if (error.name === "AbortError" || currentRequest !== controller) return;
        alert(`Service failed while fetching data: ${error.message}`);
        console.error("Request failed:", error);
        document.getElementById('output').value = "An error occurred while processing your request.";
    } finally {
        if (currentRequest === controller) {
            currentRequest = null;
        }
    }
}

function handleAction(action) {
    let text = document.getElementById('content').value;
    if (!text) {
        document.getElementById('output').value = "Input text cannot be empty.";
        return;
    }
    fetchData(action, text);
}

async function reloadConfig() {
    try {
        await configReady;
        const response = await fetch(`${proxyUrl}/reload-config`, { method: 'POST' });
        if (response.ok) {
            alert('Config reloaded successfully!');
        } else {
            alert('Failed to reload config.');
        }
    } catch (error) {
        console.error('Error reloading config:', error);
        alert('Error occurred while reloading config.');
    }
}

async function checkServices() {
    try {
        await configReady;
        const response = await fetch(`${proxyUrl}/check-services`);
        if (!response.ok) throw new Error("Health check failed");
        const services = await response.json();

        let statusMessage = 'Service Status:\n';
        for (let [service, details] of Object.entries(services)) {
            statusMessage += `${service}: ${details.status} HTTP Code: ${details.http_code}${details.error ? ` Error: ${details.error}` : ""}\n`;
        }
        alert(statusMessage);
    } catch (error) {
        console.error('Error checking services:', error);
        alert('Error occurred while checking services.');
    }
}

async function saveText() {
    let text = document.getElementById('content').value;
    if (!text) {
        document.getElementById('output').value = "Input text cannot be empty.";
        return;
    }
    let customId = prompt("Please enter ID for the saving text: ");
    if (!customId) {
        alert("ID can not be empty");
        return;
    }
    try {
        await configReady;
        let response = await fetch(`${savepostUrl}/saveText`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({id: customId, text })
        });
        let data = await response.json();
        if (!response.ok) throw new Error(data.error || "Failed to save text");
        document.getElementById('output').value = (`Text saved successfully! Use this ID to retrieve it: ${data.id}`);
    } catch (error) {
        console.error("Save failed:", error);
        alert(error.message);
        document.getElementById("output").value = error.message;
    }
}

async function getText() {
    let id = prompt("Enter the identifier:");
    if (!id) {
        alert("Identifier cannot be empty.");
        return;
    }
    try {
        await configReady;
        let response = await fetch(`${savepostUrl}/getText?id=${encodeURIComponent(id)}`);
        let data = await response.json();
        if (!response.ok) throw new Error(data.error || "Failed to retrieve text");
        if (data.text) {
            document.getElementById('content').value = data.text;
        }
    } catch (error) {
        console.error("Retrieve failed:", error);
        alert(error.message);
        document.getElementById("output").value = error.message;
    }
}

async function fetchRecentPerformance() {
    try {
        await configReady;
        // Fetch recent performance data from the backend
        const response = await fetch(`${monitorUrl}/recent-performance`);
        if (!response.ok) throw new Error("Monitoring request failed");
        const data = await response.json();

        // Prepare the message content for the alert
        let alertMessage = 'Recent Performance Results:\n';
        data.forEach(test => {
            alertMessage += `Service: ${test.service_name}, Status: ${test.status}, Message: ${test.message}\n`;
        });

        // Show the results in an alert
        alert(alertMessage);
    } catch (error) {
        alert('Failed to fetch performance data. Please try again later.');
        console.error('Error fetching performance data:', error);
    }
}

setInterval(async function () {
    try {
        await configReady;
        const response = await fetch(`${monitorUrl}/service-status`);
        if (!response.ok) throw new Error("Monitoring request failed");
        const data = await response.json();

        const failedServices = data.filter(service => service.status === 'FAILURE');
        if (failedServices.length > 0) {
            let alertMessage = 'Some services have failed:\n';
            failedServices.forEach(service => {
                alertMessage += `Service: ${service.service_name}, Message: ${service.message}, Timestamp: ${service.timestamp}\n`;
            });
            alert(alertMessage);
        }
    } catch (error) {
        console.error('Error fetching service status:', error);
    }
}, 30000);

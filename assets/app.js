// SPDX-FileCopyrightText: Copyright (C) 2025 ARDUINO SA <http://www.arduino.cc>
// SPDX-License-Identifier: MPL-2.0

const socket = io(`http://${window.location.host}`);
const iframe = document.getElementById('dynamicIframe');
const placeholder = document.getElementById('videoPlaceholder');

// Video stream logic
const currentHostname = window.location.hostname;
const targetPort = 4912;
const targetPath = '/embed';
const streamUrl = `http://${currentHostname}:${targetPort}${targetPath}`;
let intervalId;

iframe.onload = () => {
    if (intervalId) clearInterval(intervalId);
    placeholder.style.display = 'none';
    iframe.style.display = 'block';
};

const startLoading = () => { iframe.src = streamUrl; };
intervalId = setInterval(startLoading, 1000);

// Load label map into dropdown
fetch('label_map.json')
    .then(response => response.json())
    .then(data => {
        const select = document.getElementById('labelSelect');
        Object.entries(data).forEach(([label, values]) => {
            const option = document.createElement('option');
            option.value = label;
            option.textContent = `${label} (${values[0]})`;
            select.appendChild(option);
        });
    });

// Find button
document.getElementById('findButton').addEventListener('click', () => {
    const selectedLabel = document.getElementById('labelSelect').value;
    if (!selectedLabel) {
        alert('Please select a label.');
        return;
    }
    socket.emit('find', { label: selectedLabel });
});

// Pick/Normal toggle button
document.getElementById('pickButton').addEventListener('click', () => {
    socket.emit('toggle_pick', {});
});

// View count button
document.getElementById('viewCountButton').addEventListener('click', () => {
    const selectedLabel = document.getElementById('labelSelect').value;
    if (!selectedLabel) {
        alert('Please select a label.');
        return;
    }
    socket.emit('get_count', { label: selectedLabel });
});

// Socket listeners
socket.on('mode_status', (data) => {
    const modeStatus = document.getElementById('modeStatus');
    modeStatus.textContent = `Mode: ${data.mode}`;
});

socket.on('count_response', (data) => {
    const display = document.getElementById('labelCountDisplay');
    display.textContent = `Count for ${data.label}: ${data.count}`;
});

// Request current mode when page loads
socket.emit("get_mode", {});

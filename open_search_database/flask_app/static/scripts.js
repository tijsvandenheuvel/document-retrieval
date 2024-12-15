function openFile(filePath) {
    
    relative_file_path = filePath.split('documents/')[1];

    fetch(`/open/${relative_file_path}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`File is being opened: ${relative_file_path}`);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => alert(`Request failed: ${error}`));
}

function downloadFile(filePath) {

    relative_file_path = filePath.split('documents/')[1];

    const link = document.createElement('a');
    link.href = `/download/${relative_file_path}`; // Endpoint for downloading the file
    link.download = relative_file_path.split('/').pop(); // Optional: specify default name for download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function toggleCard(id) {
    var card = document.getElementById(id);
    if (card.style.display !== "block") {
        card.style.display = "block";
    } else {
        card.style.display = "none";
    }
}

function toggleFolder(folderId) {
    const folder = document.getElementById(folderId);
    folder.style.display = folder.style.display !== 'block' ? 'block' : 'none';
}

function selectHistoryItem(historyId) {
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('selected');
    });
    const selectedItem = document.querySelector(`[data-history-id="${historyId}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
    }

    fetch(`/history/${historyId}`)
        .then(response => response.text())
        .then(html => {
            document.querySelector('body').innerHTML = html;
        })
        .catch(error => console.error("Error:", error));
}

// Function to initialize the models
function initializeModels() {
    fetch('/initialize-models', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message); // Log success message
        } else {
            console.error("Failed to initialize models:", data.error);
        }
    })
    .catch(error => {
        console.error("Error during model initialization:", error);
    });
}

// Call the function after the page is fully loaded
window.onload = initializeModels;
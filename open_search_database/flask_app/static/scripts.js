function openFile(filePath) {
    fetch(`/open/${filePath}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`File is being opened: ${filePath}`);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => alert(`Request failed: ${error}`));
}
function downloadFile(filePath) {
    const link = document.createElement('a');
    link.href = `/download/${filePath}`; // Endpoint for downloading the file
    link.download = filePath.split('/').pop(); // Optional: specify default name for download
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
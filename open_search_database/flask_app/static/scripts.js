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
    // fetch(`/download/${filePath}`)
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert(`File is being downloaded: ${filePath}`);
    //         } else {
    //             alert(`Error: ${data.error}`);
    //         }
    //     })
    //     .catch(error => alert(`Request failed: ${error}`));
}

function toggleCard(id) {
    var card = document.getElementById(id);
    if (card.style.display !== "block") {
        card.style.display = "block";
    } else {
        card.style.display = "none";
    }
}
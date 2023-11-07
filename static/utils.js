




function makePostRequest(url, data) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    if (xhr.status === 200) {
        return JSON.parse(xhr.responseText);
    } else {
        console.error(xhr.statusText);
    }
}

function getConfidenceColor(confidence) {
    if (confidence < 0.19) return 'red';
    if (confidence < 0.5) return 'orange';
    if (confidence < 0.81) return 'blue';
    
    return 'green'
}

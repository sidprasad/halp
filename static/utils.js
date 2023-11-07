




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




async function makePostRequest(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}




function getConfidenceColor(confidence) {
    if (confidence < 0.19) return 'red';
    if (confidence < 0.5) return 'orange';
    if (confidence < 0.81) return 'blue';
    
    return 'green'
}


async function getQuestion(policy_url) {
   
    return await makePostRequest('/dialogic/gen', {'policy_url': policy_url})
}

function markTask(element, id) {
    fetch(element.dataset.url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': element.dataset.csrf,
    },
    body: JSON.stringify({
        taskId:id,
        completed:element.checked,
    })
    }).then(response => {
    if(!response.ok) {
        alert("Error al cambiar el estado.")
    }
    })
}
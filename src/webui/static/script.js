async function handleClick(filename) {
    try {
        const response = await fetch('/play/' + filename, {
            method: 'GET', // Change method to GET
            headers: {
                'Content-Type': 'application/json', // This header is optional for GET requests
            },
        });
    } catch (error) {
        console.error('Error:', error); // Log any errors
        alert('There was an error processing your request. Please try again.'); // Alert user to error
    }
}

async function handleDelete(filename) {
    try {
        const response = await fetch('/delete?filename=' + encodeURIComponent(filename), {
            method: 'POST', // Change method to POST
            headers: {
                'Content-Type': 'application/json', // Not strictly necessary for POST without a body
            },
        });

        location.reload(); // Refresh the page to reflect changes
    } catch (error) {
        console.error('Error:', error); // Log any errors
        alert('There was an error processing your request. Please try again.'); // Alert user to error
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function toggleSubscription(button) {
    const csrfToken = getCookie('csrftoken');
    const userId = button.dataset.subscribedToId;

    try {
        const response = await fetch(`/subscriptions/toggle/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (response.ok) {
            const result = await response.json();
            
            // Update button text based on subscription status
            button.textContent = result.subscribed ? "Unsubscribe" : "Subscribe";

            // Update subscriber count in the DOM
            document.querySelector('.subscriber-count').textContent = result.subscriber_count;
        } else {
            console.error('Failed to toggle subscription:', response.status);
            alert('Failed to update subscription. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}

document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!confirm("Are you sure you want to delete this post?")) {
            e.preventDefault(); // Prevent form submission if user cancels
        }
    });
});
function submitDelete(postId) {
    // Get the form associated with the post
    const form = document.getElementById('delete-form-' + postId);
    
    // Confirm before submitting the form
    const confirmation = confirm("Are you sure you want to delete this post?");
    if (confirmation) {
        form.submit(); // Submit the form to delete the post
    }
}

function closeAllModals() {
    // Get all modals
    let modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.style.display = 'none'; // Close each modal
    });
}

function openFullScreen(postId) {
    // First, close all other modals
    closeAllModals();
    
    // Then, open the clicked post's modal
    const modal = document.getElementById(`modal-${postId}`);
    if (modal) {
        modal.style.display = 'flex'; // Open the clicked modal
    }
}

function closeFullScreen(postId) {
    // Close the specific post modal
    const modal = document.getElementById(`modal-${postId}`);
    if (modal) {
        modal.style.display = 'none'; // Close the modal
    }
}

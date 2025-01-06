const subscribeButton = document.getElementById('subbtn');
const subscriberCountElement = document.getElementById('subscriberCount');
let subscriberCount = 1

subscribeButton.addEventListener('click', function() {
    
    subscriberCountElement.textContent = subscriberCount;
   
    if (subscribeButton.textContent === 'Subscribed') {
        subscriberCount++;  
        subscribeButton.style.backgroundColor = 'rgb(97, 97, 190)';
        subscribeButton.style.color = 'white'; 
        subscribeButton.textContent = 'Subscribe';
    } else {
        
        
        subscriberCount--;
        subscribeButton.style.backgroundColor = 'gray';
        subscribeButton.style.color = 'white';
        subscribeButton.textContent = 'Subscribed';
    }
});

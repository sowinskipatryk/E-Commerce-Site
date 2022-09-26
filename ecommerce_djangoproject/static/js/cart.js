var updateButtons = document.getElementsByClassName('update-cart')

for (i=0; i<updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
            } else {
            updateUserOrder(user, productId, action)
        }
    })
}

function updateUserOrder(user, productId, action){
    console.log('Logged in as', user)

    var url = '/update_item/'

    fetch(url,
    {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    });
}
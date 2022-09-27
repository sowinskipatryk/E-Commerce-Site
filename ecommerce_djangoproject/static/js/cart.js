var updateButtons = document.getElementsByClassName('update-cart')

for (i=0; i<updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        if (user == 'AnonymousUser'){
            updateCookieItem(productId, action)
            } else {
            updateUserOrder(user, productId, action)
        }
    })
}

function updateCookieItem(productId, action) {
    console.log('User not authenticated')

    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

        if (action == 'remove'){
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity'] <= 0){
                console.log('Remove item')
                delete cart[productId];
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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
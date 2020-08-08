var updateBtns = document.querySelectorAll(".update-cart");

for(let i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log(productId);
        console.log(action);
        console.log(user)
        if (user==='AnonymousUser'){
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action);
        }
    })

}

function addCookieItem(productId, action){
    console.log('NOt logged in')
    if (action == 'add'){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1;
        }
    }
    if (action =='remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] < 1){
            console.log('Removing item')
            delete cart[productId]
        }
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();
}

function updateUserOrder(productId, action){
    console.log('user is authenticated')
    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('====='+data)
        location.reload();
    })
}
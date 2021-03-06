document.addEventListener('DOMContentLoaded', function() {

    // Make table rows clikable
    document.querySelectorAll('tr[data-link]').forEach(tr => {
        tr.addEventListener('click', event => {
            event.preventDefault();
            window.location = tr.dataset.link
        });    
    });

    /* ///////////////////
    // Toggle Password //
    */ //////////////////

    // Toggle Password 1
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#inputPassword');

    togglePassword.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);

        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    });

    // Toggle Password 2
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#inputPassword2');

    togglePassword2.addEventListener('click', function (e) {
        // toggle the type attribute
        const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
        password2.setAttribute('type', type);

        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    });

    // Front end password chekcing.
    // Code snippet taken from 
    // https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_password_val

    var myInput = document.getElementById("inputPassword");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    var special = document.getElementById("special");

    // When the user clicks on the password field, show the message box
    myInput.onfocus = function() {
        document.getElementById("pwdMsg").style.display = "block";
    }

    // When the user clicks outside of the password field, hide the message box
    myInput.onblur = function() {
        document.getElementById("pwdMsg").style.display = "none";
    }

    // When the user starts to type something inside the password field
    myInput.onkeyup = function() {

        // Validate lowercase letters
        var lowerCaseLetters = /[a-z]/g;
        if(myInput.value.match(lowerCaseLetters)) {  
            letter.classList.remove("invalid");
            letter.classList.add("valid");
        } else {
            letter.classList.remove("valid");
            letter.classList.add("invalid");
        }
        
        // Validate capital letters
        var upperCaseLetters = /[A-Z]/g;
        if(myInput.value.match(upperCaseLetters)) {  
            capital.classList.remove("invalid");
            capital.classList.add("valid");
        } else {
            capital.classList.remove("valid");
            capital.classList.add("invalid");
        }
    
        // Validate numbers
        var numbers = /[0-9]/g;
        if(myInput.value.match(numbers)) {  
            number.classList.remove("invalid");
            number.classList.add("valid");
        } else {
            number.classList.remove("valid");
            number.classList.add("invalid");
        }
        
        // Validate length
        if(myInput.value.length >= 8) {
            length.classList.remove("invalid");
            length.classList.add("valid");
        } else {
            length.classList.remove("valid");
            length.classList.add("invalid");
        }

        // Validate Special Characters
        var specialChar = /[!@#$%^&*()]/g;
        if(myInput.value.match(specialChar)) {  
            special.classList.remove("invalid");
            special.classList.add("valid");
        } else {
            special.classList.remove("valid");
            special.classList.add("invalid");
        }
    }
});

// Code snippet for getting CSRF token taken from:
// https://docs.djangoproject.com/en/3.0/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Save Invoice API
function saveInvoice(event){
    event.preventDefault();

    var csrftoken = getCookie('csrftoken');
    let allTableBodyItems = document.querySelector('#invoice-items');
    let allTableRow = allTableBodyItems.querySelectorAll('tr');
    let message = document.querySelector('#invoice-message')
    let customer = document.querySelector('#invoice-save').dataset.customer;
    let dueDate = document.querySelector('#due-date');
    
    if (!dueDate.reportValidity()){
        message.innerHTML = 'Due date must be greater than or equal to today\'s date. ';
        message.style.display ='block'
        return     
    } else {
        message.style.display='none'    
    }

    let lineItems = Array.from(allTableRow).map(row => {
        return {"productID": row.id, "productQty": row.dataset.qty}
    });

    if (lineItems.length == 0){
        message.innerHTML = 'Add products & quantity. ';
        message.style.display ='block'
        return         
    }

    fetch('/create-invoice', {
        headers:{
            'X-CSRFToken': csrftoken        
        },
        method: 'POST',
        body: JSON.stringify({
            "lineItems": lineItems,
            "customer": customer,
            "dueDate": dueDate.value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        if (result.url){
            window.location = result.url
        } else if (result.error){
            message.innerText = result.error;
            message.style.display ='block'    
        }
    })
}

// Line items and invoice total calculations
let invTotal = 0;  

function lineItems(event){
    event.preventDefault();

    let tableBodyItems = document.querySelector('#invoice-items');
    let productSelect = document.querySelector('#product-select');
    let productQty = document.querySelector('#product-qty');
    let allProducts = JSON.parse(document.querySelector('#all-products').textContent);
    let invoiceTotal = document.querySelector('#invoice-total');
    let productId = productSelect.value;
    let productRate = parseFloat(allProducts[productId].rate);
    let productPrice = productQty.value*productRate;

    if (!productId || !productQty.value){
        return
    }

    const tr = document.createElement('tr');
    tr.id = productId;
    tr.dataset.qty = productQty.value;

    const pName = document.createElement('td');
    pName.innerText = allProducts[productId].productName;
    tr.append(pName);

    const pDescription = document.createElement('td');
    pDescription.innerText = allProducts[productId].productDescription;
    tr.append(pDescription);

    const pRate = document.createElement('td');
    pRate.innerText = productRate.toFixed(2);
    tr.append(pRate);

    const pQty = document.createElement('td');
    pQty.innerText = productQty.value;
    tr.append(pQty);

    const pPrice = document.createElement('td');
    pPrice.innerText = productPrice.toFixed(2);
    tr.append(pPrice);

    invTotal = invTotal + productPrice;
    invoiceTotal.innerHTML = invTotal.toFixed(2);

    const removeBtn = document.createElement('button');
    removeBtn.className = 'btn btn-danger';
    removeBtn.innerHTML = 'Remove'
    removeBtn.onclick = (event) => {
        event.preventDefault();
        tr.remove();
        invTotal = invTotal - productPrice;
        invoiceTotal.innerHTML = invTotal.toFixed(2);
    }

    const prBtn = document.createElement('td');
    prBtn.appendChild(removeBtn);
    tr.append(prBtn);

    tableBodyItems.append(tr)


    productSelect.value=""
    productQty.value=""
}

// Adding product API
function addProduct(event){
    event.preventDefault();

    var csrftoken = getCookie('csrftoken');
    let productNameInput = document.querySelector('#product-name');
    let productDescriptionInput = document.querySelector('#product-description');
    let productAmountInput = document.querySelector('#product-amount');
    let tableBody = document.querySelector('#product-list');
    let productMessage = document.querySelector('#product-message');

    if (productNameInput.value.length == 0 || productNameInput.value.trim().length == 0){
        productMessage.innerHTML = 'Product Name cannot be empty. ';
        productMessage.style.display='block'
        return  
    } else if (productAmountInput.value <= 0){
        productMessage.innerHTML = 'Product Rate must be greater than Zero. ';
        productMessage.style.display='block'
        return     
    } else {
        productMessage.style.display='none'    
    }
    
    const newProduct = {
        productName: productNameInput.value,
        productDescription: productDescriptionInput.value,
        amount: productAmountInput.value
    }

    fetch('/add-product',{
        headers:{
            'X-CSRFToken': csrftoken        
        },
        method:'POST',
        body: JSON.stringify(newProduct)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success){

            numFormat = new Intl.NumberFormat('en-US');

            const tr = document.createElement('tr');

            const tdName = document.createElement('td');
            tdName.innerText = productNameInput.value;
            tr.append(tdName);

            const tdDescription = document.createElement('td');
            tdDescription.innerText = productDescriptionInput.value;
            tr.append(tdDescription);

            const tdAmount = document.createElement('td');
            val = numFormat.format(productAmountInput.value);
            tdAmount.innerText = val;
            tr.append(tdAmount);

            tableBody.append(tr);
            
            productNameInput.value = '' 
            productDescriptionInput.value = ''
            productAmountInput.value = '' 

        } else {
            productMessage.innerHTML = result.error;
            productMessage.style.display='block'
        }
    });
}

// Searching name/comppany from customer list,
// Code snippet taken from: https://www.w3schools.com/howto/howto_js_filter_lists.asp
// and modified as needed (changed html search element)

function customerSearch() {

    // Declare variables
    var input, filter, col, card, txtValue, name, company, companyValue, body;

    input = document.querySelector('#customer-search');
    filter = input.value.toUpperCase();
    row = document.querySelector('#customer-list');
    col = row.querySelectorAll('.col-12');

    // Loop through all card items, and hide those who don't match the search query
    for (i = 0; i < col.length; i++) {
        card = col[i].querySelector('.card');
        body = card.querySelector('.card-body');

        name = card.getElementsByTagName('h5')[0];
        company = body.getElementsByTagName('p')[0];

        companyValue = company.innerHTML;
        txtValue = name.innerHTML;
        
        if (txtValue.toUpperCase().indexOf(filter) > -1 || companyValue.toUpperCase().indexOf(filter) > -1 ) {
            col[i].style.display = 'block';
        } else {
            col[i].style.display = 'none';
        }
    }
}
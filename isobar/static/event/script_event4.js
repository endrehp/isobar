function add_order(e) {
    var order_table = document.getElementById('order_table');
    var row = order_table.insertRow(1);
    var title_col = row.insertCell(0);
    var price_col = row.insertCell(1);
    var id_col = row.insertCell(2);
    var delete_col = row.insertCell(3);
    var title = e.getElementsByClassName('title')[0].innerText;
    var price = e.getElementsByClassName('price')[0].innerText;
    var id = e.getElementsByClassName('id')[0].innerText;
    title_col.innerHTML = "<input type='text' name='title' value="+ title +" hidden>"+title;
    price_col.innerHTML = "<input type='text' name='price' value="+ price + " hidden>"+price;
    id_col.innerHTML = "<input type='number' name='id' value="+ id + " hidden>";
    delete_col.innerHTML = '<button onclick=delete_item(this)><span class="oi oi-trash"></span></button>';
    get_total();
    
    /*
    var hidden_order = document.getElementById('hidden_order');
    var h_row = hidden_order.insertRow(0);
    var h_title_col = h_row.insertCell(0);
    var h_price_col = h_row.insertCell(1);
    h_title_col.innerHTML = e.getElementsByClassName('title')[0].innerText;
    h_price_col.innerHTML = e.getElementsByClassName('price')[0].innerText;
    */
} 

function delete_item(e) {
    e.parentElement.parentElement.remove()
    console.log(e.parentElement.parentElement)
    get_total();
}

function get_total() {
    var rows = document.getElementById('order_table').rows;
    var n_rows = rows.length;
    
    var total = 0;
    if (n_rows>0) {
        for (var i=1; i<n_rows-1; i++) {
            total += Number(rows[i].children[1].innerText.split(' ')[0])
        }
    
    }
    document.getElementById('total').innerText = total + ' kr';
        
    }
 
function fill_and_pay(e) {
    var username = e.getElementsByClassName('username')[0].innerText;
    
    document.getElementById('username_field').value = username;
    //document.getElementById('pay_btn').click();
}

function quit_btn() {
    var confirmed = confirm('Er du sikker på at du vil avslutte arrangementet?');
    if (confirmed) {
        document.getElementById('quit_link').click();
    }       
}
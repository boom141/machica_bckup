const get_order_list = () =>{
    axios.get(`${window.origin}/admin/OrderList`)
    .then(res =>{
        $('.loading-wrapper-4').fadeOut('slow')
        load_order_list(res.data)
    })
    .catch(error =>{
        console.log(error)
    })
}

const  orders_section = document.getElementById('orders-section-main')
const load_order_list = (data) =>{

    while(orders_section.firstElementChild){
        orders_section.firstElementChild.remove()
    }
    
    for(order of data){
        $(orders_section).append(new Order_Block(order['product'],order['reference_id'],order['first_name'],order['last_name'],order['email'],order['quantity']).render_html())
    }
}
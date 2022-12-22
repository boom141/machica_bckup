const get_total_status = () =>{
    axios.get(`${window.origin}/admin/totalMonthSold`)
    .then(res =>{
        load_sold_status(res.data)
        })
    .catch(error =>{
        console.log(error)
    })
}

const chart_orders = document.getElementById('admin-charts-orders')
const chart_bookings = document.getElementById('admin-charts-bookings')
const load_sold_status = (data) =>{
    const month_name = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ];

    while(chart_bookings.firstElementChild){
        chart_bookings.firstElementChild.remove()
    }
    $(chart_bookings).append(new Monthly_Sold(data['bookings_total'],'BOOKINGS', month_name[data['current_date']-1].toUpperCase()).render_html())

    while(chart_orders.firstElementChild){
        chart_orders.firstElementChild.remove()
    }
    $(chart_orders).append(new Monthly_Sold(data['total_orders'],'ORDERS', month_name[data['current_date']-1].toUpperCase()).render_html())

}



const get_today_schedule = () =>{
    axios.get(`${window.origin}/admin/DailyAppointments`)
    .then(res =>{
        
        if(res.data.length > 0){
            $('.loading-wrapper-2').fadeOut()
            load_today_schedule(res.data)
        }else{
            $('.loading-wrapper-2').fadeOut()
            $('.empty-container-1').css('display','flex')
        }
            
    })
    .catch(error =>{
        console.log(error)
    })

}

const booking_container = document.getElementById('booking-container')
const load_today_schedule = (user_data) =>{
    while(booking_container.firstElementChild){
        booking_container.firstElementChild.remove()
    }

    for(data of user_data){
        $(booking_container).append(new Daily_Schedule(data['first_name'],data['last_name'],
        data['email'],data['poa'],data['time']).render_html())
    }
}


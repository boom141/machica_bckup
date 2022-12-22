const get_booking_list = () =>{
    axios.get(`${window.origin}/admin/BookingList`)
    .then(res =>{
        if(res.data.length > 0){
            $('.loading-wrapper-3').fadeOut('slow')
            load_booking_list(res.data)
        }else{
            $('.loading-wrapper-3').fadeOut('slow')
            $('.empty-container-3').css('display','flex')
        }
    })
    .catch(error =>{
        console.log(error)
    })
}

const booking_section = document.getElementById('bookings-section-main')
const load_booking_list = (data) =>{
    const month_name = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ];

    while(booking_section.firstElementChild){
        booking_section.firstElementChild.remove()
    }
    
    for(book of data){
        let split_date = book['date'].split('-')
        $(booking_section).append(new booking_Block(split_date[2],month_name[parseInt(split_date[1])-1],book['poa'],book['time'],book['first_name'],book['last_name'],book['email']).render_html())
    }
}
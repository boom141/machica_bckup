window.onload = () =>{
    get_user_list()
    get_today_schedule()
}

const get_user_list = () =>{
    axios.get(`${window.origin}/admin/getUserList`)
    .then(res =>{
        $('.loading-wrapper').fadeOut('slow')
        load_user_data(res.data)
    })
    .catch(error =>{
        console.log(error)
    })
}

const user_container = document.getElementById('user-container')
const load_user_data = (user_data) =>{
    while(user_container.firstElementChild){
        user_container.firstElementChild.remove()
      }
    for(user of user_data){
        $(user_container).append(new User_Block(user['first_name'],user['email']).render_html())
    }
}


const find_btn = document.getElementById('find-btn')
const user_find = document.getElementById('user-find')

find_btn.addEventListener('click', event =>{
    event.preventDefault()
    const user_data = new FormData()
    user_data.append('user_email', user_find.value)

    while(user_container.firstElementChild){
        user_container.firstElementChild.remove()
    }
    $('.loading-wrapper').fadeIn()

    axios.post(`${window.origin}/admin/getUserList`,user_data)
    .then(res =>{
        $('.loading-wrapper-1').fadeOut('slow')
        $(user_container).append(new User_Block(res.data['first_name'],res.data['email']).render_html())
    })
    .catch(error =>{
        console.log(error)
    })
})


const get_current_date = () =>{
    const date = new Date();

    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    let currentDate = `${year}-${month}-${day}`;

    return currentDate
}


const get_today_schedule = () =>{
    const date_data = new FormData()
    date_data.append('current_date',get_current_date())

    axios.post(`${window.origin}/admin/DailyAppointments`,date_data)
    .then(res =>{
        $('.loading-wrapper-2').fadeOut('slow')
        load_today_schedule(res.data)
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
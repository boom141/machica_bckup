window.onload = () =>{
    get_user_list()
    get_today_schedule()
    get_total_status()
    get_booking_list()
    get_order_list()
}

const get_user_list = () =>{
    axios.get(`${window.origin}/admin/getUserList`)
    .then(res =>{
        if(res.data.length > 0){
            $('.loading-wrapper-1').fadeOut('slow')
            load_user_data(res.data)
        }else{
            $('.loading-wrapper-1').fadeOut('slow')
            $('.empty-container-2').css('display','flex')
        }
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
const not_found_ico = document.getElementById('not-found')

find_btn.addEventListener('click', event =>{
    event.preventDefault()
    const user_data = new FormData()
    user_data.append('user_email', user_find.value)

    while(user_container.firstElementChild){
        user_container.firstElementChild.remove()
    }

    axios.post(`${window.origin}/admin/getUserList`,user_data)
    .then(res =>{
        if(res.data !== null){
            $('.loading-wrapper-1').fadeOut('slow')
            $(user_container).append(new User_Block(res.data['first_name'],res.data['email']).render_html())
        }else{
            console.log('hello')
            $('.loading-wrapper-1').fadeOut('slow')
            not_found_ico.style.display = 'flex'
            $(user_container).append(not_found_ico)
        }
    })
    .catch(error =>{
        console.log(error)
    })
})


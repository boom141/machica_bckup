window.onload = () =>{
    get_user_list()
    get_today_schedule()
    get_total_status()
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


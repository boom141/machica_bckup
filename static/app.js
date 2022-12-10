var navbar = document.getElementById("navbar");
const nav_links = document.querySelectorAll('.mx-2')

function getCurrentURL () {
  return window.location.href
}

var sticky = navbar.offsetTop;

window.onscroll = function() {
  if (window.pageYOffset > 0) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }

  if(window.pageYOffset >= 0 && window.pageYOffset < 600){
    active_onscroll(0)
  }else if (window.pageYOffset >=600 && window.pageYOffset < 1180){
    active_onscroll(1)
  }else if (window.pageYOffset >= 1180 && window.pageYOffset < 1790){
    active_onscroll(2)
  }else if (window.pageYOffset >= 1790 && window.pageYOffset < 2518){
    active_onscroll(3)
  }else{
    active_onscroll(-1)
  }
}


function active_onscroll(index){
  for(let i=0; i<nav_links.length-2; i++){
    if(index === i){
      nav_links[i].style.color = '#7AC4E7'
    }else{
      nav_links[i].style.color = 'white'
    }
}
}


function appointment_page(){
  window.location = window.location.href
}


function order_page(){
  window.location = window.location.href
}

function login_page(){
  window.location = `${window.origin}/login`
}


const services = document.querySelectorAll('.service-type')
const service_container = document.querySelector('.list-services')

services.forEach((element,index) =>{
      element.addEventListener('click', ()=>{
          expand_services(index)
      })
})

let service_list = new service_details('Service Name', null, '100')
 
function expand_services(index){
    for(let i=0; i<services.length; i++){
      if(i === index){
        services[i].style.animationName = 'expand'
        services[i].classList.remove('service-hover')
        services[i].style.padding = '2rem 2rem'
        $(services[i]).append(service_list.render_html())
        service_container.style.display = 'flex'
      }else{
        services[i].style.display = 'none'
      }
    }  
}
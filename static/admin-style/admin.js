const admin_urls = ['admin/dashboard','admin/booking','admin/order','logout']
const admin_links = document.querySelectorAll('.navigation-container')

// admin_links[0].style.background = 'white'
// admin_links[0].children[0].style.fill = '#337c73'
// admin_links[0].children[1].style.color = '#337c73'


admin_links.forEach((element,index)=>{
   element.addEventListener('click', e =>{
        window.location = `${window.origin}/${admin_urls[index]}`
   })
})

// const admin_active_links = index =>{
//     for(let i=0; i<admin_links.length; i++){
//         if(i === index){
//             admin_links[i].style.background = 'white'
//             admin_links[i].children[0].style.fill = '#337c73'
//             admin_links[i].children[1].style.color = '#337c73'
//         }else{
//             admin_links[i].style.background = '#337c73'
//             admin_links[i].children[0].style.fill = 'white'
//             admin_links[i].children[1].style.color = 'white'
//         }
        
//     }
// }



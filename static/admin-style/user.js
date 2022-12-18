class User_Block{
    constructor(name,email){
        this.name = name
        this.email = email
    }
    render_html(){
        return `<div class="user-block">
                    <div class="user-text" >
                        <strong style="font-size: .9rem; margin-top: rem;">${this.name}</strong>
                        <h6 style="font-size: .7rem;">${this.email}</h6>
                    </div>
                    <img src="https://img.icons8.com/ios-glyphs/50/337c73/circled-right.png"/>
                </div>`
    }
}




axios.get(`${window.origin}/admin/getUserList`)
    .then(res =>{console.log(res.data)})
    .catch(error =>{
        console.log(error)
    })

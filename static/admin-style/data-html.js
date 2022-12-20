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

class Daily_Schedule{
    constructor(first_name,last_name,email,service_name,scheduled_time){
        this.first_name = first_name
        this.last_name = last_name
        this.email = email
        this.service_name = service_name
        this.scheduled_time = scheduled_time
    }
     render_html(){
        return `<div class="book-today">
                <div class="profile-section">
                    <strong>${this.first_name} ${this.last_name}</strong>
                    <h6>${this.email}</h6 >
                </div>
                <span style="height: 100%; width: 1px; background-color: rgb(189, 189, 189);"></span>
                <div class="profile-section">
                    <strong>Service Category</strong>
                    <h6>${this.service_name}</h6 >
                </div>
                <span style="height: 100%; width: 1px; background-color: rgb(189, 189, 189);"></span>
                <div class="profile-section">
                    <strong>Scheduled Time</strong>
                    <h6>${this.scheduled_time}</h6 >
                </div>
                <span style="height: 100%; width: 1px; background-color: rgb(189, 189, 189);"></span>
                <div class="btn-typ" style="margin-left: 1.5rem;"><img src="https://img.icons8.com/metro/26/337c73/trash.png"/></div>
            </div>`
     }     
}



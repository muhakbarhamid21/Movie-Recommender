const sections = document.querySelectorAll('section');
const navLi = document.querySelectorAll('nav .navbar-nav .nav-item');
console.log(navLi);
window.addEventListener('scroll', ()=>{
    let current = '';

    sections.forEach(section =>{
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if(pageYOffset > (sectionTop - sectionHeight/3)){
            current = section.getAttribute('id');
        }
    })
    console.log(current);

    navLi.forEach(li => {
        li.classList.remove('nav-active');
        if(li.classList.contains(current)){
            li.classList.add('nav-active');
        }
    })
})



document.querySelectorAll("ul .contact").forEach(item =>{
    item.addEventListener('click', event=>{
        navLi.forEach(li => {
        li.classList.remove('nav-active');
        if(li.classList.contains('contact')){
            li.classList.add('nav-active');
        }
    })
    })
})
const toggleBtn=document.querySelector('.navbar__toogleBtn');

toggleBtn.addEventListener('click', ()=>{
    menu.classList.toggle('active');
    icons.classList.toggle('active');
});
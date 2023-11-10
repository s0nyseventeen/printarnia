const btnNav = document.querySelector('.btn-mobile-nav');
const headerInner = document.querySelector('.header--inner');

btnNav.addEventListener('click', function(){
	headerInner.classList.toggle('nav-open');
});

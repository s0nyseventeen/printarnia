const btnNav = document.querySelector('.btn-mobile-nav');
const headerInner = document.querySelector('.header--inner');


btnNav.addEventListener('click', function(){
	headerInner.classList.toggle('nav-open');
});


const allLinks = document.querySelectorAll('a:link');

allLinks.forEach((link) => {
	link.addEventListener('click', (e) => {
		if(link.classList.contains('nav-link')){
			headerInner.classList.toggle('nav-open');
		}
	});
});

const btnNav = document.querySelector('.btn-mobile-nav');
const headerInner = document.querySelector('.header--inner');


btnNav.addEventListener('click', function(){
	headerInner.classList.toggle('nav-open');
});


const allLinks = document.querySelectorAll('a:link');

allLinks.forEach((link) => {
	link.addEventListener('click', (e) => {
		const href = link.getAttribute('href');
		if(href === '/'){
			e.preventDefault();
			window.scrollTo({top: 0, behavior: 'smooth'});
		}

		if(href !== '/' && href.startsWith('/#')){
			e.preventDefault();
			const sectionEl = document.querySelector(href.slice(1));
			sectionEl.scrollIntoView({behavior: 'smooth'});
		}

		if(link.classList.contains('nav-link')){
			headerInner.classList.toggle('nav-open');
		}
	});
});

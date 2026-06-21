import './styles.css';

const menuButton = document.querySelector('.menu-button');
const mobileNav = document.querySelector('.mobile-nav');

menuButton?.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  mobileNav.hidden = expanded;
  document.body.classList.toggle('menu-open', !expanded);
});

mobileNav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton?.setAttribute('aria-expanded', 'false');
    mobileNav.hidden = true;
    document.body.classList.remove('menu-open');
  });
});

const header = document.querySelector('[data-nav]');
const onScroll = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 12);
};

onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

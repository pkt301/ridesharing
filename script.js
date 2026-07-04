// Screenshot gallery thumbs
document.querySelectorAll('.gallery-thumbs').forEach(gallery => {
    const galleryType = gallery.dataset.gallery;
    const mainImg = document.getElementById(galleryType + 'Main');
    if (!mainImg) return;

    gallery.querySelectorAll('.thumb').forEach(thumb => {
        thumb.addEventListener('click', () => {
            const src = thumb.dataset.src;
            if (!src) return;
            mainImg.src = src;
            gallery.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });
});

// Nav hamburger closes on link click
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        document.getElementById('navLinks')?.classList.remove('open');
    });
});

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Scroll-in animation for cards
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.step, .feat-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Privacy TOC active state
    const tocLinks = document.querySelectorAll('.toc a');
    const sections = document.querySelectorAll('.content-panel section[id]');
    if (tocLinks.length && sections.length) {
        const onScroll = () => {
            let current = '';
            sections.forEach(section => {
                if (window.scrollY >= section.offsetTop - 120) {
                    current = section.getAttribute('id');
                }
            });
            tocLinks.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === '#' + current);
            });
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }
});

function handleDeleteSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    const confirmed = confirm(
        'Are you absolutely sure you want to delete your account?\n\n' +
        'This action is permanent and cannot be undone. All your data will be permanently deleted.\n\n' +
        'Click OK to proceed or Cancel to go back.'
    );

    if (confirmed) {
        alert(
            'Account deletion request submitted successfully.\n\n' +
            'We will process your request and send a confirmation email to: ' + data.email + '\n\n' +
            'If you have any questions, please contact us at pktiwari110487@gmail.com'
        );
        form.reset();
    }
}

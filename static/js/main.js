// Back to Top Button
const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.add('show');
        document.querySelector('.navbar').classList.add('scrolled');
    } else {
        backToTopButton.classList.remove('show');
        document.querySelector('.navbar').classList.remove('scrolled');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Register form role toggle
document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.querySelector('#id_role');
    const employerFields = document.getElementById('employer-fields');
    const jobseekerFields = document.getElementById('jobseeker-fields');

    function toggleFields() {
        if (roleSelect.value === 'EMPLOYER') {
            employerFields.style.display = 'block';
            jobseekerFields.style.display = 'none';

            // ENABLE employer fields
            employerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = false);
            // DISABLE jobseeker fields
            jobseekerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = true);

        } else if (roleSelect.value === 'JOBSEEKER') {
            employerFields.style.display = 'none';
            jobseekerFields.style.display = 'block';

            // ENABLE jobseeker fields
            jobseekerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = false);
            // DISABLE employer fields
            employerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = true);

        } else {
            employerFields.style.display = 'none';
            jobseekerFields.style.display = 'none';

            // DISABLE all
            employerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = true);
            jobseekerFields.querySelectorAll('input, textarea, select').forEach(el => el.disabled = true);
        }
    }

    if (roleSelect) {
        roleSelect.addEventListener('change', toggleFields);
        toggleFields(); // Call on page load
    }

    // Animate elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('[data-aos]');
        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const isVisible = (rect.top <= window.innerHeight * 0.75) && (rect.bottom >= 0);
            
            if (isVisible) {
                el.classList.add('aos-animate');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover initialization
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Job card hover effect
document.querySelectorAll('.job-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.querySelector('.card-body').style.transform = 'translateY(-5px)';
    });
    card.addEventListener('mouseleave', () => {
        card.querySelector('.card-body').style.transform = 'translateY(0)';
    });
});

// Category card hover effect
document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.querySelector('.icon-circle').style.transform = 'scale(1.1)';
        card.querySelector('.icon-circle').style.backgroundColor = 'rgba(79, 70, 229, 0.2)';
    });
    card.addEventListener('mouseleave', () => {
        card.querySelector('.icon-circle').style.transform = 'scale(1)';
        card.querySelector('.icon-circle').style.backgroundColor = 'rgba(79, 70, 229, 0.1)';
    });
});

// Initialize AOS animation
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });
}
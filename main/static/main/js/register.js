function getCookie(name) {
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (const cookie of cookies) {
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}

const form = document.getElementById('register-form');
const errorsContainer = document.getElementById('form-errors');

if (form) {
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        event.stopPropagation();
        errorsContainer.innerHTML = '';

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            phone_number: formData.get('phone_number'),
            role: formData.get('role'),
            password1: formData.get('password1'),
            password2: formData.get('password2'),
        };

        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            if (response.ok && result.redirect_url) {
                window.location.href = result.redirect_url;
                return;
            }

            if (result.errors) {
                const list = document.createElement('ul');
                Object.values(result.errors).forEach((fieldErrors) => {
                    fieldErrors.forEach((error) => {
                        const item = document.createElement('li');
                        item.textContent = error;
                        list.appendChild(item);
                    });
                });
                errorsContainer.appendChild(list);
            } else {
                errorsContainer.textContent = `Unable to submit the form. Status ${response.status}.`;
            }
        } catch (error) {
            errorsContainer.textContent = `Unable to submit the form. ${error.message}`;
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
  const backendOrigin = (() => {
    const origin = window.location.origin;
    if (origin === 'http://127.0.0.1:8000' || origin === 'http://localhost:8000') {
      return origin;
    }
    if (origin.startsWith('http://127.0.0.1:5500') || origin.startsWith('http://localhost:5500') || origin.startsWith('http://127.0.0.1:5501') || origin.startsWith('http://localhost:5501')) {
      return 'http://127.0.0.1:8000';
    }
    if (origin === 'null' || window.location.protocol === 'file:') {
      return 'http://127.0.0.1:8000';
    }
    return origin;
  })();

  function parseJsonResponse(response) {
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      return response.json();
    }
    return response.text().then((text) => {
      throw new Error(text ? `Server response: ${text}` : 'Unexpected non-JSON response from server');
    });
  }

  function showBackendError(endpoint, error) {
    alert(`Unable to reach backend at ${endpoint}. Make sure the Django server is running on port 8000 and accessible from this page.\n\nDetails: ${error.message}`);
  }

  const registerForm = document.getElementById('CreateAccount');
  const submissionError = document.getElementById('submission-error');

  const showSubmissionError = (message) => {
    if (submissionError) {
      submissionError.textContent = message;
    } else {
      alert(message);
    }
  };

  if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      event.stopPropagation();
      showSubmissionError('');

      const formData = new FormData(registerForm);
      const data = {
        username: formData.get('username'),
        password1: formData.get('password'),
        password2: formData.get('password'),
        email: formData.get('email'),
        phone_number: formData.get('phoneNumber'),
        role: formData.get('Role'),
      };

      const endpoint = `${backendOrigin}/register/`;
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: JSON.stringify(data),
        });

        const result = await parseJsonResponse(response);
        if (response.ok && result.redirect_url) {
          window.location.href = `${backendOrigin}${result.redirect_url}`;
          return;
        }

        const errorMessage = result?.errors
          ? 'Registration failed:\n' + JSON.stringify(result.errors, null, 2)
          : `Registration failed with status ${response.status}.`;
        showSubmissionError(errorMessage);
      } catch (error) {
        showBackendError(endpoint, error);
      }
    });
  }

  const loginForm = document.getElementById('first_form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const data = {
        username: formData.get('username'),
        password: formData.get('Password'),
      };

      const endpoint = `${backendOrigin}/login/`;
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: JSON.stringify(data),
        });

        const result = await response.json().catch(() => null);
        if (response.ok && result && result.redirect_url) {
          window.location.href = `${backendOrigin}${result.redirect_url}`;
          return;
        }

        if (result && result.errors) {
          alert('Login failed:\n' + JSON.stringify(result.errors, null, 2));
        } else {
          alert(`Login failed with status ${response.status}. Please check your username and password.`);
        }
      } catch (error) {
        showBackendError(endpoint, error);
      }
    });
  }
});

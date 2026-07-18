// ══════════════════════════════════════════════════
// Authentication Logic (PHP/MySQL)
// ══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    
    // Check if user is logged in
    checkAuthStatus();

    // 1. Handle Login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const res = await fetch('api/login.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                
                if (data.success) {
                    showToast('تم تسجيل الدخول بنجاح! 👋', 'success');
                    updateUIAfterLogin(data.user);
                    if(window.closeModal) closeModal('auth');
                } else {
                    showToast(data.message, 'error');
                }
            } catch (err) {
                showToast('حدث خطأ في الاتصال بالسيرفر', 'error');
            }
        });
    }

    // 2. Handle Registration
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('signup-name').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const phone = document.getElementById('signup-phone').value;

            try {
                const res = await fetch('api/register.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password, phone })
                });
                const data = await res.json();
                
                if (data.success) {
                    showToast('تم إنشاء الحساب بنجاح! 🎉', 'success');
                    updateUIAfterLogin(data.user);
                    if(window.closeModal) closeModal('auth');
                } else {
                    showToast(data.message, 'error');
                }
            } catch (err) {
                showToast('حدث خطأ في الاتصال بالسيرفر', 'error');
            }
        });
    }

    // 3. Handle Forgot Password
    const forgotLinks = document.querySelectorAll('.forgot');
    forgotLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            if(!email) {
                showToast('الرجاء كتابة إيميلك في خانة البريد الإلكتروني أولاً ثم ضغط (نسيت كلمة المرور)', 'error');
                return;
            }

            try {
                showToast('جاري إرسال الرابط...', 'success');
                const res = await fetch('api/forgot_password.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });
                const data = await res.json();
                if(data.success) {
                    showToast('تم الإرسال! راجع بريدك الإلكتروني', 'success');
                } else {
                    showToast(data.message, 'error');
                }
            } catch(err) {
                showToast('حدث خطأ', 'error');
            }
        });
    });

});

// Check auth status on page load
async function checkAuthStatus() {
    try {
        const res = await fetch('api/check_auth.php');
        const data = await res.json();
        if (data.loggedIn) {
            updateUIAfterLogin(data.user);
        }
    } catch(err) {
        console.log("Not logged in");
    }
}

// Update UI
function updateUIAfterLogin(user) {
    const hdrUser = document.querySelector('.hdr-user');
    if(hdrUser) {
        hdrUser.innerHTML = `
            <span style="font-weight:bold; color:var(--p)">👤 أهلاً ${user.name.split(' ')[0]}</span>
            <span>|</span>
            ${user.role === 'admin' ? '<a href="admin.php" class="hdr-link-btn" style="color:#f59e0b;font-weight:700;">⚙️ الإدارة</a> <span>|</span>' : ''}
            <a href="#" onclick="logoutUser()" class="hdr-link-btn" style="color:#ef4444;">خروج</a>
        `;
    }
}

// Logout
async function logoutUser() {
    try {
        await fetch('api/logout.php');
        window.location.reload();
    } catch(err) {
        window.location.reload();
    }
}

// 4. Handle Google Login
const GOOGLE_CLIENT_ID = '244006724557-a845r5ljc7rutv6hht4m1kr537de3r42.apps.googleusercontent.com';

window.onload = function () {
    // Note: The google GIS script must be loaded. We rely on the script tag in index.html.
    if(typeof google !== 'undefined' && google.accounts) {
        google.accounts.id.initialize({
            client_id: GOOGLE_CLIENT_ID,
            callback: handleGoogleResponse
        });

        const loginContainer = document.getElementById('google-login-container');
        if(loginContainer) {
            google.accounts.id.renderButton(
                loginContainer,
                { theme: "outline", size: "large", width: 300, text: "signin_with" }
            );
        }

        const signupContainer = document.getElementById('google-signup-container');
        if(signupContainer) {
            google.accounts.id.renderButton(
                signupContainer,
                { theme: "outline", size: "large", width: 300, text: "signup_with" }
            );
        }

        // Optional: Also display the One Tap dialog
        // google.accounts.id.prompt();
    }
};

async function handleGoogleResponse(response) {
    try {
        const res = await fetch('api/google_auth.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_token: response.credential })
        });
        const data = await res.json();
        
        if (data.success) {
            showToast('تم تسجيل الدخول بحساب جوجل بنجاح! 👋', 'success');
            updateUIAfterLogin(data.user);
            if(window.closeModal) closeModal('auth');
        } else {
            showToast(data.message, 'error');
        }
    } catch (err) {
        showToast('حدث خطأ في الاتصال بالسيرفر', 'error');
    }
}

# Frontend Structure (HTML/CSS/JavaScript)

## Main Entry Point

**`frontend/index.html`** – Home page (landing)

## File Organization

```
frontend/
├── index.html                      # Home page
├── dashboard.html                  # User dashboard (requires login)
├── auth/
│   ├── register.html              # Registration form
│   ├── login.html                 # Login form
│   └── otp.html                   # OTP verification page
├── quiz/
│   ├── quiz.html                  # Quiz interface with timer & questions
│   ├── results.html               # Results page
│   └── select.html                # (To be created) Select language/level
├── admin/
│   ├── index.html                 # Admin dashboard
│   ├── questions.html             # (To be created) Manage questions
│   ├── users.html                 # (To be created) Manage users
│   └── analytics.html             # (To be created) View analytics
├── styles/
│   ├── global.css                 # Global styles + navbar + buttons
│   ├── home.css                   # Home page styles
│   ├── auth.css                   # Auth pages (register, login, OTP)
│   ├── dashboard.css              # Dashboard styles
│   ├── quiz.css                   # Quiz interface styles
│   ├── results.css                # Results page styles
│   └── admin.css                  # Admin panel styles
├── js/
│   ├── auth.js                    # Auth utilities (checkAuth, logout, getAuthHeader)
│   ├── dashboard.js               # Dashboard initialization
│   ├── quiz.js                    # Quiz logic (display, timer, submit)
│   └── results.js                 # Results logic
└── Dockerfile                      # (To be created) Container for frontend build
```

## Key Features

- **Responsive Design**: Mobile-first with Tailwind-like utility CSS
- **Glassmorphism**: Backdrop blur effects on navbar + cards
- **Smooth Animations**: CSS transitions on buttons, links
- **CSRF Protected**: OTP verification includes CSRF token exchange
- **JWT Authentication**: Tokens stored in localStorage
- **Monaco Editor**: (To be integrated) For coding questions

## Entry Flow

1. User opens `index.html` (home page)
2. Clicks "Register" → `auth/register.html`
3. Fills form, submits → Backend sends OTP via EmailJS
4. Redirected to `auth/otp.html?email=...`
5. Enters OTP → Account verified
6. Redirected to `auth/login.html`
7. Logs in → Redirected to `dashboard.html`
8. Clicks "Start Quiz" → `quiz/select.html` (to be created) → `quiz/quiz.html`
9. After quiz → `quiz/results.html`

## Styling Approach

- Purple gradient theme: `#667eea → #764ba2`
- Cards: White with subtle shadow
- Buttons: Gradient primary, outlined secondary
- Forms: Clean, minimal, focused states with glow

## To Complete

- [ ] Quiz selection page (language, level dropdown)
- [ ] Quiz history page
- [ ] Leaderboard page
- [ ] Admin pages (manage questions, users, view analytics)
- [ ] Monaco Editor integration for coding questions
- [ ] Framer Motion animations (optional)
- [ ] Toast notifications for errors/success
- [ ] Loading skeletons

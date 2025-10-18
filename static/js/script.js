document.addEventListener("DOMContentLoaded", function () {
  initializeAlerts();
  initializeNavigation();
  initializeFormValidation();
  initializeWeatherWidget();
  initializeQuizFeatures();
});

function initializeAlerts() {
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach((alert) => {
    setTimeout(() => {
      if (alert && alert.parentNode) {
        alert.style.transition = "opacity 0.5s";
        alert.style.opacity = "0";
        setTimeout(() => {
          if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
          }
        }, 500);
      }
    }, 5000);
  });
}

function initializeNavigation() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });
}

function initializeFormValidation() {
  const registerForm = document.querySelector('form[action*="register"]');
  if (registerForm) {
    const usernameInput = registerForm.querySelector('input[name="username"]');
    const passwordInput = registerForm.querySelector('input[name="password"]');
    const confirmPasswordInput = registerForm.querySelector(
      'input[name="confirm_password"]'
    );

    if (usernameInput) {
      usernameInput.addEventListener("input", function () {
        const username = this.value.trim();
        const feedback =
          this.parentNode.querySelector(".username-feedback") ||
          createFeedbackElement(this.parentNode, "username-feedback");

        if (username.length < 3) {
          this.classList.add("is-invalid");
          feedback.textContent = "Username minimal 3 karakter";
          feedback.className = "username-feedback text-danger small";
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
          this.classList.add("is-invalid");
          feedback.textContent =
            "Username hanya boleh mengandung huruf, angka, dan underscore";
          feedback.className = "username-feedback text-danger small";
        } else {
          this.classList.remove("is-invalid");
          this.classList.add("is-valid");
          feedback.textContent = "Username tersedia";
          feedback.className = "username-feedback text-success small";
        }
      });
    }

    if (passwordInput && confirmPasswordInput) {
      function validatePasswordMatch() {
        const feedback =
          confirmPasswordInput.parentNode.querySelector(".password-feedback") ||
          createFeedbackElement(
            confirmPasswordInput.parentNode,
            "password-feedback"
          );

        if (passwordInput.value !== confirmPasswordInput.value) {
          confirmPasswordInput.classList.add("is-invalid");
          feedback.textContent = "Password tidak cocok";
          feedback.className = "password-feedback text-danger small";
        } else if (confirmPasswordInput.value.length > 0) {
          confirmPasswordInput.classList.remove("is-invalid");
          confirmPasswordInput.classList.add("is-valid");
          feedback.textContent = "Password cocok";
          feedback.className = "password-feedback text-success small";
        }
      }

      passwordInput.addEventListener("input", validatePasswordMatch);
      confirmPasswordInput.addEventListener("input", validatePasswordMatch);
    }
  }
}

function createFeedbackElement(parent, className) {
  const feedback = document.createElement("div");
  feedback.className = className;
  parent.appendChild(feedback);
  return feedback;
}

function initializeWeatherWidget() {
  const cityInput = document.querySelector('input[name="city"]');
  if (cityInput) {
    const popularCities = [
      "Jakarta",
      "Surabaya",
      "Bandung",
      "Medan",
      "Semarang",
      "Makassar",
    ];

    cityInput.addEventListener("focus", function () {
      if (!document.querySelector(".city-suggestions")) {
        const suggestions = document.createElement("div");
        suggestions.className = "city-suggestions mt-2";
        suggestions.innerHTML = `
                    <small class="text-muted">Kota populer:</small><br>
                    ${popularCities
                      .map(
                        (city) =>
                          `<button type="button" class="btn btn-sm btn-outline-primary me-1 mb-1 city-btn">${city}</button>`
                      )
                      .join("")}
                `;

        this.parentNode.appendChild(suggestions);

        suggestions.querySelectorAll(".city-btn").forEach((btn) => {
          btn.addEventListener("click", function () {
            cityInput.value = this.textContent;
            suggestions.remove();
          });
        });
      }
    });

    document.addEventListener("click", function (e) {
      if (
        !e.target.closest('.form-control[name="city"]') &&
        !e.target.closest(".city-suggestions")
      ) {
        const suggestions = document.querySelector(".city-suggestions");
        if (suggestions) suggestions.remove();
      }
    });
  }
}

function initializeQuizFeatures() {
  const quizForm = document.getElementById("quiz-form");
  if (quizForm) {
    document.addEventListener("keydown", function (e) {
      if (e.key >= "1" && e.key <= "4") {
        const options = ["A", "B", "C", "D"];
        const optionIndex = parseInt(e.key) - 1;
        const radioButton = document.getElementById(
          `option_${options[optionIndex].toLowerCase()}`
        );
        if (radioButton) {
          radioButton.checked = true;
          radioButton.focus();
        }
      } else if (e.key === "Enter" && e.target.type !== "submit") {
        e.preventDefault();
        const submitBtn = document.getElementById("submit-btn");
        if (submitBtn && !submitBtn.disabled) {
          submitBtn.click();
        }
      }
    });

    const radioButtons = quizForm.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
      radio.addEventListener("change", function () {
        radioButtons.forEach((r) => {
          r.closest(".form-check").classList.remove("selected-option");
        });

        this.closest(".form-check").classList.add("selected-option");
      });
    });
  }

  if (window.location.pathname.includes("leaderboard")) {
    setInterval(function () {
      console.log("Leaderboard auto-refresh check...");
    }, 30000);
  }
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  notification.style.cssText =
    "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 5000);
}

function formatTemperature(temp) {
  return Math.round(temp) + "°C";
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  const months = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
  ];

  return `${days[date.getDay()]}, ${date.getDate()} ${
    months[date.getMonth()]
  } ${date.getFullYear()}`;
}

function startQuizTimer(duration = 300) {
  const timerElement = document.getElementById("quiz-timer");
  if (!timerElement) return;

  let timeLeft = duration;
  const timer = setInterval(() => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    timerElement.textContent = `${minutes}:${seconds
      .toString()
      .padStart(2, "0")}`;

    if (timeLeft <= 0) {
      clearInterval(timer);
      showNotification("Waktu habis!", "warning");
    }

    timeLeft--;
  }, 1000);
}

function updateProgress() {
  const progressBar = document.querySelector(".progress-bar");
  if (progressBar) {
    const currentScore = parseInt(
      document.getElementById("current-score")?.textContent || "0"
    );
    const maxScore = 100;
    const progress = Math.min((currentScore / maxScore) * 100, 100);

    progressBar.style.width = progress + "%";
    progressBar.setAttribute("aria-valuenow", progress);
  }
}

function saveUserPreference(key, value) {
  try {
    localStorage.setItem("quizApp_" + key, JSON.stringify(value));
  } catch (e) {
    console.log("Unable to save to localStorage:", e);
  }
}

function getUserPreference(key, defaultValue = null) {
  try {
    const item = localStorage.getItem("quizApp_" + key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (e) {
    console.log("Unable to read from localStorage:", e);
    return defaultValue;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const cityInput = document.querySelector('input[name="city"]');
  if (cityInput && !cityInput.value) {
    const savedCity = getUserPreference("lastCity", "Jakarta");
    cityInput.value = savedCity;
  }

  const weatherForm = document.querySelector('form[action*="home"]');
  if (weatherForm) {
    weatherForm.addEventListener("submit", function () {
      const cityInput = this.querySelector('input[name="city"]');
      if (cityInput) {
        saveUserPreference("lastCity", cityInput.value);
      }
    });
  }
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", function () {
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn && !submitBtn.classList.contains("no-loading")) {
      submitBtn.disabled = true;
      const originalText = submitBtn.textContent;
      submitBtn.textContent = "Memproses...";

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      }, 5000);
    }
  });
});
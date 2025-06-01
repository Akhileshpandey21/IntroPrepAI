document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const closeButton = document.getElementById("close-menu-button");
    const mobileMenu = document.getElementById("mobile-menu");
    const menuLinks = document.querySelectorAll("#mobile-menu a"); // Select all links inside the menu


    if (menuButton && closeButton && mobileMenu) {
      menuButton.addEventListener("click", function () {
        mobileMenu.classList.remove("hidden");
      });

      closeButton.addEventListener("click", function () {
        mobileMenu.classList.add("hidden");
      });

        // Automatically close menu when any link is clicked
        menuLinks.forEach(link => {
          link.addEventListener("click", function () {
              mobileMenu.classList.add("hidden");
          });
      });
    }
  });


   // Set the current year in the footer dynamically
document.getElementById('current-year').textContent = new Date().getFullYear();

const backToTopBtn = document.getElementById("backToTopBtn");

// Show button when user scrolls down
window.onscroll = function () {
    if (window.scrollY > 300) {
        backToTopBtn.classList.remove("opacity-0", "invisible");
    } else {
        backToTopBtn.classList.add("opacity-0", "invisible");
    }
};

// Scroll to top function
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}
setTimeout(function () {
  document.querySelectorAll(".success-alert").forEach(alert => {
    alert.remove(); // Removes all success alerts after 2 seconds
  });
}, 2000);


//dropdown home

document.addEventListener("DOMContentLoaded", function () {
  const dropdownBtn = document.getElementById("userDropdownBtn");
  const dropdownMenu = document.getElementById("userDropdownMenu");

  dropdownBtn.addEventListener("click", function () {
      dropdownMenu.classList.toggle("hidden");
  });

  // Close dropdown when clicking outside
  document.addEventListener("click", function (event) {
      if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
          dropdownMenu.classList.add("hidden");
      }
  });
});


//dropdown mobile
document.addEventListener("DOMContentLoaded", function () {
    const dropdownBtn = document.getElementById("mobileUserDropdownBtn");
    const dropdownMenu = document.getElementById("mobileUserDropdownMenu");

    if (dropdownBtn && dropdownMenu) {
        dropdownBtn.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevents click from propagating and closing the menu
            dropdownMenu.classList.toggle("hidden");
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function (event) {
            if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.add("hidden");
            }
        });
    }
});


// // Theme switcher
// document.addEventListener("DOMContentLoaded", function () {
//     const html = document.documentElement;
//     const themeToggle = document.getElementById("theme-toggle");
//     const themeDropdown = document.getElementById("theme-dropdown");
//     const themeIcon = document.getElementById("theme-icon");
//     const themeText = document.getElementById("theme-text");
  
//     // Retrieve saved theme
//     const currentTheme = localStorage.getItem("theme") || "light-mode";
//     applyTheme(currentTheme);
  
//     function applyTheme(theme) {
//       html.classList.remove("dark-mode", "light-mode");
//       html.classList.add(theme);
//       localStorage.setItem("theme", theme);
  
//       // Update button icon & text
//       if (theme === "dark-mode") {
//         themeIcon.textContent = "🌙";
//         themeText.textContent = "";
//       } else {
//         themeIcon.textContent = "🌞";
//         themeText.textContent = "";
//       }
//     }
  
//     // Theme selection function
//     window.setMode = function (theme) {
//       applyTheme(theme);
//       themeDropdown.classList.add("hidden");
//     };
  
//     // Show dropdown on button click
//     themeToggle.addEventListener("click", () => {
//       themeDropdown.classList.toggle("hidden");
//     });
  
//     // Close dropdown when clicking outside
//     document.addEventListener("click", (event) => {
//       if (!themeToggle.contains(event.target) && !themeDropdown.contains(event.target)) {
//         themeDropdown.classList.add("hidden");
//       }
//     });
//   });

const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {
  navLinks.classList.toggle("hidden");
  menuBtnIcon.className = navLinks.classList.contains("hidden")
    ? "ri-menu-line"
    : "ri-close-line";
});

ScrollReveal().reveal("header h1", { origin: "bottom", distance: "40px", duration: 1000 });
ScrollReveal().reveal("header p", { delay: 300, origin: "bottom", distance: "40px", duration: 1000 });
ScrollReveal().reveal("form", { delay: 500, origin: "bottom", distance: "40px", duration: 1000 });
ScrollReveal().reveal("header img", { delay: 700, origin: "right", distance: "60px", duration: 1000 });


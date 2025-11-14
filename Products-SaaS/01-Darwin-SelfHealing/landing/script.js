// Copy install command
function copyInstall() {
  const text = "pip install darwin-healing";
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(".copy-btn");
    const originalHTML = btn.innerHTML;
    btn.innerHTML = "✓";
    setTimeout(() => {
      btn.innerHTML = originalHTML;
    }, 2000);
  });
}

// Smooth scroll
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

// Animate on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observe all sections
document.querySelectorAll("section").forEach((section) => {
  section.style.opacity = "0";
  section.style.transform = "translateY(20px)";
  section.style.transition = "all 0.6s ease-out";
  observer.observe(section);
});

// Terminal typing effect
function typeTerminal() {
  const terminals = document.querySelectorAll(".demo-terminal");
  terminals.forEach((terminal) => {
    const lines = terminal.querySelectorAll(".terminal-line");
    lines.forEach((line, index) => {
      line.style.opacity = "0";
      setTimeout(() => {
        line.style.opacity = "1";
        line.style.animation = "fadeIn 0.5s ease-out";
      }, index * 500);
    });
  });
}

// Run on scroll to demo
const demoObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        typeTerminal();
        entry.target.dataset.animated = "true";
      }
    });
  },
  { threshold: 0.5 }
);

const demo = document.querySelector(".solution-demo");
if (demo) {
  demoObserver.observe(demo);
}

// Add fadeIn animation
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);

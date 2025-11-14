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

// Scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -100px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Animate sections on scroll
document
  .querySelectorAll(
    ".problem-card, .feature-card, .pricing-card, .benefit-item"
  )
  .forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "all 0.6s ease-out";
    observer.observe(el);
  });

// Copy code to clipboard
function copyCode(btn) {
  const codeBlock = btn.previousElementSibling;
  const code = codeBlock.textContent || codeBlock.innerText;

  navigator.clipboard
    .writeText(code)
    .then(() => {
      const originalText = btn.textContent;
      btn.textContent = "✓ Copied!";
      btn.style.background = "#10b981";

      setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = "";
      }, 2000);
    })
    .catch((err) => {
      console.error("Failed to copy:", err);
    });
}

// Navbar background on scroll
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.style.background = "rgba(15, 23, 42, 0.95)";
    navbar.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.3)";
  } else {
    navbar.style.background = "rgba(15, 23, 42, 0.8)";
    navbar.style.boxShadow = "none";
  }
});

// Simulate real-time terminal updates
function updateTerminal() {
  const agentRows = document.querySelectorAll(".agent-row");
  const messageBus = document.querySelector(".message-bus");

  if (!agentRows.length || !messageBus) return;

  // Randomly update agent metrics
  setInterval(() => {
    const randomAgent = agentRows[Math.floor(Math.random() * agentRows.length)];
    const metric = randomAgent.querySelector(".agent-metric");

    if (metric && Math.random() > 0.7) {
      // Simulate metric change
      const currentText = metric.textContent;
      metric.style.opacity = "0.5";
      setTimeout(() => {
        metric.style.opacity = "1";
      }, 300);
    }
  }, 3000);

  // Add new messages periodically
  const sampleMessages = [
    { from: "Archivus", type: "INFO", content: "Indexed 847 new documents" },
    {
      from: "Pulse",
      type: "SUCCESS",
      content: "All services healthy · 100% uptime",
    },
    { from: "Helix", type: "INFO", content: "Deploy #848 started · ETA 12s" },
    { from: "Atlas", type: "INFO", content: "Strategy optimization complete" },
    {
      from: "AgentHub",
      type: "INFO",
      content: "Auto-scaling: worker pool balanced",
    },
  ];

  let messageIndex = 0;
  setInterval(() => {
    const messagesContainer =
      messageBus.querySelector(".bus-message").parentElement;
    const messages = messagesContainer.querySelectorAll(".bus-message");

    // Remove oldest message if more than 3
    if (messages.length >= 3) {
      messages[0].remove();
    }

    // Add new message
    const msg = sampleMessages[messageIndex % sampleMessages.length];
    const now = new Date();
    const time = now.toTimeString().split(" ")[0];

    const newMessage = document.createElement("div");
    newMessage.className = "bus-message";
    if (msg.type === "SUCCESS") newMessage.classList.add("success");

    newMessage.innerHTML = `
            <span class="msg-time">${time}</span>
            <span class="msg-from">${msg.from}</span>
            <span class="msg-type">${msg.type}</span>
            <span class="msg-content">${msg.content}</span>
        `;

    messagesContainer.appendChild(newMessage);
    messageIndex++;
  }, 5000);
}

// Initialize terminal simulation
if (document.querySelector(".demo-terminal")) {
  updateTerminal();
}

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = [
  "ArrowUp",
  "ArrowUp",
  "ArrowDown",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "ArrowLeft",
  "ArrowRight",
  "b",
  "a",
];

document.addEventListener("keydown", (e) => {
  konamiCode.push(e.key);
  konamiCode = konamiCode.slice(-10);

  if (konamiCode.join(",") === konamiSequence.join(",")) {
    const heroTitle = document.querySelector(".hero-title");
    if (heroTitle) {
      heroTitle.innerHTML = `
                O Command Center<br>
                <span class="gradient-text">BATUTA MODE ACTIVATED 🎯</span>
            `;
      document.body.style.animation = "rainbow 3s infinite";
    }
  }
});

// Add rainbow animation
const style = document.createElement("style");
style.textContent = `
@keyframes rainbow {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}
`;
document.head.appendChild(style);

console.log(
  "%c🎯 AgentHub",
  "font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
);
console.log(
  "%cBuilt by Framework BATUTA Team",
  "color: #64748b; font-size: 12px;"
);
console.log(
  "%cTry the Konami Code: ↑↑↓↓←→←→BA",
  "color: #10b981; font-size: 10px;"
);

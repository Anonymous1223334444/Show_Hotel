const cursorDot = document.querySelector("[data-cursor-dot]");
const cursorOutline = document.querySelector("[data-cursor-outline]");

window.addEventListener("mousemove", function (e) {
  const posX = e.clientX;
  const posY = e.clientY;

  cursorDot.style.left = `${posX}px`;
  cursorDot.style.top = `${posY}px`;

  // cursorOutline.style.left = `${posX}px`;
  // cursorOutline.style.top = `${posY}px`;

  cursorOutline.animate(
    {
      left: `${posX}px`,
      top: `${posY}px`,
    },
    { duration: 500, fill: "forwards" }
  );
});

const btns = document.querySelectorAll("#side_btn");
btns.forEach(btn => {
  btn.addEventListener("click", function(e) {
    e.preventDefault();
    const current_active = document.querySelector("#side_btn");
    if (current_active) {
      current_active.classList.remove("btn-active");
    }
    btn.classList.add("btn-active");
    // Redirection to url
    setTimeout(function() {
      window.location.href = btn.dataset.url;
    }, 50);
  });
});
  

const extras = document.querySelectorAll(".btn-extra");
extras.forEach(extra => {
  extra.addEventListener("click", function(e) {
    e.preventDefault();
    const current_active = document.querySelector(".btn-extra");
    if (current_active) {
      current_active.classList.remove("btn-extra-active");
    }
    extra.classList.add("btn-extra-active");
    // Redirection to url
    setTimeout(function() {
      window.location.href = extra.dataset.tab;
    }, 50);
  });
});

const btn_page = document.querySelectorAll(".btn_page");
btn_page.addEventListener("click", function(e) {
  console.log(e.target);
})

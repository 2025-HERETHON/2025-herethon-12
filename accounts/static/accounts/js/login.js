const form = document.querySelector("form");
const username = document.getElementById("username");
const password = document.getElementById("password");
const kakao = document.getElementById("kakao");

kakao.addEventListener("click", () => {
  alert("개발 중인 기능입니다.");
});

// 로그인 잘못되면 테두리 색 변경
window.addEventListener("DOMContentLoaded", () => {
  const msg = document.querySelector(".message");

  if (!msg) return;

  if (msg) {
    username.style.borderColor = "var(--color-red)";
    password.style.borderColor = "var(--color-red)";
  }
});

// 스플래시 스크린 한 번만 뜨게
document.addEventListener("DOMContentLoaded", () => {
  const splash = document.querySelector(".splash-screen");
  if (!sessionStorage.getItem("splashShown")) {
    sessionStorage.setItem("splashShown", "true");
  } else {
    splash.classList.add("hidden");
  }
});

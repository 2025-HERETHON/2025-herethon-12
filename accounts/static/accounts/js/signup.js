const username = document.getElementById("username");
const usernameErr = document.getElementById("username-err");
const password = document.getElementById("password");
const passwordErr = document.getElementById("password-err");
const passwordCheck = document.getElementById("password-check");
const passwordCheckErr = document.getElementById("password-check-err");
const nickname = document.getElementById("nickname");
const nicknameErr = document.getElementById("nickname-err");
const msg = document.querySelector(".message");
const usernameDesc = document.getElementById("username-desc");

function validUsername() {
  if (msg) {
    msg.classList.add("hidden");
  }

  const regex = /^[a-z\d]{4,12}$/;
  let valid = true;
  if (!regex.test(username.value)) {
    valid = false;
    username.style.borderColor = "var(--color-red)";
    usernameErr.classList.remove("hidden");
  } else {
    username.style.borderColor = "#ababab";
    usernameErr.classList.add("hidden");
  }

  return valid;
}

function validPassword() {
  const regex =
    /^(?!^[a-z]+$)(?!^[A-Z]+$)(?!^\d+$)(?!^[^a-zA-Z\d]+$)[a-zA-Z\d\W]{6,20}$/;
  if (!regex.test(password.value)) {
    password.style.border = "1px solid var(--color-red)";
    passwordErr.classList.remove("hidden");
  } else {
    password.style.border = "none";
    passwordErr.classList.add("hidden");
  }
}

function checkPassword() {
  if (password.value !== passwordCheck.value) {
    passwordCheck.style.border = "1px solid var(--color-red)";
    passwordCheckErr.classList.remove("hidden");
  } else {
    passwordCheck.style.border = "none";
    passwordCheckErr.classList.add("hidden");
  }
}

function validNickname() {
  const regex = /^[a-zA-Z\dㄱ-ㅎㅏ-ㅣ가-힣]{2,10}$/;
  if (!regex.test(nickname.value)) {
    nickname.style.borderColor = "var(--color-red)";
    nicknameErr.classList.remove("hidden");
  } else {
    nickname.style.borderColor = "#ababab";
    nicknameErr.classList.add("hidden");
  }
}

// 아이디 중복 확인 로직
function checkId() {
  document.getElementById("password").removeAttribute("required");
  document.getElementById("password-check").removeAttribute("required");
  document.getElementById("nickname").removeAttribute("required");

  const form = document.querySelector("form");

  // 초기화
  const exist = form.querySelector('input[name="action"]');
  if (exist) {
    exist.remove();
  }

  const actionInput = document.createElement("input");
  actionInput.type = "hidden";
  actionInput.name = "action";
  actionInput.value = "check_id";
  form.appendChild(actionInput);
  // 아이디 중복확인 전에도 아이디 유효성 검사 먼저
  const usernameValid = validUsername();
  if (usernameValid) {
    form.submit();
  }
}

function restoreRequired() {
  document.getElementById("password").setAttribute("required", "true");
  document.getElementById("password-check").setAttribute("required", "true");
  document.getElementById("nickname").setAttribute("required", "true");
  usernameDesc.classList.remove("hidden");
  username.style.borderColor = "#ababab";
  msg.classList.add("hidden");
}

// 중복 확인 후 아이디 입력창 테두리 색 변경
window.addEventListener("DOMContentLoaded", () => {
  if (!msg) return;

  if (msg.classList.contains("error")) {
    username.style.borderColor = "var(--color-red)";
    usernameDesc.classList.add("hidden");
  } else if (msg.classList.contains("success")) {
    username.style.borderColor = "#4EC789";
    usernameDesc.classList.add("hidden");
  }
});

username.addEventListener("input", validUsername);
password.addEventListener("input", validPassword);
passwordCheck.addEventListener("input", checkPassword);
nickname.addEventListener("input", validNickname);

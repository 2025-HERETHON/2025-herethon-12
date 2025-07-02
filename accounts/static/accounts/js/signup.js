const username = document.getElementById("username");
const usernameErr = document.getElementById("username-err");
const password = document.getElementById("password");
const passwordErr = document.getElementById("password-err");
const passwordCheck = document.getElementById("password-check");
const passwordCheckErr = document.getElementById("password-check-err");
const nickname = document.getElementById("nickname");
const nicknameErr = document.getElementById("nickname-err");

function validUsername() {
  const regex = /^[a-z\d]{4,12}$/;
  if (!regex.test(username.value)) {
    username.style.borderColor = "var(--color-red)";
    usernameErr.classList.remove("hidden");
  } else {
    username.style.borderColor = "#ababab";
    usernameErr.classList.add("hidden");
  }
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

username.addEventListener("input", validUsername);
password.addEventListener("input", validPassword);
passwordCheck.addEventListener("input", checkPassword);
nickname.addEventListener("input", validNickname);

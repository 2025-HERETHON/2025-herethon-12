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
const form = document.querySelector("form");
const idChecked = document.getElementById("idChecked");

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
  let valid = true;
  if (!regex.test(password.value)) {
    valid = false;
    password.style.border = "1px solid var(--color-red)";
    passwordErr.classList.remove("hidden");
  } else {
    password.style.border = "none";
    passwordErr.classList.add("hidden");
  }
  return valid;
}

function checkPassword() {
  let valid = true;
  if (password.value !== passwordCheck.value) {
    valid = false;
    passwordCheck.style.border = "1px solid var(--color-red)";
    passwordCheckErr.classList.remove("hidden");
  } else {
    passwordCheck.style.border = "none";
    passwordCheckErr.classList.add("hidden");
  }
  return valid;
}

function validNickname() {
  const regex = /^[a-zA-Z\dㄱ-ㅎㅏ-ㅣ가-힣]{2,10}$/;
  let valid = true;
  if (!regex.test(nickname.value)) {
    valid = false;
    nickname.style.borderColor = "var(--color-red)";
    nicknameErr.classList.remove("hidden");
  } else {
    nickname.style.borderColor = "#ababab";
    nicknameErr.classList.add("hidden");
  }
  return valid;
}

// 아이디 중복 확인 로직
function checkId() {
  // 아이디 중복확인 전에도 아이디 유효성 검사 먼저
  if (!validUsername()) return;
  document.getElementById("password").removeAttribute("required");
  document.getElementById("password-check").removeAttribute("required");
  document.getElementById("nickname").removeAttribute("required");

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
  form.submit();
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
    idChecked.value = "false";
  } else if (msg.classList.contains("success")) {
    username.style.borderColor = "#4EC789";
    usernameDesc.classList.add("hidden");
    idChecked.value = "true";
  }
});

username.addEventListener("input", () => {
  validUsername();
  idChecked.value = "false"; // 중복확인 이후에 아이디 값이 바뀌면 재확인
});
password.addEventListener("input", validPassword);
passwordCheck.addEventListener("input", checkPassword);
nickname.addEventListener("input", validNickname);

// 제출 시 필수항목 확인
form.addEventListener("submit", (e) => {
  e.preventDefault();
  restoreRequired();

  const valid =
    validUsername() && validPassword() && checkPassword() && validNickname();

  // 중복확인 없이 회원가입 진행할 경우
  if (idChecked.value === "false") {
    alert("아이디 중복확인을 진행해 주세요.");
    usernameDesc.classList.remove("hidden");
    return;
  }

  if (valid && idChecked.value === "true") {
    form.submit();
  }
});

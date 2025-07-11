const edit = document.getElementById("edit");
const preview = document.querySelector(".preview-img");
const msg = document.querySelector(".message");
const username = document.getElementById("username");
const usernameErr = document.getElementById("username-err");
const nickname = document.getElementById("nickname");
const nicknameErr = document.getElementById("nickname-err");
const form = document.querySelector("form");
const idChecked = document.getElementById("idChecked");
const originalUsername = document.getElementById("original-username").value;

// 프로필 사진 미리보기 함수
function renderPreview(photo) {
  // 초기화
  preview.classList.add("hidden");

  const reader = new FileReader();
  reader.onload = (e) => {
    const previewImg = preview.querySelector("img");
    previewImg.src = e.target.result;
    preview.classList.remove("hidden");
  };
  reader.readAsDataURL(photo);
}

edit.addEventListener("change", () => {
  const profiles = Array.from(edit.files);
  if (profiles.length > 1) {
    alert("사진은 1장만 업로드할 수 있습니다.");
    edit.value = "";
    return;
  }

  renderPreview(profiles[0]);
});

// 여기부턴 signup.js에서 그대로 가져옴 -> 연동 과정에서 수정 가능
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

  document.getElementById("nickname").removeAttribute("required");

  // 중복확인 input 초기화
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
  document.getElementById("nickname").setAttribute("required", "true");
  if (msg) {
    msg.classList.add("hidden");
  }
}

// 중복 확인 후 아이디 입력창 테두리 색 변경
window.addEventListener("DOMContentLoaded", () => {
  if (!msg) return;

  if (msg.classList.contains("error")) {
    username.style.borderColor = "var(--color-red)";
    idChecked.value = "false";
  } else if (msg.classList.contains("success")) {
    username.style.borderColor = "#4EC789";
    idChecked.value = "true";
  }
});

username.addEventListener("input", () => {
  validUsername();
  if (username.value === originalUsername) {
    idChecked.value = "true"; // 아이디 값이 바뀌어도 기존 아이디와 같으면 그대로 true
  } else {
    idChecked.value = "false"; // 중복확인 이후에 아이디 값이 바뀌면 재확인 (중복확인 안 하면 그대로 true)
  }
});
nickname.addEventListener("input", validNickname);

// 제출 시 필수항목 확인
form.addEventListener("submit", (e) => {
  e.preventDefault();
  restoreRequired();

  const valid = validUsername() && validNickname();

  // 중복확인 없이 아이디 변경 진행할 경우
  if (idChecked.value === "false") {
    alert("아이디 중복확인을 진행해 주세요.");
    return;
  }

  if (valid && idChecked.value === "true") {
    form.submit();
  }
});

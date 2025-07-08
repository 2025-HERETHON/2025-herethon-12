const edit = document.getElementById("edit")
const prev = document.querySelector(".preview")
const preview = document.querySelector(".preview-img")
const msg = document.querySelector(".message");
const username = document.getElementById("username");
const usernameErr = document.getElementById("username-err");
const nickname = document.getElementById("nickname");
const nicknameErr = document.getElementById("nickname-err");

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
  const profiles = Array.from(edit.files)
  if (profiles.length > 1) {
    alert("사진은 1장만 업로드할 수 있습니다.");
    edit.value = "";
    return;
  }

  renderPreview(profiles[0]);
})


// 여기부턴 signup.js에서 그대로 가져옴 -> 연동 과정에서 수정 가능
function validUsername() {
  if (msg) {
    msg.classList.add("hidden")
  }

  const regex = /^[a-z\d]{4,12}$/;
  if (!regex.test(username.value)) {
    username.style.borderColor = "var(--color-red)";
    usernameErr.classList.remove("hidden");
  } else {
    username.style.borderColor = "#ababab";
    usernameErr.classList.add("hidden");
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
    document.getElementById("nickname").removeAttribute("required");

    const form = document.querySelector("form");

    const actionInput = document.createElement("input");
    actionInput.type = "hidden";
    actionInput.name = "action";
    actionInput.value = "check_id";
    form.appendChild(actionInput);

    form.submit();
}

function restoreRequired() {
  document.getElementById("nickname").setAttribute("required", "true");
  msg.classList.add("hidden");
}

// 중복 확인 후 아이디 입력창 테두리 색 변경
window.addEventListener("DOMContentLoaded", () => {
  if (!msg) return;

  if (msg.classList.contains("error")) {
    username.style.borderColor = "var(--color-red)";
  } else if (msg.classList.contains("success")) {
    username.style.borderColor = "#4EC789";
  }
})

username.addEventListener("input", validUsername);
nickname.addEventListener("input", validNickname);
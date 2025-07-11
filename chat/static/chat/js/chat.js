const darken = document.querySelector(".darken");
const completeModal = document.querySelector(".complete-modal");
const cancel = document.getElementById("cancel");
const completeBtn = document.getElementById("complete-btn");
const imgInput = document.getElementById("img-input");
const ok = document.getElementById("ok");
const preview = document.querySelector(".img-preview");
const previewDarken = document.querySelector(".preview-darken");

const successModal = document.querySelector(".success-modal");
const check = document.getElementById("check");

console.log("isCompleted 값:", isCompleted);

// 모달창 닫는 함수
function closeAll() {
  completeModal.classList.add("hidden");
  if (successModal.classList.contains("hidden")) {
    darken.classList.add("hidden");
  }
}

// 사진 미리보기 함수
function renderPreview(photo) {
  // 초기화
  preview.classList.add("hidden");
  previewDarken.classList.add("hidden");

  const reader = new FileReader();
  reader.onload = (e) => {
    const previewImg = preview.querySelector("img");
    previewImg.src = e.target.result;

    preview.classList.remove("hidden");
    previewDarken.classList.remove("hidden");
  };
  reader.readAsDataURL(photo);
}

// 거래완료 버튼 누르면 화면 어두워지고 모달창 뜸
completeBtn.addEventListener("click", (e) => {
  if (isCompleted) return;

  e.stopPropagation();
  darken.classList.remove("hidden");
  completeModal.classList.remove("hidden");
});

// 화면 모달창 닫히게 하기 위해, e 상위요소 전파 막음
completeModal.addEventListener("click", (e) => {
  e.stopPropagation();
});

// 취소 버튼 누르거나, 화면 다른 부분 누르면 모달창 닫힘
document.addEventListener("click", closeAll);
cancel.addEventListener("click", closeAll);

// ✅ 네 버튼을 눌렀을 때 기존 모달창 닫고 거래 완료 모달창 열기
ok.addEventListener("click", () => {
  completeModal.classList.add("hidden"); // 모달 닫기

  // 거래 완료 모달 열기
  successModal.classList.remove("hidden");
});

// 폼은 거래 완료 모달의 확인 버튼 눌러야 submit 됨 (다른 버튼으로 안 닫히게)
check.addEventListener("click", () => {
  successModal.classList.add("hidden");
  darken.classList.add("hidden");
});

// 사진 여러 장 업로드 금지
imgInput.addEventListener("change", () => {
  const photos = Array.from(imgInput.files);
  if (photos.length > 1) {
    alert("사진은 1장만 업로드할 수 있습니다.");
    imgInput.value = "";
    return;
  }
  // 사진 미리보기
  renderPreview(photos[0]);
});

// 입력 없을 경우 전송되지 않게 (여전히 전송됨.. 해결해야함) => 해결 완료!
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".chat-input");
  const textInput = document.getElementById("text-input");
  const imgInput = document.getElementById("img-input");
  const sendBtn = document.getElementById("send-btn");

  // 초기화
  textInput.removeAttribute("disabled");
  textInput.removeAttribute("readonly");

  // 사진 파일이 올라와 있으면 text 입력은 못하게
  imgInput.addEventListener("change", () => {
    textInput.setAttribute("readonly", true);
    // text도 같이 보내진다고 착각하지 않게 입력창 비움
    textInput.value = "";
    // 나중에 사진 삭제하는 기능이 만약에,, 나와서 사진 삭제되면 다시 text 입력할 수 있게
    //   if (imgInput.files.length > 0) {
    //   textInput.setAttribute("readonly", true);
    //   textInput.value = "";
    // } else {
    //   textInput.removeAttribute("readonly");
    // }
  });

  sendBtn.addEventListener("click", function (e) {
    const text = textInput.value.trim();
    const image = imgInput.files[0];

    // 현재 템플릿 조건문이 image 먼저 체크하므로 text image 둘 다 올리면 image만 올라가게
    if (text && image) {
      textInput.setAttribute("disabled", true);
    }

    if (!text && !image) {
      // alert 없이 조용히 전송 막기
      e.preventDefault();
      form.style.borderColor = "var(--color-red)"; // 경고 표시로 input창 테두리 색 변경
    } else {
      form.style.borderColor = "#bebebe"; // 테두리 색 원상복구
      preview.classList.add("hidden");
      previewDarken.classList.add("hidden");
    }
  });

  // 거래 완료 상태 확인 (버튼 색 변경)
  if (isCompleted) {
    completeBtn.style.backgroundColor = "#8A8A8A"; // 거래완료 시 회색 버튼 됨
  }
});

// 리다이렉트 시 최신 채팅으로 스크롤 이동
window.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const anchor = document.getElementById("scroll-anchor");
    anchor?.scrollIntoView({ behavior: "auto" });
  }, 50); // 일부러 지연시켜서 타이밍 어긋나지 않게
});



completeBtn.addEventListener("click", (e) => {
  console.log("거래 완료 버튼 클릭됨");
  if (isCompleted) {
    console.log("이미 완료된 거래입니다.");
    return;
  }

  e.stopPropagation();
  console.log("모달 열기 시도 중...");
  darken.classList.remove("hidden");
  completeModal.classList.remove("hidden");
});
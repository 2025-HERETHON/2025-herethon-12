const darken = document.querySelector(".darken");
const completeModal = document.querySelector(".complete-modal");
const cancel = document.getElementById("cancel");
const completeBtn = document.getElementById("complete-btn");
const imgInput = document.getElementById("img-input");
const ok = document.getElementById("ok");

// 모달창 닫는 함수
function closeAll() {
  darken.classList.add("hidden");
  completeModal.classList.add("hidden");
}

// 거래완료 버튼 누르면 화면 어두워지고 모달창 뜸
completeBtn.addEventListener("click", (e) => {
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

// ✅ 네 버튼을 눌렀을 때도 모달창 닫기
ok.addEventListener("click", () => {
  closeAll();  // 모달 닫기
  // 폼은 그대로 submit 됨
});

// 사진 여러 장 업로드 금지
imgInput.addEventListener("change", () => {
  const photos = Array.from(imgInput.files);
  if (photos.length > 1) {
    alert("사진은 1장만 업로드할 수 있습니다.");
    imgInput.value = "";
    return;
  }
});

// 입력 없을 경우 전송되지 않게 (여전히 전송됨.. 해결해야함)
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".chat-input");
  const textInput = document.getElementById("text-input");
  const imgInput = document.getElementById("img-input");

  form.addEventListener("submit", function (e) {
    const text = textInput.value.trim();
    const image = imgInput.files[0];

    if (!text && !image) {
      // alert 없이 조용히 전송 막기
      e.preventDefault();
    }
  });
});
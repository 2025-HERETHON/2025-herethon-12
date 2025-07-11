const logoutBtn = document.querySelector(".logout");
const darken = document.querySelector(".darken");
const logoutModal = document.querySelector(".logout-modal");
const cancel = document.getElementById("cancel");
const ok = document.getElementById("ok");

// 전체 모달창 닫는 함수
function closeAll() {
  logoutModal.classList.add("hidden");
  darken.classList.add("hidden");
}

// 로그아웃 버튼 누르면 화면 어두워지고 모달 뜸
logoutBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  logoutModal.classList.remove("hidden");
  darken.classList.remove("hidden");
});

// 화면 모달창 누르면 안 닫히게 e 상위요소 전파 막음
logoutModal.addEventListener("click", (e) => {
  e.stopPropagation();
});

// 취소 버튼 누르거나, 화면 다른 부분 누르면 모달창 닫힘
document.addEventListener("click", closeAll);
cancel.addEventListener("click", closeAll);

// ✅ 네 버튼을 눌렀을 때도 모달창 닫기 => submit은 됨
ok.addEventListener("click", () => {
  closeAll(); // 모달 닫기
});

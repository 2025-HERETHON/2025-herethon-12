const logoutBtn = document.querySelector(".logout");
const darken = document.querySelector(".darken");
const logoutModal = document.querySelector(".logout-modal");
const cancel = document.getElementById("cancel");
const ok = document.getElementById("ok");
const logoutForm = document.getElementById("logout-form");

// 전체 모달창 닫는 함수
function closeAll() {
  logoutModal?.classList.add("hidden");
  darken?.classList.add("hidden");
}

// 로그아웃 버튼 누르면 화면 어두워지고 모달 뜸
logoutBtn?.addEventListener("click", (e) => {
  e.preventDefault();
  e.stopPropagation();
  logoutModal?.classList.remove("hidden");
  darken?.classList.remove("hidden");
});

// 모달창 클릭 시 닫히는 것 방지
logoutModal?.addEventListener("click", (e) => {
  e.stopPropagation();
});

// 취소 버튼 누르거나 바깥 클릭 시 닫기
document.addEventListener("click", closeAll);
cancel?.addEventListener("click", closeAll);

// ✅ 확인(네) 버튼 누르면 form 제출로 로그아웃 실행
ok?.addEventListener("click", () => {
  logoutForm?.submit(); // 진짜 로그아웃 요청!
});

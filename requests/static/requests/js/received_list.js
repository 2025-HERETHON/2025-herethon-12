const darken = document.querySelector(".darken");
const rejectModal = document.querySelector(".reject-modal");
const cancel = document.getElementById("cancel");
const rejects = document.querySelectorAll(".reject");
const dropdown = document.querySelector(".mini-dropdown");
const selected = document.querySelector(".selected");
const options = document.querySelector(".options");

// 모달창 닫는 함수
function closeAll() {
  darken.classList.add("hidden");
  rejectModal.classList.add("hidden");
}

// 거절 버튼 누르면 모달창 나오고, 다른 화면 어두워짐
rejects.forEach((reject) => {
  reject.addEventListener("click", (e) => {
    e.stopPropagation();
    darken.classList.remove("hidden");
    rejectModal.classList.remove("hidden");
  });
});

// 화면 모달창 닫히게 하기 위해, e 상위요소 전파 막음
rejectModal.addEventListener("click", (e) => {
  e.stopPropagation();
});

// 취소 버튼 누르거나, 화면 다른 부분 누르면 모달창 모두 닫힘
document.addEventListener("click", closeAll);
cancel.addEventListener("click", closeAll);

// 드롭다운 누르면 열리고 다시 누르면 닫힘
selected.addEventListener("click", (e) => {
  e.stopPropagation();
  options.classList.toggle("hidden");
});

// 드롭다운 열린 상태에서 드롭다운 제외 영역 누르면 닫힘
document.addEventListener("click", () => {
  if (!options.classList.contains("hidden")) {
    options.classList.add("hidden");
  }
});

const darken = document.querySelector(".darken");
const rejectModal = document.querySelector(".reject-modal");
const cancel = document.getElementById("cancel");
const rejects = document.querySelectorAll(".reject");

// 드롭다운, 모달창 닫는 함수
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

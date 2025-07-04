const imgContainer = document.querySelector(".img-box");
const dots = document.querySelectorAll(".dot");
const moreBtn = document.querySelector(".more-btn");
const dropdown = document.querySelector(".header-dropdown");
const deleteBtn = document.querySelector(".dropdown-delete");
const darken = document.querySelector(".darken");
const deleteModal = document.querySelector(".delete-modal");
const cancel = document.getElementById("cancel");

// 이미지 부분에 인디케이터(점 모양) 추가
imgContainer.addEventListener("scroll", () => {
  const index = Math.round(imgContainer.scrollLeft / imgContainer.clientWidth);
  dots.forEach((dot, i) => {
    dot.classList.toggle("dot-active", i === index);
  });
});

// 드롭다운, 모달창 닫는 함수
function closeAll() {
  dropdown.classList.add("hidden");
  darken.classList.add("hidden");
  deleteModal.classList.add("hidden");
}

// 더보기 버튼 누르면 드롭다운 나옴
moreBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  dropdown.classList.toggle("hidden");
});

// 드롭다운에서 삭제 버튼 누르면 모달창 나오고, 다른 화면 어두워짐
deleteBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  darken.classList.remove("hidden");
  deleteModal.classList.remove("hidden");
});

// 화면 다른 부분 누르면 드롭다운, 모달창 닫히게 하기 위해, e 상위요소 전파 막음
dropdown.addEventListener("click", (e) => {
  e.stopPropagation();
});
deleteModal.addEventListener("click", (e) => {
  e.stopPropagation();
});

// 취소 버튼 누르거나, 화면 다른 부분 누르면 드롭다운, 모달창 모두 닫힘
document.addEventListener("click", closeAll);
cancel.addEventListener("click", closeAll);

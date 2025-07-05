const dropdown = document.querySelector(".mini-dropdown");
const selected = document.querySelector(".selected");
const options = document.querySelector(".options");

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

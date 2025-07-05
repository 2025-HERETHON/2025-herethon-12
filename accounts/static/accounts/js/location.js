const region = document.getElementById("region");
const submitBtn = document.querySelector(".submit-btn");

// 추후 조건에 맞는 함수로 수정 필요
region.addEventListener("input", () => {
  if (region.value) {
    submitBtn.style.backgroundColor = "var(--color-main)";
  } else {
    submitBtn.style.backgroundColor = "#8A8A8A";
  }
});

submitBtn.addEventListener("click", () => {
  submitBtn.style.backgroundColor = "var(--color-deep-main)";
});

const mainForm = document.querySelector(".main-form");
const place = document.getElementById("place");
const placeErr = document.getElementById("place-err");
const desc = document.getElementById("description");
const descErr = document.getElementById("desc-err");
const darken = document.querySelector(".darken");
const modal = document.querySelector(".modal");

// 필수항목 제어
place.addEventListener("input", () => {
  const placeValue = place.value.trim();
  if (!placeValue || placeValue.length > 12) {
    place.style.borderColor = "var(--color-red)";
    placeErr.classList.remove("hidden");
  } else {
    place.style.borderColor = "#bcbcbc";
    placeErr.classList.add("hidden");
  }
});

desc.addEventListener("input", () => {
  const descValue = desc.value.trim();
  if (!descValue || descValue.length > 200) {
    desc.style.borderColor = "var(--color-red)";
    descErr.classList.remove("hidden");
  } else {
    desc.style.borderColor = "#bcbcbc";
    descErr.classList.add("hidden");
  }
});

// 제출 시 필수항목 확인
mainForm.addEventListener("submit", (e) => {
  let valid = true;

  const placeValue = place.value.trim();
  if (!placeValue || placeValue.length > 12) {
    valid = false;
    e.preventDefault();
    place.style.borderColor = "var(--color-red)";
    placeErr.classList.remove("hidden");
  }

  const descValue = desc.value.trim();
  if (!descValue || descValue.length > 200) {
    valid = false;
    e.preventDefault();
    desc.style.borderColor = "var(--color-red)";
    descErr.classList.remove("hidden");
  }

  // 정상적으로 submit 된다면 완료 모달창 띄움
  if (valid) {
    darken.classList.remove("hidden");
    modal.classList.remove("hidden");
  }
});

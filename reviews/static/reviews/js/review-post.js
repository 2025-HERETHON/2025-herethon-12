const mainForm = document.querySelector(".main-form");
const rateWrap = document.querySelector(".rating");
const labels = document.querySelectorAll(".rating-label");
const input = document.querySelectorAll(".rating-label input");
const labelsLength = labels.length;
const stars = document.querySelectorAll(".star-icon");
const desc = document.getElementById("description");
const descErr = document.getElementById("desc-err");
const photoInput = document.getElementById("photo-input");

checkedRate(); // 새로고침할 때 별점 기본값 채움

// e.target보다 index가 낮은 .star-icon에 .filled 추가
function filledRate(index) {
  for (let i = 0; i <= index; i++) {
    stars[i].classList.add("star-icon-filled");
  }
}

// 선택된 radio보다 index 낮은 radio에 별점 active
function checkedRate() {
  initStars();
  const checked = document.querySelector(".rating-label input:checked");
  if (!checked) return;

  const index = [...input].indexOf(checked);
  filledRate(index);
}

// 별점 초기화
function initStars() {
  for (let i = 0; i < stars.length; i++) {
    stars[i].classList.remove("star-icon-filled");
  }
}

// hover시 별 채워진 걸로 보임
stars.forEach((starIcon, index) => {
  starIcon.addEventListener("mouseenter", () => {
    initStars();
    filledRate(index);
  });
});

// 별 선택 시 채워진 걸로 보임
input.forEach((radio) => {
  radio.addEventListener("change", () => {
    checkedRate();
  });
});

// 마우스가 별점 영역 벗어나면 선택된 상태로 남김
rateWrap.addEventListener("mouseleave", () => {
  checkedRate();
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

photoInput.addEventListener("change", () => {
  const photos = Array.from(photoInput.files);
  if (photos.length > 1) {
    alert("사진은 1장만 업로드할 수 있습니다.");
    photoInput.value = "";
    return;
  }
});

mainForm.addEventListener("submit", (e) => {
  const descValue = desc.value.trim();
  if (!descValue || descValue.length > 200) {
    e.preventDefault();
    desc.style.borderColor = "var(--color-red)";
    descErr.classList.remove("hidden");
  }
});

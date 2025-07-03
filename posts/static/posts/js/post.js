const mainForm = document.querySelector(".main-form");
const photoInput = document.getElementById("photo-input");
const photoErr = document.getElementById("photo-err");
const category = document.getElementById("category");
const categorySelected = document.querySelector(".category-selected");
const place = document.getElementById("place");
const placeErr = document.getElementById("place-err");
const title = document.getElementById("title");
const titleErr = document.getElementById("title-err");
const desc = document.getElementById("description");
const descErr = document.getElementById("desc-err");
const tradeTypes = document.getElementsByName("trade_type");
const typeLabels = document.querySelectorAll(".btn-label");
const typeErr = document.getElementById("type-err");

// 사진 3장 넘어가면 첨부 못하게
photoInput.addEventListener("change", () => {
  const photos = Array.from(photoInput.files); // photo-input에 올라간 사진 파일 배열
  if (photos.length > 3) {
    alert("사진은 최대 3장까지 업로드할 수 있습니다.");
    photoInput.value = "";
    return;
  }

  if (photos.length >= 1 && photos.length <= 3) {
    photoErr.classList.add("hidden");
  }
});

category.addEventListener("change", () => {
  const categoryValue = category.value;
  if (!categoryValue) {
    categorySelected.style.borderColor = "var(--color-red)";
  }
});

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

title.addEventListener("input", () => {
  const titleValue = title.value.trim();
  if (!titleValue || titleValue.length > 12) {
    title.style.borderColor = "var(--color-red)";
    titleErr.classList.remove("hidden");
  } else {
    title.style.borderColor = "#bcbcbc";
    titleErr.classList.add("hidden");
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

tradeTypes.forEach((type) => {
  type.addEventListener("change", () => {
    if (type.checked) {
      typeLabels.forEach((label) => {
        label.style.borderColor = "#bcbcbc";
        typeErr.classList.add("hidden");
      });
    }
  });
});

// 모든 드롭다운 닫는 함수
function closeDropdowns() {
  document.querySelectorAll(".options").forEach((option) => {
    option.classList.add("hidden");
  });
}

// 모든 드롭다운에 이벤트 리스너 추가
document.querySelectorAll(".dropdown").forEach((dropdown) => {
  const selected = dropdown.querySelector(".selected");
  const options = dropdown.querySelector(".options");
  const hiddenInput = dropdown.querySelector(".hidden-input");
  const placeholder = hiddenInput.placeholder;
  const name = selected.querySelector("p");
  const arrow = selected.querySelector("img");

  // 드롭다운 누르면 열림
  selected.addEventListener("click", (e) => {
    e.stopPropagation();
    if (options.classList.contains("hidden")) {
      closeDropdowns();
      name.textContent = placeholder; // 드롭다운 열 때마다 타이틀 보이게
      hiddenInput.value = ""; // 드롭다운 값 초기화
      arrow.classList.remove("hidden"); // 타이틀 옆에 있는 화살표도 보이게
      options.classList.remove("hidden");
      options.scrollIntoView({ behavior: "smooth" });
    } else {
      options.classList.add("hidden");
    }
  });

  options.addEventListener("click", (e) => {
    const item = e.target.closest(".item"); // 클릭한 항목 선언
    if (item) {
      const text = item.textContent;
      name.textContent = text; // 클릭한 항목으로 보이게
      arrow.classList.add("hidden"); // 항목 선택했으므로 화살표 숨김
      hiddenInput.value = text; // 드롭다운마다 숨겨둔 input에 value 보냄
      options.classList.add("hidden");
      categorySelected.style.borderColor = "#bcbcbc";
    }
  });
});

// 드롭다운 타이틀 부분 제외 누르면 닫히게
document.addEventListener("click", () => {
  closeDropdowns();
});

// 제출 시 필수항목 확인
mainForm.addEventListener("submit", (e) => {
  const photos = Array.from(photoInput.files);
  if (photos.length < 1) {
    e.preventDefault();
    photoErr.classList.remove("hidden");
  }

  if (!category.value) {
    e.preventDefault();
    categorySelected.style.borderColor = "var(--color-red)";
  }

  const placeValue = place.value.trim();
  if (!placeValue || placeValue.length > 12) {
    e.preventDefault();
    place.style.borderColor = "var(--color-red)";
    placeErr.classList.remove("hidden");
  }

  const titleValue = title.value.trim();
  if (!titleValue || titleValue.length > 12) {
    e.preventDefault();
    title.style.borderColor = "var(--color-red)";
    titleErr.classList.remove("hidden");
  }

  const descValue = desc.value.trim();
  if (!descValue || descValue.length > 200) {
    e.preventDefault();
    desc.style.borderColor = "var(--color-red)";
    descErr.classList.remove("hidden");
  }

  if (!tradeTypes[0].checked && !tradeTypes[1].checked) {
    typeLabels.forEach((label) => {
      label.style.borderColor = "var(--color-red)";
      typeErr.classList.remove("hidden");
    });
  }
});

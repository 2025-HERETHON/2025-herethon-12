const mainForm = document.querySelector(".main-form");
const photoInput = document.getElementById("photo-input");
const photoStatus = document.querySelector(".photo-input-status");
const photoErr = document.getElementById("photo-err");
const previews = document.querySelectorAll(".photo-preview");
const unknowns = document.querySelectorAll(".photo-preview-unknown");

// 현재 화면 기준으로 카운트
const currentCount = () =>
  Array.from(previews).filter((prev) => !prev.classList.contains("hidden"))
    .length;

let allPhotos = [];

document.addEventListener("DOMContentLoaded", () => {
  photoStatus.textContent = `${currentCount()}/3`;
});

// 미리보기 렌더링
function renderPreview(photos) {
  const startIndex = currentCount(); // 원래 있던 사진의 카운트 고정
  let loaded = 0; // 로딩 카운터
  photos.forEach((photo, i) => {
    const targetIndex = startIndex + i;
    if (targetIndex >= 3) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      previews[targetIndex].querySelector("img").src = e.target.result;
      previews[targetIndex].classList.remove("hidden");
      unknowns[targetIndex].classList.add("hidden");
      loaded++;
      if (loaded === photos.length) {
        // 모든 이미지 로딩 끝나야 카운트 갱신
        photoStatus.textContent = `${currentCount()}/3`;
      }
    };
    reader.readAsDataURL(photo);
  });
}

photoInput.addEventListener("change", () => {
  const photos = Array.from(photoInput.files);
  const current = currentCount();
  const remain = 3 - current;

  if (photos.length > remain) {
    alert("사진은 최대 3장까지 업로드할 수 있습니다.");
    photoInput.value = "";
    return;
  }

  allPhotos = allPhotos.concat(photos);
  renderPreview(photos);
  photoInput.value = "";
  if (currentCount() >= 1) photoErr.classList.add("hidden");
});

// 드롭다운 & 필수 항목 검증 로직은 그대로 유지 (간단하게만 정리)
function validateForm() {
  let valid = true;

  const category = document.getElementById("category");
  const place = document.getElementById("place");
  const title = document.getElementById("title");
  const desc = document.getElementById("description");
  const tradeTypes = document.getElementsByName("trade_type");

  const categorySelected = document.querySelector(".category-selected");
  const placeErr = document.getElementById("place-err");
  const titleErr = document.getElementById("title-err");
  const descErr = document.getElementById("desc-err");
  const typeErr = document.getElementById("type-err");
  const typeLabels = document.querySelectorAll(".btn-label");

  if (currentCount() + allPhotos.length < 1) {
    photoErr.classList.remove("hidden");
    valid = false;
  }

  if (!category.value) {
    categorySelected.style.borderColor = "var(--color-red)";
    valid = false;
  }

  if (!place.value.trim() || place.value.length > 12) {
    place.style.borderColor = "var(--color-red)";
    placeErr.classList.remove("hidden");
    valid = false;
  }

  if (!title.value.trim() || title.value.length > 12) {
    title.style.borderColor = "var(--color-red)";
    titleErr.classList.remove("hidden");
    valid = false;
  }

  if (!desc.value.trim() || desc.value.length > 200) {
    desc.style.borderColor = "var(--color-red)";
    descErr.classList.remove("hidden");
    valid = false;
  }

  if (![...tradeTypes].some((t) => t.checked)) {
    typeLabels.forEach(
      (label) => (label.style.borderColor = "var(--color-red)")
    );
    typeErr.classList.remove("hidden");
    valid = false;
  }

  return valid;
}

mainForm.addEventListener("submit", (e) => {
  e.preventDefault();

  if (!validateForm()) return;

  const formData = new FormData(mainForm);
  formData.delete("photos");
  allPhotos.forEach((p) => formData.append("photos", p));

  fetch(mainForm.action, {
    method: "POST",
    body: formData,
  }).then((res) => {
    if (res.redirected) {
      window.location.href = res.url;
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

  // 수정 창에서 이전에 선택된 게 저장되도록
  const inputValue = hiddenInput.value;
  selected.querySelector("p").textContent = inputValue || placeholder;

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

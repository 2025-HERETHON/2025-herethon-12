const mainForm = document.querySelector(".main-form");
const photoInput = document.getElementById("photo-input");
const photoStatus = document.querySelector(".photo-input-status");
const photoErr = document.getElementById("photo-err");
const previews = document.querySelectorAll(".photo-preview");
const unknowns = document.querySelectorAll(".photo-preview-unknown");

const currentCount = () => document.querySelectorAll(".photo-preview:not(.hidden)").length;
let allPhotos = [];

document.addEventListener("DOMContentLoaded", () => {
  photoStatus.textContent = `${currentCount()}/3`;
});

// 미리보기 렌더링
function renderPreview(photos) {
  photos.forEach((photo, i) => {
    const targetIndex = currentCount() + i;
    if (targetIndex >= 3) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      previews[targetIndex].querySelector("img").src = e.target.result;
      previews[targetIndex].classList.remove("hidden");
      unknowns[targetIndex].classList.add("hidden");
    };
    reader.readAsDataURL(photo);
  });
}

photoInput.addEventListener("change", () => {
  const photos = Array.from(photoInput.files);
  const remain = 3 - currentCount() - allPhotos.length;

  if (photos.length > remain) {
    alert("사진은 최대 3장까지 업로드할 수 있습니다.");
    photoInput.value = "";
    return;
  }

  allPhotos = allPhotos.concat(photos);
  photoStatus.textContent = `${currentCount() + allPhotos.length}/3`;
  renderPreview(photos);
  photoInput.value = "";
  if (currentCount() + allPhotos.length >= 1) photoErr.classList.add("hidden");
});


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
    typeLabels.forEach((label) => label.style.borderColor = "var(--color-red)");
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

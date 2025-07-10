// 별점 후기 페이지는 로직 필요 없어서 지웠습니다
//   // 별점 기능
//   const rateWrap = document.querySelector(".rating");
//   const labels = document.querySelectorAll(".rating-label");
//   const input = document.querySelectorAll(".rating-label input");
//   const stars = document.querySelectorAll(".star-icon");

//   function filledRate(index) {
//     for (let i = 0; i <= index; i++) {
//       stars[i].classList.add("star-icon-filled");
//     }
//   }

//   function initStars() {
//     for (let i = 0; i < stars.length; i++) {
//       stars[i].classList.remove("star-icon-filled");
//     }
//   }

//   function checkedRate() {
//     initStars();
//     const checked = document.querySelector(".rating-label input:checked");
//     if (!checked) return;
//     const index = [...input].indexOf(checked);
//     filledRate(index);
//   }

//   checkedRate();

//   stars.forEach((starIcon, index) => {
//     starIcon.addEventListener("mouseenter", () => {
//       initStars();
//       filledRate(index);
//     });
//   });

//   input.forEach((radio) => {
//     radio.addEventListener("change", () => {
//       checkedRate();
//     });
//   });

//   rateWrap.addEventListener("mouseleave", () => {
//     checkedRate();
//   });

// 입력 페이지가 아닌데 이 부분도 필요가 할까요...?
document.addEventListener("DOMContentLoaded", () => {
  // 후기 입력 유효성 검사
  const mainForm = document.querySelector(".main-form");
  const desc = document.getElementById("description");
  const descErr = document.getElementById("desc-err");
  const photoInput = document.getElementById("photo-input");
  const darken = document.querySelector(".darken");
  const modal = document.querySelector(".modal");

  desc?.addEventListener("input", () => {
    const descValue = desc.value.trim();
    if (!descValue || descValue.length > 200) {
      desc.style.borderColor = "var(--color-red)";
      descErr?.classList.remove("hidden");
    } else {
      desc.style.borderColor = "#bcbcbc";
      descErr?.classList.add("hidden");
    }
  });

  photoInput?.addEventListener("change", () => {
    const photos = Array.from(photoInput.files);
    if (photos.length > 1) {
      alert("사진은 1장만 업로드할 수 있습니다.");
      photoInput.value = "";
    }
  });

  mainForm?.addEventListener("submit", (e) => {
    const descValue = desc.value.trim();
    if (!descValue || descValue.length > 200) {
      e.preventDefault();
      desc.style.borderColor = "var(--color-red)";
      descErr?.classList.remove("hidden");
    } else {
      darken?.classList.remove("hidden");
      modal?.classList.remove("hidden");
    }
  });

  // 삭제 모달 기능
  const deleteBtns = document.querySelectorAll(".delete-btn");
  const confirmDeleteBtn = document.getElementById("confirmDelete");
  const cancelDeleteBtn = document.getElementById("cancelDelete");
  const modalOverlay = document.getElementById("deleteModal");

  if (!confirmDeleteBtn || !cancelDeleteBtn || !modalOverlay) {
    console.error("❌ 모달 요소가 없습니다. id 확인하세요.");
    return;
  }

  let targetReview = null;

  deleteBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      targetReview = btn.closest(".review-item");
      modalOverlay.classList.remove("hidden");
    });
  });

  confirmDeleteBtn.addEventListener("click", () => {
    if (targetReview) {
      targetReview.remove();
      targetReview = null;
    }
    modalOverlay.classList.add("hidden");
  });

  cancelDeleteBtn.addEventListener("click", () => {
    modalOverlay.classList.add("hidden");
  });

  const ratingBoxes = document.querySelectorAll(".rating-box");

  ratingBoxes.forEach((box) => {
    const scoreBox = box.querySelector(".rating-score");
    const stars = box.querySelectorAll(".star-icon");
    const score = parseFloat(scoreBox.textContent.trim());
    const fill = Math.round(score * 2);

    for (let i = 0; i < stars.length; i++) {
      if (i < fill) {
        stars[i].classList.add("star-icon-filled");
      } else {
        stars[i].classList.remove("star-icon-filled");
      }
    }
  });
});

/* 받은 후기, 작성 후기 드롭다운 */
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
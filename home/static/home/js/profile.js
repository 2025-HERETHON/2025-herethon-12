  const ratingBoxes = document.querySelectorAll(".rating-box");

  ratingBoxes.forEach((box) => {
    const scoreBox = box.querySelector(".rating-score");
    const stars = box.querySelectorAll(".star-icon");
    const score = parseFloat(scoreBox.textContent.trim());
    const fill = Math.round(score * 2);

    for (let i = 0; i < stars.length; i++) {
      if (i < fill) {
        stars[i].classList.add("star-icon-filled");
      } else {3
        stars[i].classList.remove("star-icon-filled");
      }
    }
  });

  
// 토글 함수 
function toggleSection(id) {
  const content = document.getElementById(id);
  content.classList.toggle("collapsed");
}
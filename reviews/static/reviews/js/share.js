document.addEventListener('DOMContentLoaded', function () {
  const dropdown = document.querySelector(".mini-dropdown");
  const selected = dropdown.querySelector(".selected");
  const options = dropdown.querySelector(".options");
  const downIcon = dropdown.querySelector(".down-icon");

  selected.addEventListener("click", (e) => {
    e.stopPropagation();
    options.classList.toggle("hidden");
    downIcon.classList.toggle("hidden");
  });

  document.addEventListener("click", () => {
    if (!options.classList.contains("hidden")) {
      options.classList.add("hidden");
      downIcon.classList.add("hidden");
    }
  });
});

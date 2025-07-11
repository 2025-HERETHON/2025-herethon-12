document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const categoryList = document.getElementById("categoryList");

  if (searchInput && categoryList) {
    searchInput.addEventListener("focus", () => {
      categoryList.classList.remove("hidden");
    });

    searchInput.addEventListener("blur", () => {
      setTimeout(() => categoryList.classList.add("hidden"), 150);
    });
  }
});


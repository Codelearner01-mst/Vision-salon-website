/**
 * gallery.js - Gallery page filter interactivity
 *
 * Handles:
 *   - Filter button toggling (active state)
 *   - Category-based filtering of gallery grid items
 *   - Show/hide items based on selected category or All Styles
 *
 * Depends on: rendered gallery.html template elements with
 *   .filter-btn (buttons) and .gallery-grid-item (items)
 */

document.addEventListener("DOMContentLoaded", function () {
  const filterButtons = document.querySelectorAll(".filter-btn");
  const galleryItems = document.querySelectorAll(".gallery-grid-item");

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      filterButtons.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");

      const filterValue = this.getAttribute("data-filter");

      galleryItems.forEach((item) => {
        const itemCategory = item.getAttribute("data-category");

        if (filterValue === "all" || itemCategory === filterValue) {
          item.classList.remove("hide");
        } else {
          item.classList.add("hide");
        }
      });
    });
  });
});

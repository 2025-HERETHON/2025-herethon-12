document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('reject-modal hidden');
  const cancelBtn = document.getElementById('cancel');
  const confirmForm = document.getElementById('reject-form');
  const rejectButtons = document.querySelectorAll('.reject-button');

  rejectButtons.forEach(button => {
    button.addEventListener('click', function () {
      const actionUrl = this.getAttribute('data-url');
      confirmForm.setAttribute('action', actionUrl);
      modal.classList.remove('hidden');
    });
  });

  cancelBtn.addEventListener('click', function () {
    modal.classList.add('hidden');
  });
});
(function () {
  const savedPosition = sessionStorage.getItem('catalogScrollPosition');
  if (savedPosition) {
    window.scrollTo(0, parseInt(savedPosition, 10));
    sessionStorage.removeItem('catalogScrollPosition');
  }

  const form = document.querySelector('[data-catalog-filters]');
  if (!form) return;

  const selectFields = form.querySelectorAll('select');
  const inputFields = form.querySelectorAll('input[type="search"], input[type="number"]');

  const submitForm = () => {
    sessionStorage.setItem('catalogScrollPosition', String(window.scrollY));
    const pageInput = form.querySelector('input[name="page"]');
    if (pageInput) {
      pageInput.value = '1';
    }
    form.submit();
  };

  selectFields.forEach((field) => {
    field.addEventListener('change', submitForm);
  });

  let debounceTimer;
  inputFields.forEach((field) => {
    field.addEventListener('input', function () {
      window.clearTimeout(debounceTimer);
      debounceTimer = window.setTimeout(submitForm, 600);
    });

    field.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        window.clearTimeout(debounceTimer);
        submitForm();
      }
    });
  });
})();

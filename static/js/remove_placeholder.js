function remove_placeholder(_placeholder = 'Space separated') {
  const skills_length = $('form li').not('.js-template').length;
  const skills_input = document.getElementById('question-input-101');

  if (skills_length === 0) skills_input.placeholder = _placeholder;
  else skills_input.placeholder = '';
}

(function() {
  fetch('https://c4c2d2de-af5f-4a37-b685-424eae62c49b-ide.cs50.xyz:8080/registration');
})();

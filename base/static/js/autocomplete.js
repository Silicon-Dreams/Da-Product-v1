// const searchInput = document.querySelector('#search-input');
// searchInput.addEventListener('input', () => {
//   const query = searchInput.value;
//   fetch(`http://127.0.0.1:8000/products/3ac374db-34b7-440d-93f6-493b6a29aa0b?name__icontains=${query}`)
//     .then(response => response.json())
//     .then(data => {
//       const suggestionsList = document.createElement('ul');
//       data.forEach(productName => {
//         const suggestionItem = document.createElement('li');
//         suggestionItem.textContent = productName;
//         suggestionsList.appendChild(suggestionItem);
//       });
//       // Display suggestionsList below search input
//     })
//     .catch(error => console.error(error));
// });
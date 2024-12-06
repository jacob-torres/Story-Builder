// Update word count
const wordCountLink = document.getElementById('word-count-link');
const wordCountForm = document.getElementById('word-count-form')

// Toggle form visibility for updating story word count
function toggleWordCountForm() {
    var form = document.getElementById('word-count-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Jump to word count form when clicking certain links
wordCountLink.addEventListener('click', () => {
    wordCountForm.style.display = 'block';
});

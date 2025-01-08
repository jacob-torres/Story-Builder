// Update word count
const wordCountLink = document.getElementById('word-count-link');
const wordCountForm = document.getElementById('word-count-form');

// Toggle form visibility for updating story word count
function toggleWordCountForm() {
    wordCountForm.style.display = wordCountForm.style.display === 'none' ? 'block' : 'none';
}

// Jump to word count form when clicking the word count link
wordCountLink.addEventListener('click', () => {
    wordCountForm.style.display = 'block';
});

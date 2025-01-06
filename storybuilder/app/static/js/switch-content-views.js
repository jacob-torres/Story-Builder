// For switching between content views
const viewLinks = document.querySelectorAll('.view-link');
const viewTabs = document.querySelectorAll('.view-tab');
const contentDivs = document.querySelectorAll('.content-view');

// Clicking on a link in the details exposes and jumps to the corresponding view
viewLinks.forEach((link, index) => {
    link.addEventListener('click', () => {

        // Hide all content views
        contentDivs.forEach(div => div.style.display = 'none');

        // Display content view corresponding with the clicked link
        contentDivs[index].style.display = 'block';
    });
});

// Clicking on a tab heading activates the corresponding view
viewTabs.forEach((link, index) => {
    link.addEventListener('click', () => {

        // Remove the active class from each tab
        viewTabs.forEach(link => link.classList.remove('active'));

        // Add the active class back to the tab corresponding to the clicked link
        link.classList.add('active');

        // Hide all view content
        contentDivs.forEach(div => div.style.display = 'none');

        // Show the content corresponding to the clicked link
        contentDivs[index].style.display = 'block';
    });
});
// For switching between content views
const navTabs = document.querySelectorAll('.view-tab');
const contentDivs = document.querySelectorAll('.content-view')

navTabs.forEach((link, index) => {
    link.addEventListener('click', () => {

        // Remove the active class from each tab
        navTabs.forEach(link => link.classList.remove('active'));

        // Add the active class back to the tab corresponding to the clicked link
        link.classList.add('active');

        // Hide all view content
        contentDivs.forEach(div => div.style.display = 'none');

        // Show the content corresponding to the clicked link
        contentDivs[index].style.display = 'block';
    });
});
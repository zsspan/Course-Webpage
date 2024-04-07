document.addEventListener("DOMContentLoaded", function() {
    const alterGradeButtons = document.querySelectorAll('.alter-grade');
    const modal = document.getElementById('gradeModal');
    const closeBtn = modal.querySelector('.close');
    const assignmentNumberSpan = modal.querySelector('#assignmentNumber');
    const remarkInfos = modal.querySelectorAll('.remark-info');
    const forms = modal.querySelectorAll('.grade-form');

    // event listeners for all "Alter Grade" buttons
    alterGradeButtons.forEach((button) => {
        button.addEventListener('click', function() {
            // get assignment information from the clicked button's data attributes
            const assignmentNumber = this.getAttribute('data-number');

            assignmentNumberSpan.textContent = assignmentNumber;

            // display/hide each remark info based on if it matches the assignment number
            remarkInfos.forEach((info) => {
                if (info.getAttribute('data-assignment-number') !== assignmentNumber) {
                    info.classList.add('hidden');
                } else {
                    info.classList.remove('hidden');
                }
            });

            forms.forEach((form) => {
                if (form.getAttribute('data-assignment-number') !== assignmentNumber) {
                    form.classList.add('hidden');
                } else {
                    form.classList.remove('hidden');
                }
            });

            modal.classList.remove('hidden');
        });
    });

    // close when x is pressed
    closeBtn.addEventListener('click', function() {
        modal.classList.add('hidden');
        remarkInfos.forEach((info) => {
            info.classList.remove('hidden');
        });
        forms.forEach((form) => {
            form.classList.remove('hidden');
        });
    });

    // close when user clicks elsewhere
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
            remarkInfos.forEach((info) => {
                info.classList.remove('hidden');
            });
            forms.forEach((form) => {
                form.classList.remove('hidden');
            });
        }
    });
});

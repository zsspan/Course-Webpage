document.addEventListener("DOMContentLoaded", function() {
    const remarkButtons = document.querySelectorAll('.remark-btn');
    const modal = document.getElementById('myModal');
    const closeBtn = modal.querySelector('.close');
    const assignmentIdInput = modal.querySelector('#assignmentId');
    const assignmentNumberSpan = modal.querySelector('#assignmentNumber');
    const studentButtons = document.querySelectorAll('.student-btn');

    // event listeners to all "Request Remark" buttons
    remarkButtons.forEach((button) => {
      button.addEventListener('click', function() {
        // get the assignment number and description from the clicked row
        const assignmentNumber = this.parentNode.parentNode.querySelector('.assignment-number').textContent;
        assignmentIdInput.value = assignmentNumber; 
        assignmentNumberSpan.textContent = assignmentNumber;
        modal.classList.remove('hidden');
      });
    });
  
    // for each student button
    studentButtons.forEach((button) => {
      button.addEventListener('click', function() {
          const username = this.getAttribute('data-student-id');
          window.location.href = `/grades/${username}`;
      });
    });

    // close when x is pressed
    closeBtn.addEventListener('click', function() {
      modal.classList.add('hidden');
    });

    // close when user clicks elsewhere
    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        modal.classList.add('hidden');
      }
  });
  
});

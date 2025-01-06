document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like-btn").forEach(btn =>
    btn.addEventListener("click", () => {
      const count = btn.querySelector(".like-count");
      count.textContent = +count.textContent + (btn.classList.toggle("liked") ? 1 : -1);
    })
  );

  const commentBtns = document.querySelectorAll(".comment-btn");
let commentCount = 0;

commentBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const commentsSection = btn.closest(".post").querySelector(".comments-section");
    const text = prompt("Write your comment:");
    if (text) {
      commentsSection.innerHTML += `<div class='comment'><div class='comment-avatar' style='background:#fff'></div><div class='comment-text'>${text}</div></div>`;
    }
  });
});
});
document.addEventListener("DOMContentLoaded", () => {
  const uploadTrigger = document.getElementById('upload-trigger');
  const uploadOptions = document.getElementById('upload-options');
  const fileInput = document.getElementById('file-input');
  const selectButton = document.getElementById('select-button');
  const fileNameLabel = document.getElementById('file-name');
  const uploadButton = document.getElementById('upload-button');
  let fileSelected = false;

  uploadTrigger.addEventListener('click', () => {
    uploadOptions.style.display = (fileSelected || uploadOptions.style.display === "flex") ? "none" : "flex";
  });

  selectButton.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    fileNameLabel.textContent = fileInput.files.length ? `Datei: ${fileInput.files[0].name}` : "Keine Datei ausgewählt";
    fileSelected = !!fileInput.files.length;
    uploadButton.disabled = !fileSelected;
  });

  uploadButton.addEventListener('click', () => {
    if (fileSelected) {
      fetch('/upload/', {
        method: 'POST',
        body: new FormData(document.getElementById('upload-form'))
      }).then(() => resetForm());
    } else {
      uploadOptions.style.display = "none";
    }
  });

  const resetForm = () => {
    fileInput.value = "";
    fileNameLabel.textContent = "Keine Datei ausgewählt";
    uploadButton.disabled = true;
    uploadOptions.style.display = "none";
    fileSelected = false;
  };
});
document.addEventListener("DOMContentLoaded", () => {
  
  // Alle Buttons zum Kommentieren finden
  const commentSubmitButtons = document.querySelectorAll('.comment-submit-btn');

  commentSubmitButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const commentsSection = e.target.closest('.comments-section');
      const inputField = commentsSection.querySelector('.comment-input');

      const newCommentText = inputField.value.trim();

      if (newCommentText) {
        // Neues Kommentar-Element erstellen
        const newComment = document.createElement('div');
        newComment.className = 'comment';

        const commentAvatar = document.createElement('img');
        commentAvatar.className = 'comment-avatar';
        commentAvatar.src = "https://picsum.photos/30/30";

        const commentText = document.createElement('p');
        commentText.className = 'comment-text';
        commentText.innerHTML = `<strong>You:</strong> ${newCommentText}`;

        newComment.appendChild(commentAvatar);
        newComment.appendChild(commentText);

        // Kommentar unter den bestehenden einfügen
        commentsSection.insertBefore(newComment, inputField.parentElement);

        inputField.value = '';  // Eingabefeld leeren
      }
    });
  });
});


document.querySelectorAll('.profile-container').forEach(item => {
  item.addEventListener('mouseenter', () => {
    const dropdown = item.querySelector('.dropdown-menu');
    if (dropdown) {
      dropdown.style.display = 'block';
    }
  });

  item.addEventListener('mouseleave', () => {
    const dropdown = item.querySelector('.dropdown-menu');
    if (dropdown) {
      dropdown.style.display = 'none';
    }
  });
});

function showEditForm() {
  document.getElementById('profileView').classList.add('hidden');
  document.getElementById('editView').classList.remove('hidden');
}

function goBack() {
  document.getElementById('editView').classList.add('hidden');
  document.getElementById('profileView').classList.remove('hidden');
}

function changeProfilePicture() {
  const input = document.getElementById('uploadPic');
  const image = document.getElementById('profilePicEdit');
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      image.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}

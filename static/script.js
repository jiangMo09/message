function validateForm() {
  var fileInput = document.getElementById("imageInput");
  var file = fileInput.files[0];
  var maxSize = 5 * 1024 * 1024; // 5MB

  if (file) {
    if (file.size > maxSize) {
      alert("圖片大小不能超過 5MB");
      return false;
    }
    if (!file.type.startsWith("image/")) {
      alert("請上傳圖片文件");
      return false;
    }
  }
  return true;
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("postForm");
  const submitButton = form.querySelector('input[type="submit"]');

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (validateForm()) {
      submitForm();
    }
  });

  const validateForm = () => {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];
    const maxSize = 5 * 1024 * 1024; // 5MB

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
  };

  const submitForm = () => {
    const formData = new FormData(form);

    // 禁用提交按鈕並改變文字
    submitButton.disabled = true;
    submitButton.value = "提交中...";

    fetch("/post", {
      method: "POST",
      body: formData
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // 清空表單
          form.reset();
          // 顯示成功消息
          alert("留言發送成功！");
        } else {
          alert("發送留言失敗：" + data.detail);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("發送留言時出錯");
      })
      .finally(() => {
        // 重新啟用提交按鈕並恢復文字
        submitButton.disabled = false;
        submitButton.value = "發送留言";
      });
  };
});

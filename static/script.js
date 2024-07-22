import { fetchData } from "/static/fetchData.js";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("postForm");
  const submitButton = form.querySelector('input[type="submit"]');
  const postList = document.querySelector(".post-list");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    await submitForm();
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

  const submitForm = async () => {
    const formData = new FormData(form);

    submitButton.disabled = true;
    submitButton.value = "提交中...";

    try {
      const response = await fetch("/post", {
        method: "POST",
        body: formData // 直接發送 FormData，不要進行任何轉換
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData));
      }

      const data = await response.json();

      if (data.success) {
        window.location.reload();
      } else {
        alert("發送留言失敗：" + data.detail);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("發送留言時出錯: " + error.message);
    } finally {
      submitButton.disabled = false;
      submitButton.value = "發送留言";
    }
  };
});

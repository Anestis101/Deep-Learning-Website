document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById("photo-upload");
  const formData = new FormData();
  formData.append("photo", fileInput.files[0]);

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Analyzing...";

  try {
      const response = await fetch("http://localhost:5000/analyze", {
          method: "POST",
          body: formData,
      });

      const data = await response.json();
      if (response.ok) {
          resultDiv.innerHTML = `
              <strong>Analysis Result:</strong> ${data.result}<br>
              <small>${data.message}</small>
          `;
      } else {
          resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
      }
  } catch (error) {
      resultDiv.innerHTML = `<strong>Error:</strong> Could not connect to the server.`;
  }
});

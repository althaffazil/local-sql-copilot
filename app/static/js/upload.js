async function uploadCSV() {

    const fileInput =
      document.getElementById(
        "csvFile"
      );
  
    if (!fileInput.files.length) {
  
      alert(
        "Please select a CSV file"
      );
  
      return;
    }
  
    const formData =
      new FormData();
  
    formData.append(
      "file",
      fileInput.files[0]
    );
  
    try {
  
      document.getElementById(
        "uploadStatus"
      ).innerHTML =
        "Uploading...";
  
      const response =
        await fetch(
          `${API_BASE}/upload-csv`,
          {
            method: "POST",
            body: formData
          }
        );
  
      const data =
        await response.json();
  
      if (!data.success) {
  
        document.getElementById(
          "uploadStatus"
        ).innerHTML =
          data.error;
  
        return;
      }
  
      document.getElementById(
        "uploadStatus"
      ).innerHTML =
        "✅ Upload Successful";
  
      renderTableInfo(
        data.table
      );
  
      loadSchema();
  
    } catch(error) {
  
      document.getElementById(
        "uploadStatus"
      ).innerHTML =
        error.message;
    }
  }
  
  function renderTableInfo(table) {
  
    document.getElementById(
      "tableInfo"
    ).innerHTML =
    `
    <div class="alert alert-success">
  
      <strong>Table:</strong>
      ${table.table_name}
  
      <br>
  
      <strong>Rows:</strong>
      ${table.rows}
  
      <br>
  
      <strong>Columns:</strong>
      ${table.columns.join(", ")}
  
    </div>
    `;
  }
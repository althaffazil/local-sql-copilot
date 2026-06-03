async function runQuery() {
  const question = document.getElementById("question").value;

  if (!question.trim()) {
    alert("Please enter a question");

    return;
  }

  addHistory(question);

  document.getElementById("loading").style.display = "block";

  try {
    const response = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    });

    const data = await response.json();

    renderResponse(data);
  } catch (error) {
    document.getElementById("status").innerHTML = "❌ Request Failed";
  } finally {
    document.getElementById("loading").style.display = "none";
  }
}

function renderResponse(data) {
  document.getElementById("originalSql").textContent = data.original_sql || "";

  document.getElementById("finalSql").textContent = data.final_sql || "";

  document.getElementById("confidenceBadge").innerHTML =
    `Confidence: ${data.confidence || "N/A"}`;

  document.getElementById("exportButtons").style.display = "none";
  if (!data.success) {
    document.getElementById("status").innerHTML = "❌ Failed";

    document.getElementById("results").innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
            `;

    document.getElementById("repairInfo").innerHTML = "No execution performed";

    return;
  }

  if (data.repair_count > 0) {
    document.getElementById("status").innerHTML =
      `⚠️ Auto Repaired (${data.repair_count})`;
  } else {
    document.getElementById("status").innerHTML = "✅ Success";
  }

  renderRepairInfo(data);

  document.getElementById("exportButtons").style.display = "block";

  renderTable(data.result);
}

function renderRepairInfo(data) {
  const container = document.getElementById("repairInfo");

  if (!data.attempts || data.attempts.length === 0) {
    container.innerHTML = `
            <div class="alert alert-success">
                No repairs required
            </div>
            `;

    return;
  }

  let html = "";

  data.attempts.forEach((attempt) => {
    html += `
            <div class="card mb-3">

                <div class="card-header">
                    Attempt ${attempt.attempt}
                </div>

                <div class="card-body">

                    <h6>SQL</h6>

                    <pre>${attempt.sql}</pre>

                    <h6>Error</h6>

                    <pre>${attempt.error}</pre>

                </div>

            </div>
            `;
  });

  container.innerHTML = html;
}

function renderTable(result) {
  const container = document.getElementById("results");

  if (!result) {
    container.innerHTML = `
            <div class="alert alert-warning">
                No results returned
            </div>
            `;

    return;
  }

  if (!result.success) {
    container.innerHTML = `
            <div class="alert alert-danger">
                ${result.error}
            </div>
            `;

    return;
  }

  if (!result.rows || result.rows.length === 0) {
    container.innerHTML = `
            <div class="alert alert-info">
                Query executed successfully but returned 0 rows.
            </div>
            `;

    return;
  }

  let html = `
        <div class="table-responsive">

        <table class="table table-striped table-hover table-bordered">
        `;

  html += "<thead><tr>";

  result.columns.forEach((col) => {
    html += `
            <th>${col}</th>
            `;
  });

  html += "</tr></thead>";

  html += "<tbody>";

  result.rows.forEach((row) => {
    html += "<tr>";

    row.forEach((cell) => {
      html += `
                    <td>${cell}</td>
                    `;
    });

    html += "</tr>";
  });

  html += `
        </tbody>
        </table>
        </div>
    `;

  container.innerHTML = html;
}
function exportCSV() {
  window.open(`${API_BASE}/export/csv`, "_blank");
}

function exportExcel() {
  window.open(`${API_BASE}/export/excel`, "_blank");
}

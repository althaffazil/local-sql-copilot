async function loadSchema() {

  try {

      const response =
          await fetch(
              `${API_BASE}/schema`
          );

      const data =
          await response.json();

      renderSchema(
          data.tables
      );

  } catch (error) {

      document.getElementById(
          "schemaExplorer"
      ).innerHTML =
          "Failed to load schema";
  }
}


function renderSchema(
  tables
) {

  const container =
      document.getElementById(
          "schemaExplorer"
      );

  let html = "";

  tables.forEach(
      table => {

          html += `
          <div class="schema-table">

              <div
                  class="d-flex justify-content-between align-items-center">

                  <strong>
                      ${table.table}
                  </strong>

                  <button
                      class="btn btn-sm btn-outline-danger"
                      onclick="
                          deleteTable(
                              '${table.table}'
                          )
                      ">

                      <i class="bi bi-trash"></i>

                  </button>

              </div>
          `;

          table.columns.forEach(
              column => {

                  html += `
                  <div
                      class="schema-column">

                      • ${column.name}
                      (${column.type})

                  </div>
                  `;
              }
          );

          html += `
          </div>
          `;
      }
  );

  container.innerHTML =
      html;
}


async function deleteTable(
  tableName
) {

  const confirmed =
      confirm(
          `Delete table '${tableName}'?`
      );

  if (!confirmed) {
      return;
  }

  try {

      const response =
          await fetch(
              `${API_BASE}/schema/${tableName}`,
              {
                  method: "DELETE"
              }
          );

      const data =
          await response.json();

      if (!data.success) {

          alert(
              data.error
          );

          return;
      }

      loadSchema();

  } catch (error) {

      alert(
          "Failed to delete table."
      );
  }
}
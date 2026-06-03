let sidebarVisible = true;

function toggleSidebar() {

    const sidebar =
        document.getElementById("sidebar");

    const main =
        document.getElementById("mainContent");

    const button =
        document.getElementById("sidebarToggle");

    if (sidebarVisible) {

        sidebar.style.display = "none";

        main.classList.remove("col-md-9");
        main.classList.add("col-md-12");

        button.innerHTML =
            '<i class="bi bi-table"></i> Show Schema';

    } else {

        sidebar.style.display = "block";

        main.classList.remove("col-md-12");
        main.classList.add("col-md-9");

        button.innerHTML =
            '<i class="bi bi-table"></i> Hide Schema';
    }

    sidebarVisible = !sidebarVisible;
}



function clearHistory() {

  document.getElementById(
    "history"
  ).innerHTML = "";
}

function addHistory(question) {

  const history =
    document.getElementById(
      "history"
    );

  const item =
    document.createElement(
      "li"
    );

  item.textContent =
    question;

  history.prepend(
    item
  );
}

function copyText(elementId) {

  const text =
    document.getElementById(
      elementId
    ).innerText;

  navigator.clipboard.writeText(
    text
  );

  const status =
    document.getElementById(
      "status"
    );

  const original =
    status.innerHTML;

  status.innerHTML =
    "📋 SQL Copied";

  setTimeout(() => {

    status.innerHTML =
      original;

  }, 1500);
}
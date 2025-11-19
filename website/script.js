let fullData = [];

fetch('ghc_base_versions.json')
  .then(response => {
    if (!response.ok) throw new Error("Failed to load JSON");
    return response.json();
  })
  .then(data => {
    fullData = data;
    renderTable(data);
  })
  .catch(error => {
    console.error("Error loading JSON:", error);
    const tbody = document.querySelector('#ghc-table tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="2">Failed to load data</td>`;
    tbody.appendChild(tr);
  });

function renderTable(data) {
  const tbody = document.querySelector('#ghc-table tbody');
  tbody.innerHTML = '';
  data.forEach(entry => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${entry.ghc}</td><td>${entry.base || ''}</td>`;
    tbody.appendChild(tr);
  });
}

document.getElementById('filter-box').addEventListener('input', (e) => {
  const text = e.target.value.trim();
  if (text === '') {
    renderTable(fullData);
    return;
  }

  const filtered = fullData.filter(entry =>
    entry.ghc.startsWith(text) || (entry.base && entry.base.startsWith(text))
  );

  renderTable(filtered);
});
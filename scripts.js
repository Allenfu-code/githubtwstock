function loadCSV() {
    const stock_no = document.getElementById('stock-selector').value;
    const csvUrl = `data/${stock_no}.csv`;
  
    Papa.parse(csvUrl, {
      download: true,
      header: true,
      complete: function(results) {
        displayTable(results.data);
      },
      error: function(error) {
        console.error("無法載入 CSV 檔案", error);
      }
    });
  }
  
  function displayTable(data) {
    const tableHead = document.getElementById('table-head');
    const tableBody = document.getElementById('table-body');
  
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';
  
    if(data.length === 0){
      tableBody.innerHTML = '<tr><td colspan="5">無資料</td></tr>';
      return;
    }
  
    // 建立表頭
    const headers = Object.keys(data[0]);
    const headRow = document.createElement('tr');
    headers.forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      headRow.appendChild(th);
    });
    tableHead.appendChild(headRow);
  
    // 填入資料
    data.forEach(row => {
      const tr = document.createElement('tr');
      headers.forEach(header => {
        const td = document.createElement('td');
        td.textContent = row[header];
        tr.appendChild(td);
      });
      tableBody.appendChild(tr);
    });
  }
  
const proposalsData = JSON.parse(document.getElementById('chart-data').dataset.proposals);
const certifiedData = JSON.parse(document.getElementById('chart-data').dataset.certified);
const typesData = JSON.parse(document.getElementById('chart-data').dataset.types);

const proposalsChart = new Chart(document.getElementById('proposalsChart'), {
  type: 'pie',
  data: {
      labels: proposals_data.map(item => item[0]),
      datasets: [{
          data: proposals_data.map(item => item[1]),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
      }]
  }
});

const certifiedClientsChart = new Chart(document.getElementById('certifiedClientsChart'), {
  type: 'bar',
  data: {
      labels: ['Certificados', 'No Certificados'],
      datasets: [{
          data: [certified_jya, uncertified_jya],
          backgroundColor: ['#36A2EB', '#FF6384']
      }]
  }
});

const disabilityTypesChart = new Chart(document.getElementById('disabilityTypesChart'), {
  type: 'pie',
  data: {
      labels: disability_types_data.map(item => item[0]),
      datasets: [{
          data: disability_types_data.map(item => item[1]),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
      }]
  }
});

const clientCategoryChart = new Chart(document.getElementById('clientCategoryChart'), {
  type: 'bar',
  data: {
      labels: disability_data.map(item => item[0]),
      datasets: [{
          data: disability_data.map(item => item[1]),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
      }]
  }
});
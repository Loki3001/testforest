document.getElementById('forestHealthForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        treeHeight: parseFloat(document.getElementById('treeHeight').value),
        dbh: parseFloat(document.getElementById('dbh').value),
        crownWidth: parseFloat(document.getElementById('crownWidth').value),
        soilTN: parseFloat(document.getElementById('soilTN').value),
        soilTP: parseFloat(document.getElementById('soilTP').value),
        soilAP: parseFloat(document.getElementById('soilAP').value),
        fireRiskIndex: parseFloat(document.getElementById('fireRiskIndex').value),
        disturbanceLevel: parseFloat(document.getElementById('disturbanceLevel').value)
    };

    const predictionResult = predictForestHealth(formData);
    
    const resultElement = document.getElementById('predictionResult');
    const detailsElement = document.getElementById('predictionDetails');
    
    resultElement.innerHTML = `Forest Health Status: <span class="${predictionResult.status.toLowerCase().replace('-', '')}">${predictionResult.status}</span>`;
    
    detailsElement.innerHTML = `
        <p>Total Health Score: ${predictionResult.score.toFixed(2)}</p>
        <p>Key Factors:</p>
        <ul>
            ${Object.entries(predictionResult.factors)
                .map(([factor, value]) => `<li>${factor}: ${value > 0 ? 'Positive' : 'Negative'}</li>`)
                .join('')}
        </ul>
    `;
});

function predictForestHealth(data) {
    const healthFactors = {
        treeHeight: data.treeHeight > 10 ? 1 : -1,
        dbh: data.dbh > 30 ? 1 : -1,
        crownWidth: data.crownWidth > 5 ? 1 : -1,
        soilTN: data.soilTN > 0.5 ? 1 : -1,
        soilTP: data.soilTP > 0.3 ? 1 : -1,
        fireRiskIndex: data.fireRiskIndex < 5 ? 1 : -1,
        disturbanceLevel: data.disturbanceLevel < 3 ? 1 : -1
    };

    const totalScore = Object.values(healthFactors).reduce((a, b) => a + b, 0);

    let status;
    if (totalScore > 4) status = 'Healthy';
    else if (totalScore > 0) status = 'Sub-Healthy';
    else status = 'Unhealthy';

    return {
        status: status,
        score: totalScore,
        factors: healthFactors
    };
}
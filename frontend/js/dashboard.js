document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('historyTableBody');
    
    try {
        // Fetch stats
        const stats = await apiClient.getStats();
        if (stats) {
            document.getElementById('statTotal').textContent = stats.total_scans;
            document.getElementById('statLatency').textContent = stats.avg_latency_ms;
            
            // Find most common
            let maxCount = 0;
            let maxClass = '--';
            for (const [cls, count] of Object.entries(stats.disease_distribution)) {
                if (count > maxCount && cls !== 'Healthy') {
                    maxCount = count;
                    maxClass = cls.replace(/_/g, ' ');
                }
            }
            document.getElementById('statCommon').textContent = maxClass;
        }

        // Fetch history
        const history = await apiClient.getHistory(20);
        
        tableBody.innerHTML = '';
        if (!history || history.items.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px;">No scans recorded yet.</td></tr>';
            return;
        }

        history.items.forEach(item => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border)';
            
            const date = new Date(item.created_at).toLocaleString();
            const cls = item.defect_class.replace(/_/g, ' ');
            const conf = (item.confidence * 100).toFixed(1) + '%';
            const lat = item.latency_ms.toFixed(1) + ' ms';
            
            // Highlight healthy vs diseased
            let clsColor = 'var(--text-primary)';
            if (item.defect_class === 'Healthy' || item.defect_class === 'Tomato_healthy') {
                clsColor = 'var(--primary)';
            } else if (item.confidence > 0.8) {
                clsColor = 'var(--danger)';
            }
            
            tr.innerHTML = `
                <td style="padding: 12px; color: var(--text-secondary); font-size: 0.875rem;">${date}</td>
                <td style="padding: 12px; font-weight: 600; color: ${clsColor};">${cls}</td>
                <td style="padding: 12px;">${conf}</td>
                <td style="padding: 12px;" class="mono">${lat}</td>
            `;
            tableBody.appendChild(tr);
        });

    } catch (error) {
        console.error(error);
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px; color: var(--danger);">Failed to load data. Is the backend running?</td></tr>';
    }
});

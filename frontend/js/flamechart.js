window.updateFlameChart = function(prepMs, infMs, postMs) {
    // Round to 1 decimal
    prepMs = Number(prepMs).toFixed(1);
    infMs = Number(infMs).toFixed(1);
    postMs = Number(postMs).toFixed(1);
    
    const totalMs = (parseFloat(prepMs) + parseFloat(infMs) + parseFloat(postMs)).toFixed(1);
    
    // Update labels
    document.getElementById('lblPrep').textContent = prepMs;
    document.getElementById('lblInf').textContent = infMs;
    document.getElementById('lblPost').textContent = postMs;
    document.getElementById('totalLatency').textContent = `${totalMs} ms`;

    // Calculate percentages
    const total = parseFloat(totalMs);
    const prepPct = (prepMs / total) * 100;
    const infPct = (infMs / total) * 100;
    const postPct = (postMs / total) * 100;

    // Animate bars (start at 0, grow to target)
    const barPrep = document.getElementById('barPrep');
    const barInf = document.getElementById('barInf');
    const barPost = document.getElementById('barPost');

    barPrep.style.width = '0%';
    barInf.style.width = '0%';
    barPost.style.width = '0%';

    // Trigger reflow
    void barPrep.offsetWidth;

    // Set new widths
    setTimeout(() => {
        barPrep.style.width = `${prepPct}%`;
        barInf.style.width = `${infPct}%`;
        barPost.style.width = `${postPct}%`;
    }, 50);
};

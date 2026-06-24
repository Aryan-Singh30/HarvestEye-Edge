document.addEventListener('DOMContentLoaded', () => {
    const simulatorTarget = document.getElementById('simulatorTarget');
    
    if (simulatorTarget) {
        simulatorTarget.addEventListener('change', (e) => {
            const val = e.target.value;
            if (val === 'cloud_gpu') {
                console.log("Simulating Cloud GPU (lower inference, higher network latency)");
            } else if (val === 'edge_cpu') {
                console.log("Simulating Edge CPU (INT8 Quantized, no network latency)");
            } else if (val === 'rpi') {
                console.log("Simulating Raspberry Pi 4 (higher inference latency)");
            }
        });
    }
});

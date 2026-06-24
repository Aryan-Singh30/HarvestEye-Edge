// Generates a mock heatmap overlay for demonstration purposes
// In a full production system, the backend would return a binary mask
// which we would render onto this canvas.

window.clearHeatmap = function() {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

window.drawHeatmap = function(imgElement) {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) return;

    // Match canvas size to displayed image size
    canvas.width = imgElement.clientWidth;
    canvas.height = imgElement.clientHeight;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Create a random organic-looking blob to simulate disease segmentation
    const centerX = canvas.width * (0.3 + Math.random() * 0.4);
    const centerY = canvas.height * (0.3 + Math.random() * 0.4);
    const radius = Math.min(canvas.width, canvas.height) * 0.25;

    // Create radial gradient for the heatmap
    const gradient = ctx.createRadialGradient(
        centerX, centerY, radius * 0.1,
        centerX, centerY, radius
    );
    
    // Cargill-warning colors (Yellow to Red)
    gradient.addColorStop(0, 'rgba(220, 53, 69, 0.8)');   // Red center (high severity)
    gradient.addColorStop(0.5, 'rgba(245, 158, 11, 0.6)'); // Yellow/Orange mid
    gradient.addColorStop(1, 'rgba(0, 133, 68, 0.0)');     // Fade to transparent

    ctx.fillStyle = gradient;
    
    // Draw an irregular blob
    ctx.beginPath();
    for (let i = 0; i < Math.PI * 2; i += 0.5) {
        const r = radius * (0.8 + Math.random() * 0.4);
        const x = centerX + Math.cos(i) * r;
        const y = centerY + Math.sin(i) * r;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fill();
};

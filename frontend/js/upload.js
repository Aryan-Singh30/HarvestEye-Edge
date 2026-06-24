document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const cameraInput = document.getElementById('cameraInput');
    
    // UI States
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');
    const resultsState = document.getElementById('resultsState');
    
    // Result Elements
    const previewImage = document.getElementById('previewImage');
    const diseaseName = document.getElementById('diseaseName');
    const confidenceBadge = document.getElementById('confidenceBadge');
    
    // Drag & Drop Handlers
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // File Input Handlers
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    cameraInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    async function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
        }

        // 1. Show Preview & Loading State
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            // Clear previous heatmap
            if(window.clearHeatmap) window.clearHeatmap();
        };
        reader.readAsDataURL(file);

        emptyState.classList.add('hidden');
        resultsState.classList.add('hidden');
        loadingState.classList.remove('hidden');

        try {
            // Apply simulator penalties if any (for realistic demo)
            const target = document.getElementById('simulatorTarget').value;
            
            // 2. Call API
            const result = await apiClient.scanImage(file);
            
            // Artificial delay for simulator if needed
            if (target === 'rpi') {
                await new Promise(r => setTimeout(r, 800)); // RPi is slower
                result.latency.inference_ms *= 12.5; 
            } else if (target === 'cloud_gpu') {
                await new Promise(r => setTimeout(r, 200)); // Network latency
                // GPU is faster but network overhead is high
                result.latency.inference_ms = 8.5; 
                result.latency.preprocessing_ms += 200.0; // Add to prep bar to represent network upload
            }
            
            // 3. Update UI
            diseaseName.textContent = formatClassName(result.defect_class);
            
            const confPercent = (result.confidence * 100).toFixed(1);
            confidenceBadge.textContent = `${confPercent}% Confidence`;
            
            if (result.confidence > 0.9) {
                confidenceBadge.style.color = '#006B36'; // Green
                confidenceBadge.style.backgroundColor = '#E8F5E9';
            } else if (result.confidence > 0.6) {
                confidenceBadge.style.color = '#B45309'; // Yellow/Orange
                confidenceBadge.style.backgroundColor = '#FEF3C7';
            } else {
                confidenceBadge.style.color = '#991B1B'; // Red
                confidenceBadge.style.backgroundColor = '#FEE2E2';
            }
            
            // 4. Update Latency Flame Chart
            if (window.updateFlameChart) {
                window.updateFlameChart(
                    result.latency.preprocessing_ms, 
                    result.latency.inference_ms, 
                    result.latency.postprocessing_ms
                );
            }

            // 5. Draw Heatmap (Simulated for Demo based on confidence)
            previewImage.onload = () => {
                if (window.drawHeatmap && result.defect_class !== 'Healthy' && result.defect_class !== 'Tomato_healthy') {
                    window.drawHeatmap(previewImage);
                }
            };

            // Switch views
            loadingState.classList.add('hidden');
            resultsState.classList.remove('hidden');

        } catch (error) {
            console.error(error);
            alert("Analysis failed. Ensure the backend is running. " + error.message);
            loadingState.classList.add('hidden');
            emptyState.classList.remove('hidden');
        }
    }

    function formatClassName(name) {
        return name.replace(/_/g, ' ');
    }
});

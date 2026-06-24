class HarvestEyeClient {
    constructor() {
        // Use relative path so Nginx reverse proxy handles it
        this.apiBaseUrl = '/api/v1';
    }

    async scanImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.apiBaseUrl}/scan`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to scan image');
            }

            return await response.json();
        } catch (error) {
            console.error("Scan error:", error);
            throw error;
        }
    }

    async getHistory(limit = 10) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/history?limit=${limit}`);
            return await response.json();
        } catch (error) {
            console.error("History fetch error:", error);
            return null;
        }
    }

    async getStats() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/stats`);
            return await response.json();
        } catch (error) {
            console.error("Stats fetch error:", error);
            return null;
        }
    }
}

const apiClient = new HarvestEyeClient();

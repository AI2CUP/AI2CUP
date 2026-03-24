/**
 * ================================================
 * AI2CUP — Frontend JavaScript
 * ================================================
 * Handles all API calls, UI interactions, and data display.
 * Connects to the FastAPI backend at the same origin.
 * ================================================
 */

// ── API Base URL (same origin since FastAPI serves the frontend) ──
const API_BASE = '/api';

// ── State ──
let selectedFile = null;       // Currently selected image file
let currentTab = 'sellers';    // Active marketplace tab
let marketplaceData = null;    // Cached marketplace data

// ================================================
// INITIALIZATION
// ================================================
document.addEventListener('DOMContentLoaded', () => {
    loadMarketplace();  // Load marketplace data on page load
    setupDragAndDrop();  // Enable drag-and-drop for image upload
    setupNavigation();   // Smooth scroll navigation
});

// ================================================
// NAVIGATION
// ================================================
function setupNavigation() {
    document.querySelectorAll('.navbar-nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            document.querySelectorAll('.navbar-nav a').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// ================================================
// TOAST NOTIFICATIONS
// ================================================
function showToast(message, type = 'error') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✅' : '❌';
    toast.innerHTML = `${icon} ${message}`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 4000);
}

// ================================================
// SECTION 1: PRICE PREDICTION
// ================================================
async function predictPrice() {
    const btn = document.getElementById('predictBtn');
    const spinner = document.getElementById('priceSpinner');
    const btnText = document.getElementById('predictBtnText');

    // Gather form values
    const payload = {
        region: document.getElementById('regionSelect').value,
        month: parseInt(document.getElementById('monthSelect').value),
        altitude: parseFloat(document.getElementById('altitudeInput').value),
        rainfall: parseFloat(document.getElementById('rainfallInput').value),
        variety: document.getElementById('varietySelect').value,
    };

    // Show loading state
    btn.disabled = true;
    spinner.classList.add('active');
    btnText.textContent = 'Predicting...';

    try {
        const response = await fetch(`${API_BASE}/predict-price`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Prediction failed');
        }

        const data = await response.json();
        displayPriceResult(data);
        loadMonthlyChart(payload.region, payload.altitude, payload.rainfall, payload.variety);
        showToast('Price prediction complete!', 'success');
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        spinner.classList.remove('active');
        btnText.textContent = '🔮 Predict Price';
    }
}

function displayPriceResult(data) {
    const resultCard = document.getElementById('priceResult');
    resultCard.classList.add('visible');

    document.getElementById('predictedPrice').textContent = `$${data.predicted_price_usd.toFixed(2)}`;

    const detailsEl = document.getElementById('priceResultDetails');
    const inputs = data.inputs;
    detailsEl.innerHTML = `
        <div class="result-detail-item"><div class="result-detail-label">Region</div><div class="result-detail-value">${inputs.region}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Month</div><div class="result-detail-value">${getMonthName(inputs.month)}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Altitude</div><div class="result-detail-value">${inputs.altitude}m</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Rainfall</div><div class="result-detail-value">${inputs.rainfall}mm</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Variety</div><div class="result-detail-value">${inputs.variety}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Model</div><div class="result-detail-value">${data.model_info}</div></div>
    `;
}

// ── Monthly Price Chart ──
async function loadMonthlyChart(region, altitude, rainfall, variety) {
    const chartContainer = document.getElementById('priceChart');
    const chartBars = document.getElementById('chartBars');
    chartBars.innerHTML = '';

    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const prices = [];

    // Fetch predictions for all 12 months
    for (let m = 1; m <= 12; m++) {
        try {
            const res = await fetch(`${API_BASE}/predict-price`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region, month: m, altitude, rainfall, variety }),
            });
            const d = await res.json();
            prices.push(d.predicted_price_usd);
        } catch {
            prices.push(0);
        }
    }

    const maxPrice = Math.max(...prices, 1);

    for (let i = 0; i < 12; i++) {
        const heightPct = (prices[i] / maxPrice) * 100;
        const group = document.createElement('div');
        group.className = 'chart-bar-group';
        group.innerHTML = `
            <div class="chart-bar-value">$${prices[i].toFixed(1)}</div>
            <div class="chart-bar" style="height: ${heightPct}%" title="${months[i]}: $${prices[i].toFixed(2)}/kg"></div>
            <div class="chart-bar-label">${months[i]}</div>
        `;
        chartBars.appendChild(group);
    }

    chartContainer.classList.add('visible');
}

// ================================================
// SECTION 2: QUALITY DETECTION
// ================================================
function setupDragAndDrop() {
    const area = document.getElementById('uploadArea');
    ['dragenter','dragover'].forEach(evt => {
        area.addEventListener(evt, (e) => { e.preventDefault(); area.classList.add('drag-over'); });
    });
    ['dragleave','drop'].forEach(evt => {
        area.addEventListener(evt, (e) => { e.preventDefault(); area.classList.remove('drag-over'); });
    });
    area.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) { processFile(files[0]); }
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) processFile(file);
}

function processFile(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please upload an image file');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        showToast('File too large. Maximum 10MB.');
        return;
    }
    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('uploadPreview').classList.add('visible');
    };
    reader.readAsDataURL(file);

    document.getElementById('analyzeBtn').disabled = false;
}

async function analyzeQuality() {
    if (!selectedFile) { showToast('Please select an image first'); return; }

    const btn = document.getElementById('analyzeBtn');
    const spinner = document.getElementById('qualitySpinner');
    const btnText = document.getElementById('analyzeBtnText');

    btn.disabled = true;
    spinner.classList.add('active');
    btnText.textContent = 'Analyzing...';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(`${API_BASE}/analyze-quality`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Analysis failed');
        }

        const data = await response.json();
        displayQualityResult(data);
        showToast('Quality analysis complete!', 'success');
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        spinner.classList.remove('active');
        btnText.textContent = '🔬 Analyze Quality';
    }
}

function displayQualityResult(data) {
    const resultCard = document.getElementById('qualityResult');
    resultCard.classList.add('visible');

    const badge = document.getElementById('qualityBadge');
    badge.textContent = `${getQualityEmoji(data.quality)} ${data.quality} Quality`;
    badge.className = `quality-badge ${data.quality.toLowerCase()}`;

    document.getElementById('qualityDescription').textContent = data.description;

    const pct = Math.round(data.confidence * 100);
    document.getElementById('confidenceValue').textContent = `${pct}%`;
    setTimeout(() => { document.getElementById('confidenceFill').style.width = `${pct}%`; }, 100);

    const detailsEl = document.getElementById('qualityDetails');
    let html = '';
    if (data.details) {
        for (const [key, val] of Object.entries(data.details)) {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            html += `<div class="result-detail-item"><div class="result-detail-label">${label}</div><div class="result-detail-value">${val}</div></div>`;
        }
    }
    detailsEl.innerHTML = html;
}

// ================================================
// SECTION 3: MARKETPLACE
// ================================================
async function loadMarketplace() {
    const loading = document.getElementById('marketLoading');
    loading.classList.add('active');

    try {
        const response = await fetch(`${API_BASE}/match`);
        if (!response.ok) throw new Error('Failed to load marketplace');
        marketplaceData = await response.json();

        document.getElementById('statSellers').textContent = marketplaceData.total_sellers;
        document.getElementById('statBuyers').textContent = marketplaceData.total_buyers;

        renderListings(currentTab);
    } catch (error) {
        showToast(`Marketplace: ${error.message}`);
    } finally {
        loading.classList.remove('active');
    }
}

function switchTab(tab) {
    currentTab = tab;
    document.getElementById('tabSellers').classList.toggle('active', tab === 'sellers');
    document.getElementById('tabBuyers').classList.toggle('active', tab === 'buyers');
    renderListings(tab);
}

function renderListings(tab) {
    const list = document.getElementById('marketplaceList');
    if (!marketplaceData) { list.innerHTML = '<p style="color:var(--color-text-muted);">Loading...</p>'; return; }

    const items = tab === 'sellers' ? marketplaceData.sellers : marketplaceData.buyers;
    list.innerHTML = items.map(item => {
        if (tab === 'sellers') {
            return `<div class="listing-card">
                <div class="listing-info">
                    <div class="listing-name">🌱 ${item.name}</div>
                    <div class="listing-meta">
                        <span>📍 ${item.region}</span>
                        <span>🏷️ ${item.variety}</span>
                        <span class="quality-badge ${item.quality.toLowerCase()}" style="padding:2px 8px;font-size:0.7rem;">${item.quality}</span>
                        <span>📦 ${(item.available_kg / 1000).toFixed(1)}t available</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="listing-price">$${item.price_per_kg.toFixed(2)}/kg</div>
                    <div class="listing-rating">⭐ ${item.rating}</div>
                </div>
            </div>`;
        } else {
            return `<div class="listing-card">
                <div class="listing-info">
                    <div class="listing-name">🛒 ${item.name}</div>
                    <div class="listing-meta">
                        <span>🌍 ${item.country}</span>
                        <span>📍 ${item.preferred_region || 'Any region'}</span>
                        <span>📊 Min: ${item.min_quality}</span>
                        <span>📦 Needs ${(item.volume_needed_kg / 1000).toFixed(1)}t</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="listing-price">≤$${item.max_price_per_kg.toFixed(2)}/kg</div>
                    <div class="listing-rating">⭐ ${item.rating}</div>
                </div>
            </div>`;
        }
    }).join('');
}

// ================================================
// UTILITY FUNCTIONS
// ================================================
function getMonthName(m) {
    return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m - 1] || '?';
}

function getQualityEmoji(q) {
    return { High: '🟢', Medium: '🟡', Low: '🔴' }[q] || '⚪';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

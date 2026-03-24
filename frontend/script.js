/**
 * ================================================
 * AI2CUP — Frontend JavaScript
 * ================================================
 * Ethiopian coffee trade platform.
 * Handles API calls, dual currency (ETB/USD), ECX grading,
 * and marketplace display.
 * ================================================
 */

const API_BASE = '/api';

// State
let selectedFile = null;
let currentTab = 'sellers';
let marketplaceData = null;

// ================================================
// INITIALIZATION
// ================================================
document.addEventListener('DOMContentLoaded', () => {
    loadMarketplace();
    setupDragAndDrop();
    setupNavigation();
});

// ================================================
// NAVIGATION — smooth scroll, active tab highlight
// ================================================
function setupNavigation() {
    document.querySelectorAll('.navbar-nav a').forEach(link => {
        link.addEventListener('click', () => {
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
    toast.innerHTML = `${type === 'success' ? '✅' : '❌'} ${message}`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ================================================
// SECTION 1: PRICE PREDICTION (ETB + USD)
// ================================================
async function predictPrice() {
    const btn = document.getElementById('predictBtn');
    const spinner = document.getElementById('priceSpinner');
    const btnText = document.getElementById('predictBtnText');

    const payload = {
        region: document.getElementById('regionSelect').value,
        month: parseInt(document.getElementById('monthSelect').value),
        altitude: parseFloat(document.getElementById('altitudeInput').value),
        rainfall: parseFloat(document.getElementById('rainfallInput').value),
        variety: document.getElementById('varietySelect').value,
        processing: document.getElementById('processingSelect').value,
        ecx_grade: parseInt(document.getElementById('ecxGradeSelect').value),
    };

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
        loadMonthlyChart(payload.region, payload.altitude, payload.rainfall,
                         payload.variety, payload.processing, payload.ecx_grade);
        showToast('Price prediction complete!', 'success');
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        spinner.classList.remove('active');
        btnText.textContent = '🔮 Predict Price · ዋጋ ተንብይ';
    }
}

function displayPriceResult(data) {
    document.getElementById('priceResult').classList.add('visible');

    // Dual currency display
    document.getElementById('predictedPriceETB').textContent =
        `${data.predicted_price_etb.toFixed(2)} ETB`;
    document.getElementById('predictedPriceUSD').textContent =
        `$${data.predicted_price_usd.toFixed(2)}`;

    // ECX Grade label
    document.getElementById('ecxGradeLabel').textContent = data.ecx_grade_label;

    // Details grid
    const inputs = data.inputs;
    document.getElementById('priceResultDetails').innerHTML = `
        <div class="result-detail-item"><div class="result-detail-label">Region</div><div class="result-detail-value">${inputs.region}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Month</div><div class="result-detail-value">${getMonthName(inputs.month)}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Altitude</div><div class="result-detail-value">${inputs.altitude}m</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Rainfall</div><div class="result-detail-value">${inputs.rainfall}mm</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Variety</div><div class="result-detail-value">${inputs.variety}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Processing</div><div class="result-detail-value">${inputs.processing}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">ECX Grade</div><div class="result-detail-value">Grade ${inputs.ecx_grade}</div></div>
        <div class="result-detail-item"><div class="result-detail-label">Model</div><div class="result-detail-value">${data.model_info}</div></div>
    `;
}

// ── Monthly Price Chart (ETB) ──
async function loadMonthlyChart(region, altitude, rainfall, variety, processing, ecx_grade) {
    const chartContainer = document.getElementById('priceChart');
    const chartBars = document.getElementById('chartBars');
    chartBars.innerHTML = '<div style="color:var(--color-text-dim);font-size:0.85rem;padding:var(--space-md);">Loading chart...</div>';
    chartContainer.classList.add('visible');

    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const prices = [];

    // Fetch all 12 months in parallel
    const promises = [];
    for (let m = 1; m <= 12; m++) {
        promises.push(
            fetch(`${API_BASE}/predict-price`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region, month: m, altitude, rainfall, variety, processing, ecx_grade }),
            }).then(r => r.json()).then(d => d.predicted_price_etb).catch(() => 0)
        );
    }
    const results = await Promise.all(promises);
    prices.push(...results);

    const maxPrice = Math.max(...prices, 1);
    chartBars.innerHTML = '';

    for (let i = 0; i < 12; i++) {
        const heightPct = (prices[i] / maxPrice) * 100;
        const group = document.createElement('div');
        group.className = 'chart-bar-group';
        group.innerHTML = `
            <div class="chart-bar-value">${prices[i].toFixed(0)}</div>
            <div class="chart-bar" style="height:${heightPct}%" title="${months[i]}: ${prices[i].toFixed(2)} ETB/kg"></div>
            <div class="chart-bar-label">${months[i]}</div>
        `;
        chartBars.appendChild(group);
    }
}

// ================================================
// SECTION 2: QUALITY DETECTION (ECX Grading)
// ================================================
function setupDragAndDrop() {
    const area = document.getElementById('uploadArea');
    ['dragenter','dragover'].forEach(evt => {
        area.addEventListener(evt, e => { e.preventDefault(); area.classList.add('drag-over'); });
    });
    ['dragleave','drop'].forEach(evt => {
        area.addEventListener(evt, e => { e.preventDefault(); area.classList.remove('drag-over'); });
    });
    area.addEventListener('drop', e => {
        if (e.dataTransfer.files.length > 0) processFile(e.dataTransfer.files[0]);
    });
}

function handleFileSelect(event) {
    if (event.target.files[0]) processFile(event.target.files[0]);
}

function processFile(file) {
    if (!file.type.startsWith('image/')) { showToast('Please upload an image file'); return; }
    if (file.size > 10 * 1024 * 1024) { showToast('File too large. Maximum 10MB.'); return; }
    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    const reader = new FileReader();
    reader.onload = e => {
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
        const response = await fetch(`${API_BASE}/analyze-quality`, { method: 'POST', body: formData });
        if (!response.ok) { const err = await response.json(); throw new Error(err.detail || 'Analysis failed'); }
        const data = await response.json();
        displayQualityResult(data);
        showToast('Quality analysis complete!', 'success');
    } catch (error) {
        showToast(`Error: ${error.message}`);
    } finally {
        btn.disabled = false;
        spinner.classList.remove('active');
        btnText.textContent = '🔬 Analyze Quality · ጥራት ተንትን';
    }
}

function displayQualityResult(data) {
    document.getElementById('qualityResult').classList.add('visible');

    // Quality badge
    const badge = document.getElementById('qualityBadge');
    badge.textContent = `${getQualityEmoji(data.quality)} ${data.quality}`;
    badge.className = `quality-badge ${data.quality.toLowerCase()}`;

    // ECX Grade badge
    const ecxBadge = document.getElementById('ecxGradeBadge');
    ecxBadge.textContent = `ECX ${data.ecx_label}`;
    ecxBadge.className = 'ecx-grade-badge';

    // Amharic grade name
    document.getElementById('ecxAmharic').textContent = data.ecx_amharic || '';

    // Description
    document.getElementById('qualityDescription').textContent = data.description;

    // Export eligibility
    const exportEl = document.getElementById('exportEligible');
    if (data.export_eligible) {
        exportEl.innerHTML = '🟢 <strong>Export Eligible</strong> — ለወጭ ንግድ ብቁ';
        exportEl.style.color = 'var(--color-success)';
    } else {
        exportEl.innerHTML = '🔴 <strong>Domestic Only</strong> — ለአገር ውስጥ ገበያ ብቻ';
        exportEl.style.color = 'var(--color-danger)';
    }

    // Confidence bar
    const pct = Math.round(data.confidence * 100);
    document.getElementById('confidenceValue').textContent = `${pct}%`;
    setTimeout(() => { document.getElementById('confidenceFill').style.width = `${pct}%`; }, 100);

    // Details
    const detailsEl = document.getElementById('qualityDetails');
    let html = '';
    // Add defect count and SCAA score
    html += `<div class="result-detail-item"><div class="result-detail-label">Defects</div><div class="result-detail-value">${data.defect_count}</div></div>`;
    html += `<div class="result-detail-item"><div class="result-detail-label">SCAA Score</div><div class="result-detail-value">${data.scaa_score_range}</div></div>`;
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
    if (!marketplaceData) { list.innerHTML = '<p style="color:var(--color-text-muted)">Loading...</p>'; return; }

    const items = tab === 'sellers' ? marketplaceData.sellers : marketplaceData.buyers;

    list.innerHTML = items.map(item => {
        if (tab === 'sellers') {
            const certs = (item.certification || []).map(c => `<span class="cert-tag">${c}</span>`).join('');
            return `<div class="listing-card">
                <div class="listing-info">
                    <div class="listing-name">🌱 ${item.name}</div>
                    ${item.name_amharic ? `<div class="listing-amharic">${item.name_amharic}</div>` : ''}
                    <div class="listing-meta">
                        <span>📍 ${item.region}</span>
                        <span>🏷️ ${item.variety}</span>
                        <span>⚙️ ${item.processing}</span>
                        <span class="quality-badge ${item.quality.toLowerCase()}" style="padding:2px 8px;font-size:0.65rem;">ECX G${item.ecx_grade}</span>
                        <span>📦 ${(item.available_kg / 1000).toFixed(0)}t</span>
                    </div>
                    <div class="listing-certs">${certs}</div>
                </div>
                <div style="text-align:right;">
                    <div class="listing-price">${item.price_per_kg_etb} ETB</div>
                    <div class="listing-price-usd">$${item.price_per_kg_usd}/kg</div>
                    <div class="listing-rating">⭐ ${item.rating}</div>
                    ${item.members ? `<div class="listing-members">👥 ${item.members.toLocaleString()} farmers</div>` : ''}
                </div>
            </div>`;
        } else {
            const certs = (item.certification_required || []).map(c => `<span class="cert-tag">${c}</span>`).join('');
            return `<div class="listing-card">
                <div class="listing-info">
                    <div class="listing-name">🛒 ${item.name}</div>
                    <div class="listing-meta">
                        <span>🌍 ${item.country}</span>
                        <span>📍 ${item.preferred_region || 'Any region'}</span>
                        <span>📊 Min: ${item.min_quality} (G${item.max_ecx_grade})</span>
                        <span>📦 Needs ${(item.volume_needed_kg / 1000).toFixed(0)}t</span>
                    </div>
                    ${certs ? `<div class="listing-certs">Requires: ${certs}</div>` : ''}
                </div>
                <div style="text-align:right;">
                    <div class="listing-price">≤${item.max_price_per_kg_etb} ETB</div>
                    <div class="listing-price-usd">≤$${item.max_price_per_kg_usd}/kg</div>
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

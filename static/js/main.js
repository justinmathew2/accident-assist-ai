document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const btnUpload = document.getElementById('btn-upload');
    const btnRecord = document.getElementById('btn-record');
    const fileInput = document.getElementById('file-input');
    const aiSection = document.querySelector('.ai-section');
    const aiDescription = document.querySelector('.ai-description');
    const badgeStatus = document.querySelector('.badge-status');
    const mainContent = document.querySelector('.main-content');
    
    // Navigation Elements
    const navReport = document.getElementById('nav-report');
    const navStatus = document.getElementById('nav-status');
    const navHistory = document.getElementById('nav-history');

    // Store original content for tab switching
    const originalMainContent = mainContent.innerHTML;

    // --- 1. Tab Switching Logic ---
    const switchTab = (tabId) => {
        // Update active class
        [navReport, navStatus, navHistory].forEach(nav => nav.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');

        if (tabId === 'nav-report') {
            mainContent.innerHTML = originalMainContent;
            // Re-bind events after restoring HTML
            bindReportEvents();
        } else {
            mainContent.innerHTML = `
                <div class="fade-in" style="padding: 2rem; text-align: center; margin-top: 4rem;">
                    <div class="icon-container" style="margin: 0 auto 1.5rem; width: 5rem; height: 5rem; font-size: 2.5rem;">🚧</div>
                    <h2 style="margin-bottom: 1rem;">Coming Soon</h2>
                    <p style="color: var(--on-surface-variant);">The <strong>${tabId.split('-')[1].charAt(0).toUpperCase() + tabId.split('-')[1].slice(1)}</strong> module is under development for the hackathon finale.</p>
                    <button class="btn-emergency" style="height: 3rem; margin-top: 2rem; background: var(--primary);" onclick="location.reload()">
                        <span style="font-size: 0.9rem;">Back to Report</span>
                    </button>
                </div>
            `;
        }
    };

    navReport.addEventListener('click', (e) => { e.preventDefault(); switchTab('nav-report'); });
    navStatus.addEventListener('click', (e) => { e.preventDefault(); switchTab('nav-status'); });
    navHistory.addEventListener('click', (e) => { e.preventDefault(); switchTab('nav-history'); });

    // --- 2. Report Functionality ---
    const handleIncidentReport = async (type, file = null) => {
        // UI Transition to Processing
        badgeStatus.textContent = 'Analyzing...';
        badgeStatus.classList.add('pulse');
        aiDescription.innerHTML = `<p class="pulse"><strong>Analyzing Bengaluru Traffic & Incident...</strong></p><p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">Cross-referencing Hebbal & Silk Board gridlock data...</p>`;

        try {
            let payload = {
                type: type,
                description: `Emergency ${type} reported via incident card.`,
                location: 'Silk Board', // Simulated location
                timestamp: new Date().toISOString()
            };

            // If a file is provided, we could convert it to Base64 (simplified for demo)
            if (file) {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                await new Promise(resolve => reader.onload = resolve);
                payload.image_data = reader.result;
            }

            const response = await fetch('/api/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            renderActionCard(data);

        } catch (error) {
            console.error('Error reporting incident:', error);
            badgeStatus.textContent = 'Error';
            aiDescription.textContent = 'Failed to process incident report. Please try again.';
        }
    };

    const renderActionCard = (data) => {
        const { triage, mobility } = data;
        const aiSectionInDOM = document.querySelector('.ai-section');
        
        aiSectionInDOM.innerHTML = '';
        aiSectionInDOM.classList.add('fade-in');

        const cardHtml = `
            <div class="ai-header">
                <div class="icon-container" style="background: var(--primary); color: white; width: 2.5rem; height: 2.5rem; font-size: 1rem;">
                    🛡️
                </div>
                <div style="flex: 1">
                    <div style="font-weight: 700; font-size: 0.9rem;">Emergency Action Card</div>
                    <div class="label-data" style="font-size: 0.65rem;">Triage Level ${triage.triage_level}</div>
                </div>
                <span class="badge-status" style="background: var(--secondary)">ACTIVE REPORT</span>
            </div>
            
            <div class="action-card-result">
                <h3 class="severity-${triage.severity}">${triage.severity} SEVERITY</h3>
                <p style="font-size: 0.9rem; margin-top: 0.5rem; color: var(--on-surface-variant)">
                    ${triage.incident_summary}
                </p>

                <div style="margin-top: 1rem; padding: 0.75rem; background: var(--surface-container-low); border-radius: var(--radius-md); border-left: 3px solid var(--secondary);">
                    <div class="label-data" style="font-size: 0.6rem;">Forensic Analysis</div>
                    <div style="font-size: 0.8rem; font-style: italic;">"${triage.forensic_notes}"</div>
                    <div style="font-weight: 800; font-size: 0.75rem; margin-top: 0.4rem; color: var(--secondary);">${triage.ambulance_priority}</div>
                </div>
                
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--outline-variant);">
                    <div class="label-data" style="color: var(--primary)">Mobility Impact</div>
                    <div style="font-weight: 700; font-size: 0.85rem;">${mobility.reason}</div>
                    <div style="font-size: 0.8rem; color: var(--secondary)">Risk Level: ${mobility.risk_level} (+${mobility.ambulance_eta_modifier}m ETA)</div>
                </div>

                <div style="margin-top: 1rem;">
                    <div class="label-data">Recommended Actions</div>
                    <ul style="font-size: 0.85rem; padding-left: 1.2rem; margin-top: 0.5rem;">
                        ${triage.recommended_actions.map(action => `<li>${action}</li>`).join('')}
                    </ul>
                </div>
            </div>

            <button class="btn-emergency" style="height: 3.5rem; margin-top: 1.5rem; background: var(--primary);" 
                    onclick="window.location.reload()">
                <div class="btn-emergency-text" style="font-size: 1rem;">DISMISS & LOG</div>
            </button>
        `;

        aiSectionInDOM.innerHTML = cardHtml;
    };

    const bindReportEvents = () => {
        const bUp = document.getElementById('btn-upload');
        const bRec = document.getElementById('btn-record');
        
        if (bUp) {
            bUp.addEventListener('click', () => {
                const fInput = document.getElementById('file-input');
                if (fInput) fInput.click();
            });
        }

        if (bRec) {
            bRec.addEventListener('click', () => handleIncidentReport('voice'));
        }
    };

    // Listen for file selection
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleIncidentReport('visual', e.target.files[0]);
            }
        });
    }

    // Initial binding
    bindReportEvents();
});

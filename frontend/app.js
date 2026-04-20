const contentArea = document.getElementById('main-content');
const navButtons = document.querySelectorAll('.nav-btn');

// API Base URL (adjust if port changes)
const API_URL = 'http://127.0.0.1:8000/api';

const posMap = {
    'Forward': '공격수',
    'Midfielder': '미드필더',
    'Defender': '수비수',
    'Goalkeeper': '골키퍼'
};

const contMap = {
    'Asia': '아시아',
    'Europe': '유럽',
    'Africa': '아프리카',
    'South America': '남미',
    'North America': '북미'
};

const natMap = {
    'South Korea': '대한민국',
    'England': '잉글랜드',
    'Norway': '노르웨이',
    'Belgium': '벨기에',
    'Egypt': '이집트',
    'Brazil': '브라질'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadView('dashboard');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active state
            navButtons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // Load view
            loadView(e.target.dataset.view);
        });
    });
});

window.showNationPlayers = function(nationId) {
    navButtons.forEach(b => b.classList.remove('active'));
    document.querySelector('[data-view="players"]').classList.add('active');
    loadView('players', nationId);
};

async function loadView(view, param = null) {
    contentArea.innerHTML = '<span class="loader"></span>';
    
    try {
        if (view === 'dashboard') {
            await renderDashboard();
        } else if (view === 'nations') {
            await renderNations();
        } else if (view === 'players') {
            await renderPlayers(param);
        }
    } catch (error) {
        console.error("Error loading view:", error);
        contentArea.innerHTML = `<p style="color: #ef4444;">데이터를 불러오는 중 오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인해주세요.</p>`;
    }
}

async function fetchFromAPI(endpoint) {
    const res = await fetch(`${API_URL}${endpoint}`);
    if (!res.ok) throw new Error("API Network Error");
    return res.json();
}

async function renderDashboard() {
    const data = await fetchFromAPI('/dashboard');
    
    let html = `<h1>대시보드 개요</h1>`;
    
    // Top Performers section
    html += `<div class="dashboard-section">
        <h2>최고의 활약 선수 (평점 순)</h2>
        <div class="grid-container">`;
        
    data.top_performers.forEach(player => {
        const nation_kr = natMap[player.nation_name] || player.nation_name;
        const position_kr = posMap[player.position] || player.position;
        html += `
            <div class="glass-card">
                <div class="top-performer-header">
                    <div style="display:flex; align-items:center;">
                        <img src="${player.image_url}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; margin-right: 15px; border: 2px solid var(--primary-color);">
                        <img src="${player.flag_url}" class="flag-icon" alt="${nation_kr}" title="${nation_kr}" style="width: 30px; height: 20px;">
                    </div>
                    <span class="rating-badge">${player.rating}</span>
                </div>
                <div class="player-name">${player.name}</div>
                <div class="player-meta">${player.club_name} • ${position_kr}</div>
                
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-value">${player.goals}</div>
                        <div class="stat-label">골</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${player.assists}</div>
                        <div class="stat-label">도움</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += `</div></div>`;
    
    // Global Hitmap Stats
    html += `<div class="dashboard-section">
        <h2>국가별 리그 기여도</h2>
        <div class="grid-container">`;
        
    data.hitmap.forEach(nation => {
        const nation_kr = natMap[nation.name] || nation.name;
        const cont_kr = contMap[nation.continent] || nation.continent;
        html += `
            <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.2rem; font-weight:800;">${nation_kr}</div>
                    <div class="player-meta">${cont_kr}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2rem; font-weight: 800; color: var(--primary-color)">${nation.player_count}</div>
                    <div class="stat-label">EPL 소속 선수</div>
                </div>
            </div>
        `;
    });
        
    html += `</div></div>`;
    
    contentArea.innerHTML = html;
}

async function renderNations() {
    const nations = await fetchFromAPI('/nations');
    
    let html = `<h1>국가별 리그 기록</h1>
        <div class="grid-container">`;
        
    nations.forEach(n => {
        const nation_kr = natMap[n.name] || n.name;
        const cont_kr = contMap[n.continent] || n.continent;
        html += `
            <div class="glass-card" style="cursor: pointer;" onclick="showNationPlayers(${n.id})" title="클릭하여 선수 보기">
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                    <img src="${n.flag_url}" class="flag-icon" alt="${nation_kr}">
                    <div>
                        <div style="font-size: 1.3rem; font-weight: bold;">${nation_kr}</div>
                        <div class="player-meta">${cont_kr}</div>
                    </div>
                </div>
                
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-value">${n.player_count}</div>
                        <div class="stat-label">선수 수</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${n.total_goals}</div>
                        <div class="stat-label">총 득점</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${n.total_assists}</div>
                        <div class="stat-label">총 도움</div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 15px; font-size: 0.85rem; color: var(--primary-color);">
                    ➔ 선수 목록 보기
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    contentArea.innerHTML = html;
}

async function renderPlayers(nationId) {
    const endpoint = nationId ? `/players?nation_id=${nationId}` : '/players';
    const players = await fetchFromAPI(endpoint);
    
    let html = `<h1>선수 아카이브 ${nationId && players.length > 0 ? `(${natMap[players[0].nation_name] || players[0].nation_name})` : ''}</h1>`;
    
    if (players.length === 0) {
        html += `<p style="color: var(--text-muted); margin-top: 20px;">기록된 해당 국가 선수가 없습니다.</p>`;
        contentArea.innerHTML = html;
        return;
    }

    html += `<div class="grid-container" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">`;
        
    players.forEach(p => {
        const nation_kr = natMap[p.nation_name] || p.nation_name;
        const position_kr = posMap[p.position] || p.position;
        html += `
            <div class="glass-card" style="display:flex; flex-direction:column;">
                <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div style="display:flex; align-items:flex-end;">
                        <img src="${p.image_url}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid rgba(59, 130, 246, 0.5);">
                        <img src="${p.flag_url}" class="flag-icon" alt="${nation_kr}" title="${nation_kr}" style="width: 30px; height: 20px; margin-left: -15px; z-index: 2; border: 1px solid #1f2937;">
                    </div>
                    <div class="rating-badge" style="background: rgba(59,130,246,0.2); color: var(--primary-color); border: 1px solid rgba(59,130,246,0.5);">
                        ★ ${p.rating || 'N/A'}
                    </div>
                </div>
                <div class="player-name">${p.name}</div>
                <div class="player-meta">${p.club_name}</div>
                <div class="player-meta" style="margin-bottom: 10px;">${position_kr} • 출생: ${p.birth_date}</div>
                
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-value" style="font-size: 1.1rem">${p.goals || 0}</div>
                        <div class="stat-label">골</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" style="font-size: 1.1rem">${p.assists || 0}</div>
                        <div class="stat-label">도움</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" style="font-size: 1.1rem">${p.minutes_played || 0}</div>
                        <div class="stat-label">출장(분)</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    contentArea.innerHTML = html;
}

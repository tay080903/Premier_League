# ⚽ EPL National Stats (프리미어리그 국가별 선수 전적 시스템)

잉글랜드 프리미어리그(EPL)에서 활약하는 선수들의 데이터를 **'국적'**이라는 관점에서 재구성하여 제공하는 웹 플랫폼입니다. 특정 국가 출신 선수들의 통합 전적과 개별 활약상을 한눈에 비교할 수 있습니다.

---

## 🚀 프로젝트 개요
- **목적**: EPL 내 다양한 국적 선수들의 데이터를 시각화하여 국가별 기여도 및 성적 확인
- **주요 타겟**: 데이터 기반 축구 분석을 즐기는 팬, 특정 국가(예: 한국) 선수들의 활약상을 추적하고 싶은 사용자

## 🛠 기술 스택 (Technical Stack)
- **Frontend**: React.js / Vite (빠른 빌드 및 컴포넌트 기반 UI 구성)
- **Backend**: Python / FastAPI 또는 Flask (전적 데이터 처리 API)
- **Database**: PostgreSQL 또는 MySQL (선수 정보, 경기 기록, 국가 통계 저장)
- **Deployment**: Vercel (Frontend) / AWS (Backend)

---

## 📌 주요 메뉴 구성 (Navigation)

1. **Dashboard (홈)**: 리그 전체 요약 및 실시간으로 가장 뛰어난 활약을 펼치는 국가/선수 하이라이트
2. **Nationalities (국가별 보기)**: 대륙별/국가별 카테고리 필터링 (예: 유럽, 아시아, 남미 등)
3. **League Table (국가 기여도)**: 골, 도움 등 주요 지표를 합산하여 어느 나라 선수들이 리그를 주도하는지 보여주는 랭킹
4. **Player Archives (선수 사전)**: 이름, 클럽, 포지션별 선수 검색 및 전체 데이터 조회
5. **Insights (커뮤니티)**: 선수 비교 분석 및 차기 시즌 국적별 유망주 토론 공간

---

## 💻 주요 화면 구성 (UI/UX)

### 1. 메인 화면 (Landing Page)
- **Global Hitmap**: 전 세계 지도에서 EPL 선수가 배출된 국가를 강조 표시
- **Top Performer**: 주간 평점이 가장 높은 선수를 국기와 함께 카드 형태로 노출

### 2. 국가별 상세 페이지 (Country Detail)
- **Stats Overview**: 해당 국가 선수들의 총 득점, 총 어시스트, 최다 출전 선수 정보 요약
- **Player Grid**: 해당 국적 선수들의 리스트를 소속 클럽 엠블럼과 함께 그리드 레이아웃으로 배치
- **Historical Legends**: 현재 활동 선수뿐만 아니라 해당 국가 출신의 역대 레전드 누적 기록 섹션

### 3. 선수 상세 데이터 (Player Statistics)
- **Performance Chart**: 레이더 차트를 통한 능력치(공격, 수비, 피지컬 등) 시각화
- **Trend Graph**: 시즌별 득점 및 평점 추이를 선 그래프로 표시

---

## 📂 데이터베이스 구조 (Database Schema)

- **`nations`**: `id`, `name`, `flag_url`, `continent`
- **`players`**: `id`, `name`, `nation_id`, `club_name`, `position`, `birth_date`
- **`match_stats`**: `id`, `player_id`, `goals`, `assists`, `minutes_played`, `rating`, `season`

---

## ⚙️ 실행 방법 (Local Setup)

```bash
# 저장소 복제
git clone [https://github.com/username/epl-national-stats.git](https://github.com/username/epl-national-stats.git)

# 프론트엔드 설정
cd frontend
npm install
npm run dev

# 백엔드 설정
cd backend
pip install -r requirements.txt
python main.py
import streamlit as st
import web_page.registration as registration
#import web_page.demand as demand
import web_page.demandt as demandt
import web_page.faq as faq
import web_page.faqt as faqt
import web_page.home as home

# 페이지 기본 설정
st.set_page_config(
    page_title="친환경 자동차 현황",
    page_icon="🚗",
    layout="wide"
)

# 사이드바 메뉴
st.sidebar.title("📂 MENU")
menu = st.sidebar.radio(
    "페이지를 선택하세요:",
    ["🏠 Home", "📊 친환경 자동차 등록 현황", "📈 국내 주요 5사 자동차 분석", "📈 국내 주요 5사 자동차 분석(test)", "❓ FAQ", "❓ FAQ(test)"],
    key="main_menu"
)

# 각 메뉴에 따라 페이지 로드
if menu == "🏠 Home":
    home.run()
elif menu == "📊 친환경 자동차 등록 현황":
    registration.run()
#elif menu == "📈 국내 주요 5사 자동차 분석":
    #demand.run()
elif menu == "📈 국내 주요 5사 자동차 분석(test)":
    demandt.run()
elif menu == "❓ FAQ":
    faq.run()
elif menu == "❓ FAQ(test)":
    faqt.run()

st.write("")  # 빈 줄
st.write("---")  # 구분선
st.write("")  # 빈 줄

st.markdown("""
    # 👋🏻 팀 소개 👋🏻
## 📌 팀 명
SKN09-1st-2Team : 🌟 blank 🌟


## 📌 팀 멤버

  :man: 김우중(@kwj9942): Crawling,(담당작성)

  
  :girl: 김하늘(@nini12091): Crawling, Streamlit, (담당작성)

  
  :girl: 전성원(@hack012): Crawling, DB, Streamlit, ReadME

  
  :girl: 박유진(@YUJINDL01): Crawling, (담당작성)

  

## :blue_car: 국내 친환경 자동차(전기 & 하이브리드) 현황 및 데이터 통합 플랫폼 🚗
### 📌 개발 기간
2025.01.06 ~ 2025.01.08 (총 3일)

### 📌 프로젝트 내용
국내 하이브리드 및 전기자동차 등록 현황과 주요 자동차 제조사의 수요데이터를 시각화하고, 전기차 관련 FAQ 정보를 제공하는 플랫폼

### 📌 프로젝트 필요성
- 친환경 자동차 수요 증가

환경 규제와 탄소 배출 감소 노력으로 인해 하이브리드 및 전기 자동차의 수요가 빠르게 증가

- 전기차 선택을 위한 맞춤형 정보 제공

전기차 관련 FAQ와 트렌드 데이터를 통합적으로 제공함으로써 소비자와 관련 업계의 정보 접근성을 높이고, 신뢰할 수 있는 데이터를 기반으로 올바른 선택을 할 수 있도록 지원

### 📌 프로젝트 목표
:one: **국내 하이브리드 및 전기 자동차 등록 현황 시각화**
  - 지도 기반 지역별 등록 현황 및 막대 그래프를 통한 자동차별 등록 현황 제공

:two: **주요 5대 자동차 제조사의 수요 현황 분석**
  - 연도별 수요 데이터를 선 그래프로 시각화하고, 하이브리드 및 전기차 수요 비중을 파악

:three: **전기차 관련 FAQ 제공**
  - 전기차에 대한 주요 질문과 답변을 크롤링하여 사용자 친화적인 방식으로 제공

### 📌 기술 스택 :chart_with_upwards_trend: 
  :heavy_check_mark: **프론트엔드 및 대시보드** : Streamlit


  :heavy_check_mark: **데이터베이스**: MySQL


  :heavy_check_mark: **데이터 처리 및 분석**: Pandas, Numpy


  :heavy_check_mark: **시각화**: map, plotly, Matplotlib


  :heavy_check_mark: **데이터수집**: BeautifulSoup4, Selenium

### 📌 WBS
|작업 명|시작일|종료일|담당자|산출물|의존작업|
|------|------|------|------|--------|-------------|
|프로젝트 주제 선정|01-02|01-06|ALL|없음|없음|
|Streamlit 화면 설계 및 구현|01-05|01-08|전성원, 김하늘|설계파일 WEB 화면|없음|
|Streamlit-DB연동|01-07|01-07|전성원|DB table|Streamlit 화면|
|FAQ 크롤링|01-06|01-07|ALL|csv, .xlsx|Streamlit 작업|
|5사 수요데이터 수집|01-06|01-07|ALL|csv, .xlsx|Streamlit 작업|
|ERD 작성|01-07|01-08|박유진,전성원|ERD 다이어그램|없음|
|코드 취합|01-07|01-08|ALL|Web 페이지/ DB 데이터|크롤링, 데이터수집|
|최종 점검|01-08|01-08|ALL|Web 페이지|없음|

#### :robot: 주요기능
1. **전기차 등록 현황 시각화**
  - 지도(Map) 기반의 지역별 등록 현황 표시
  - bar그래프를 통한 자동차별 등록 현황 비교
  - pie그래프를 통한 화석연료 vs 친환경(전기, 하이브리드) 자동차 비율 비교
2. **주요 5사 수요 현황 분석**
  - 연도별 수요 데이터 트렌드 제공(line 그래프)
  - 하이브리드 및 전기차의 수요 비중(%)시각화
3. **전기차 FAQ 제공**
  - 크롤링을 통해 수집한 자동차 관련 주요 질문과 답변 제공

#### :open_hands: 주요산출물
1. 지역별 및 자동차별 등록 현황 시각화 결과
2. 주요 5사 수요 데이터 분석 그래프
3. 통합된 전기차 FAQ 데이터셋과 검색 인터페이스(검색기능 안돼면 수정 필요)
4. 직관적인 웹 기반 대시보드.

### 📌 데이터베이스 (ERD)
image


### 📌 프로젝트 수행 결과 (최종 streamlit UI)
차량 소비자 증가 그래프	국산 차량 브랜드 순위
image	image
상위 차량 브랜드의 모델	상위 차량 브랜드 통합 FAQ 조회 시스템
image	image

### 📌 한줄회고
- 김우중:
- 김하늘:
- 전성원: 재미(?)있었습니다.. 🙂
- 박유진:

""")